from collections import Counter
from enum import Enum
from typing import cast, Optional

from ipydatagrid import DataGrid

from components.sidebars.entity_sidebar import EntityExtractSidebar, CommonEntitiesSidebar

from tools.parse import *
from tools.text import *
import solara, solara.lab

from assets.entity_state import EntityState

cell_column = solara.reactive(cast(Optional[str],None))
cell_indx = solara.reactive(cast(Optional[int], None))
cell_value = solara.reactive(cast(Optional[str], ""))

class SidebarType(Enum):
    PARSE = 0
    COMMON_ENTS = 1

@solara.component
def Page():

    chosen_column = State.chosen_column.value

    side_bar_type, set_type = solara.use_state(SidebarType.PARSE)


    def change_sidebar(signal):
        new_sidebar = SidebarType(signal)
        set_type(new_sidebar)

    df = None
    datagrid = None

    if parse_data.finished:
        df = parse_data.value
    elif State.chosen_dataframe.value is not None:
        df = State.get_dataframe(State.chosen_dataframe.value)

    with solara.lab.Tabs(on_value=change_sidebar):
        with solara.lab.Tab("Data view", disabled=df is None):
            if side_bar_type == SidebarType.PARSE:
                EntityExtractSidebar()
            if side_bar_type == SidebarType.COMMON_ENTS:
                CommonEntitiesSidebar()
            with solara.Card():
                with solara.Columns([1,2]):
                    if df is not None:
                        with solara.Column():
                            column = State.chosen_column.value
                            dff = df[[column]] if column is not None else df.copy()
                            dg = DataGrid.element(dataframe=dff, selection_mode="cell", editable=False,
                                                        base_column_size=200)
                            datagrid = dg
                        with solara.Column():
                            cell = None
                            if cell_indx.value is not None and cell_column.value is not None:
                                dataframe_names = State.dataframe_names.value
                                chosen_dataframe = State.chosen_dataframe.value
                                dataframes = State.dataframes.value
                                dataframe = dataframes[dataframe_names.index(chosen_dataframe)]
                                # cell_indx.set(cell_dict['row'])
                                # column.set(cell_dict['column'])
                                cell = dataframe.iloc[cell_indx.value][cell_column.value]

                            with solara.Card("Entity view", margin=1, elevation=5):
                                # cell_index = State.entity_cell.value
                                    if cell is not None:
                                        if rendered_entities(cell_column.value) in dataframe.columns.to_list():
                                            ent_cell = dataframe.iloc[cell_indx.value][rendered_entities(cell_column.value)]
                                            solara.Markdown(ent_cell)
                                        # solara.Markdown(cell)
                                        with solara.Card(margin=3):
                                            if spacy_doc_col(chosen_column) in dataframe.columns.to_list():
                                                spacy_doc = dataframe.iloc[cell_indx.value][spacy_doc_col(chosen_column)]
                                                counter = Counter()
                                                for ent in spacy_doc.ents:
                                                    counter.update([ent.text])
                                                doc_df = create_entity_doc_df(counter)
                                                doc_df = doc_df.sort_values(ascending=False, by="Corpus #").head(100).reset_index()
                                                State.entity_dataframe = doc_df
                                                # solara.DataFrame(doc_df, cell_actions=[solara.CellAction(icon="mdi-white-balance-sunny", name="Search corpora",
                                                #       on_click=search_corpora)])
                                                solara.DataFrame(doc_df)
                                            with solara.Card("Dependency view", margin=3):
                                                if rendered_entities(cell_column.value) in dataframe.columns.to_list():
                                                    dep_cell = dataframe.iloc[cell_indx.value][rendered_dependency(cell_column.value)]
                                                    solara.Markdown(dep_cell)

        def update_df():
            if datagrid is not None:
                datagrid_widget = cast(DataGrid, solara.get_widget(datagrid))
                datagrid_widget.data = dff
                if chosen_column is not None and (spacy_doc_col(chosen_column) in df.columns.to_list()):
                    datagrid_widget.on_cell_click(set_cell_values)
        solara.use_effect(update_df, None)

        with solara.lab.Tab("Common Entites", disabled=EntityState.common_entities is None or len(EntityState.common_entities) <= 0):
            if EntityState.common_entities is not None and len(EntityState.common_entities) > 0:
                # with solara.Card("Entity breakdown"):
                    with solara.Column():
                        if EntityState.chosen_entity_type.value is not None:
                            entity_df = build_entity_df(EntityState.chosen_entity_type.value)
                            solara.DataFrame(entity_df)
                        # with solara.Row():
                        #     for i, counter in enumerate(State.common_entities.keys()):
                        #         with solara.Column():
                        #             entity_df = build_entity_df(counter)
                        #             solara.DataFrame(entity_df,
                        #                              cell_actions=[solara.CellAction(icon="mdi-white-balance-sunny",
                        #                                                              name="Explore cell",
                        #                                                              on_click=get_corpus_subset)])
                        # with solara.Row():
                        # with solara.Card("Text annotation", margin=1, elevation=5):
                        #     cell_index = State.entity_cell.value
                        #     if cell_index is not None:
                        #         column = State.chosen_column.value
                        #         cell = dataframe.iloc[cell_index['index']][column]
                        #         solara.InputText(label="Document",value=str(cell))
                        #         solara.Button("Save")
                        #         solara.Checkbox(label="Apply to all",value=State.apply_to_all)
                        #         solara.Checkbox(label="Label span", value=State.annotate_span)
                        #         if State.annotate_span.value:
                        #             solara.InputText("Label name")

                # elif df is not None:
                #     column = State.chosen_column.value
                #     dff = df[[column]] if column else df
                #     datagrid = DataGrid.element(dataframe=dff, selection_mode="cell", editable=False,
                #                                 base_column_size=200)
                #     def update_df():
                #         datagrid_widget = cast(DataGrid, solara.get_widget(datagrid))
                #         datagrid_widget.data = dff
                #
                #     solara.use_effect(update_df, None)

