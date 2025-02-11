
from typing import cast

from ipydatagrid import DataGrid

from components.sidebars.embedding_sidebar import EmbeddingSidebar
from assets.embedding_state import EmbeddingState
from tools.dataframe import *
import solara
@solara.component
def Page():

    data_table = None
    dff = None

    EmbeddingSidebar()

    if State.chosen_dataframe.value is not None:
        df = State.get_dataframe(State.chosen_dataframe.value)
        embed_cols = EmbeddingState.embedding_columns.value
        if len(embed_cols) > 0:
            dff = df[embed_cols]
        with solara.Column():
            if dff is not None:
                datagrid = DataGrid.element(dataframe=dff, selection_mode="cell", base_column_size=600,editable=False)
                data_table = datagrid
    else:
        solara.Markdown("Please select or upload a dataset to start creating embeddings.")

    def update_df():
        if data_table is not None and dff is not None:
            datagrid_widget = cast(DataGrid, solara.get_widget(data_table))
            datagrid_widget.data = dff

    solara.use_effect(update_df, None)

        # with solara.Column():
            # solara.ProgressLinear(value=processing)
            # with solara.Card("Data selection:"):
            #     with solara.Row():
            #         solara.Checkbox(label="Clean data", value=clean_data, on_value=set_clean_data)
            #         solara.Checkbox(label="Remove stopwords", value=remove_stopwords, on_value=set_remove_stopwords)
            #         solara.Checkbox(label="Keep all annotations", value=keep_annotations, on_value=set_keep_annotations)
            #         solara.Checkbox(label="Combine only", value=combine_only, on_value=set_combine_only)
            #     with solara.Row():
            #         solara.InputText("Custom stopwords - 'comma separated values'", value=custom_stopwords, on_value=set_custom_stopwords)
            #     with solara.Row():
            #         solara.SelectMultiple(label="Column select",values=State.embedding_columns,all_values=df.columns.to_list())
            #     solara.Button(label="Create embeddings", margin=3, on_click=create_embeddings, disabled=len(State.embedding_columns.value)<=0)
            # with solara.Card("Download"):
            #     if (create_sentence_embeddings.finished and data_subset is not None and fields._embedding in data_subset.columns.to_list()):
            #         with solara.Row(margin=3):
            #             solara.FileDownload(create_numpy_dump(data_subset[fields._embedding].to_list()),label="Download embeddings", filename="embeddings.npy")
            #         with solara.Row(margin=3):
            #             solara.FileDownload(data_subset.to_csv(), label="Download data", filename="data.csv")
