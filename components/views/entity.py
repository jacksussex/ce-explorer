from collections import Counter
from tools.parse import *
from tools.dataframe import *
from tools.text import *
import solara
# @solara.component
# def EntityView():
#     chosen_column = State.chosen_column.value
#     df = None
#     if parse_data.finished:
#         df = parse_data.value
#     # State.page_view.set(DataView.ENTITY)
#     with solara.Card():
#         with solara.Columns([1,1]):
#             with solara.Column():
#                 if spacy_doc_col(chosen_column) in df.columns.to_list():
#                     solara.DataFrame(df[[State.chosen_column.value]], column_actions=column_actions,
#                                      cell_actions=cell_actions)
#                     with solara.Column():
#                         with solara.Card("Entity view", margin=1, elevation=5):
#                             cell_index = State.entity_cell.value
#                             if cell_index is not None:
#                                 dataframe_names = State.dataframe_names.value
#                                 chosen_dataframe = State.chosen_dataframe.value
#                                 dataframes = State.dataframes.value
#                                 dataframe = dataframes[dataframe_names.index(chosen_dataframe)]
#                                 cell = dataframe.iloc[cell_index['index']][cell_index['column']]
#                                 solara.Markdown(cell)
#                                 with solara.Card(margin=3):
#                                     spacy_doc = dataframe.iloc[cell_index['index']][spacy_doc_col(chosen_column)]
#                                     counter = Counter()
#                                     for ent in spacy_doc.ents:
#                                         counter.update([ent.text])
#                                     doc_df = create_entity_doc_df(counter)
#                                     doc_df = doc_df.sort_values(ascending=False, by="Corpus #").head(100).reset_index()
#                                     State.entity_dataframe = doc_df
#                                     solara.DataFrame(doc_df, cell_actions=[solara.CellAction(icon="mdi-white-balance-sunny", name="Search corpora",
#                                           on_click=search_corpora)])
#                         # with solara.Row():
#                         with solara.Card("Text annotation", margin=1, elevation=5):
#                             cell_index = State.entity_cell.value
#                             if cell_index is not None:
#                                 column = State.chosen_column.value
#                                 cell = dataframe.iloc[cell_index['index']][column]
#                                 solara.InputText(label="Document",value=str(cell))
#                                 solara.Button("Save")
#                                 solara.Checkbox(label="Apply to all",value=State.apply_to_all)
#                                 solara.Checkbox(label="Label span", value=State.annotate_span)
#                                 if State.annotate_span.value:
#                                     solara.InputText("Label name")
#
#                     if State.common_entities is not None and len(State.common_entities) > 0:
#                         with solara.Card("Entity breakdown"):
#                             with solara.Row():
#                                 for i, counter in enumerate(State.common_entities.keys()):
#                                     with solara.Column():
#                                         entity_df = build_entity_df(counter)
#                                         solara.DataFrame(entity_df,
#                                                          cell_actions=[solara.CellAction(icon="mdi-white-balance-sunny",
#                                                                                          name="Explore cell",
#                                                                                          on_click=get_corpus_subset)])
#                 else:
#                     solara.DataFrame(df[[State.chosen_column.value]], column_actions=column_actions)

@solara.component
def ExtractEntities():

    # with solara.Card("Parsing progress"):
        with solara.Column(margin=3):
            if parse_data.finished or parse_data.not_called:
                solara.ProgressLinear(value=False)
            else:
                solara.ProgressLinear(value=parse_data.progress)
        with solara.Row():
            if not parse_data.finished:
                solara.Button("Cancel", on_click=parse_data.cancel)

def on_entity_cell(column, row_index):
    State.entity_cell.value = {"column" : rendered_entities(column), "index" : row_index}

def on_dep_cell(column, row_index):
    State.entity_cell.value = {"column": rendered_dependency(column), "index": row_index}


column_actions = [solara.ColumnAction(icon="mdi-sunglasses", name="Entity extract",
                                      on_click=parse_data),
                  # solara.ColumnAction(icon="mdi-sunglasses", name="PoS extract",
                  #                     on_click=pos_extract)
                  ]
cell_actions = [solara.CellAction(icon="mdi-white-balance-sunny", name="Explore entities",
                                  on_click=on_entity_cell), solara.CellAction(icon="mdi-white-balance-sunny", name="Explore dependencies",
                                  on_click=on_dep_cell)]

def build_entity_df(counter):
    def unpack_tuple(tuple_to_unpack):
        if tuple_to_unpack is None:
            return '', '','',''
        return tuple_to_unpack[0],tuple_to_unpack[1],tuple_to_unpack[2],tuple_to_unpack[3]
    entity_df = pd.DataFrame.from_dict(State.common_entities[counter],
                           orient='index').reset_index()
    entity_df = entity_df.rename(columns={'index': counter, 0: 'Count'})
    entity_df['wiki-data'] = entity_df[counter].apply(lambda x: State.entity_wiki[x])
    entity_df = entity_df.sort_values(ascending=False, by="Count").head(100).reset_index()
    return entity_df