# @solara.component
# def ExtractEntities():
#     with solara.Card("Parsing progress"):
#         with solara.Column(margin=3):
#             solara.ProgressLinear(value=parse_data.progress)
#         with solara.Row():
#             solara.Button("Cancel", on_click=parse_data.cancel)

# def on_entity_cell(column, row_index):
#     State.entity_cell.value = {"column" : rendered_entities(column), "index" : row_index}
#
# def on_dep_cell(column, row_index):
#     State.entity_cell.value = {"column": rendered_dependency(column), "index": row_index}


# column_actions = [solara.ColumnAction(icon="mdi-sunglasses", name="Entity extract",
#                                       on_click=parse_data),
                  # solara.ColumnAction(icon="mdi-sunglasses", name="PoS extract",
                  #                     on_click=pos_extract)
#                   ]
# cell_actions = [solara.CellAction(icon="mdi-white-balance-sunny", name="Explore entities",
#                                   on_click=on_entity_cell), solara.CellAction(icon="mdi-white-balance-sunny", name="Explore dependencies",
#                                   on_click=on_dep_cell)]

def build_entity_df(counter):
    def unpack_tuple(tuple_to_unpack):
        if tuple_to_unpack is None:
            return '', '','',''
        return tuple_to_unpack[0],tuple_to_unpack[1],tuple_to_unpack[2],tuple_to_unpack[3]
    entity_df = pd.DataFrame.from_dict(EntityState.common_entities[counter],
                           orient='index').reset_index()
    entity_df = entity_df.rename(columns={'index': counter, 0: 'Count'})

    entity_df['wiki-data'] = entity_df[counter].apply(lambda x: EntityState.entity_wiki[x])
    entity_df = entity_df.sort_values(ascending=False, by="Count").head(100).reset_index()
    return entity_df

def set_cell_values(cell_dict):
    print(cell_dict)
    cell_value.set(cell_dict['cell_value'])
    cell_indx.set(cell_dict['row'])
    cell_column.set(cell_dict['column'])