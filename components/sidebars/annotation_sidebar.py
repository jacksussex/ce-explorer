from components.solara_components.data_upload import DataUpload
from components.solara_components.data_view import DataView
from tools.text import *
from assets.annotation_state import AnnotationState

import solara

drag_and_drop = "Drag and drop data to be upload or try out the tool with an inbuilt sample."

@solara.component
def AnnotationSideBar():
    chosen_dataframe = State.chosen_dataframe.value
    df = None
    # dff = None
    # columns = []
    if chosen_dataframe is not None:
        df = State.get_dataframe(chosen_dataframe)
        AnnotationState.data.set(df)
        # columns = AnnotationState.data.value.columns.tolist()
    # dataframes = State.dataframes.value
    # dataframe_names = State.dataframe_names.value

    with solara.Sidebar():

        ## Upload data component
        DataUpload()

        DataView(df)

        # with solara.Card("Data view", margin=1, elevation=1):
        #     if len(dataframe_names) > 0:
        #         solara.Select("Dataset", values=dataframe_names, value=State.chosen_dataframe, on_value=State.reset_column)
        #     if AnnotationState.data.value is not None:
        #         # df = dataframes[dataframe_names.index(chosen_dataframe)]
        #         # columns = df.columns.tolist()
        #         solara.Select("Column", values=columns, value=State.chosen_column)
        #         with solara.Row(margin=3):
        #             solara.Button("Reset data-view", color="primary", text=True,outlined=True,on_click=State.reset_view)
        if State.chosen_column.value is not None and State.chosen_dataframe.value is not None:
            with solara.Card("Add prefix"):
                solara.InputText(label="Delimiter", value=AnnotationState.pre_delim)
                solara.InputText(label="Add prefix", value=AnnotationState.prefix)
                solara.Checkbox(label="Keep original", value=AnnotationState.pre_keep_orig)
                with solara.Row():
                    solara.Button(label="Add Prefix", on_click=add_column_prefix)
                with solara.Row():
                    if AnnotationState.pre_keep_orig.value:
                        solara.Info("Original column data will be stored at: " + State.chosen_column.value + "_original")
            with solara.Card("Add suffix"):
                solara.InputText(label="Delimiter", value=AnnotationState.suff_delim)
                solara.InputText(label="Add suffix", value=AnnotationState.suffix)
                solara.Checkbox(label="Keep original", value=AnnotationState.suff_keep_orig)
                with solara.Row():
                    solara.Button(label="Add Suffix", on_click=add_column_suffix)
                with solara.Row():
                    if AnnotationState.suff_keep_orig.value:
                        solara.Info("Original column data will be stored at: " + State.chosen_column.value + "_original")
        else:
            with solara.Card():
                solara.Markdown("Please choose a dataset and column to annotate.")

def add_column_prefix():
    dataset = AnnotationState.data.value
    col = State.chosen_column.value
    pre = AnnotationState.prefix.value
    delim = AnnotationState.pre_delim.value
    keep_original = AnnotationState.pre_keep_orig.value
    AnnotationState.annotated_df.set(True)
    AnnotationState.data.set(concatenate_column_prefix(dataset,col,pre,delim,keep_original))
    flip = True if not AnnotationState.annotated_df.value else False
    AnnotationState.annotated_df.set(flip)
    # return data.value


def add_column_suffix():
    dataset = AnnotationState.data.value
    col = State.chosen_column.value
    suff = AnnotationState.suffix.value
    delim = AnnotationState.suff_delim.value
    keep_original = AnnotationState.suff_keep_orig.value
    AnnotationState.data.set(concatenate_column_suffix(dataset,col,suff,delim,keep_original))
    flip = True if not AnnotationState.annotated_df.value else False
    AnnotationState.annotated_df.set(flip)
    # return data.value