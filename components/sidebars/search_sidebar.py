from components.solara_components.data_upload import DataUpload
from components.solara_components.dataset_picker import DatasetPicker
from tools.dataframe import *
from tools.text import *
from tools.span import annotate_matches
import solara,solara.lab
from typing import Optional, cast
from assets.search_state import SearchState

# tooltip messages
replace_tooltip = "Selecting this will perform an-place replacement of all matching search phrases."
replace_txt_tooltip = "The text to replace all matches with."
class_label_tooltip = "Label matching text spans with a class/entity label."
case_sens_tooltip = "Specify whether your search should be case-sensitive of not. "
results_dataset_tooltip = "Should search results be stored as a new dataset."

@solara.component
def FindReplaceSidebar():

    # working dataset
    chosen_dataframe = SearchState.chosen_dataframe.value
    # df = None
    # if chosen_dataframe is not None:
    #     df = SearchState.get_dataframe(chosen_dataframe)
    # dataframes = SearchState.dataframes.value

    with solara.Sidebar():

        DataUpload()

        with solara.Card("Data view", margin=1, elevation=1):

            # Choose working dataset
            # if len(dataframes) > 0:
            #     solara.Select("Datasets", values=SearchState.dataframe_names.value, value=SearchState.chosen_dataframe, on_value=SearchState.reset_column)

            # if df is not None:
            #     #  Column search selector
            #     columns = df.columns.tolist()
            #     solara.SelectMultiple("Column", all_values=columns, values=SearchState.chosen_columns)
            #     with solara.Row(margin=3):
            #         solara.Button("Reset data-view", color="primary", text=True,outlined=True,on_click=reset_view)

            DatasetPicker()

            if len(SearchState.chosen_dataframes.value) > 0:

                with solara.Card("Text find/replace", margin=1, elevation=1):

                    # search phrase text box
                    solara.InputText("Enter some text", value=SearchState.search_query)

                    # Replacement text
                    with solara.Tooltip(replace_txt_tooltip, color="black"):
                        if SearchState.replace_text.value:
                            solara.InputText("Replace with", value=SearchState.replacement_text)

                    # Search or find/replace buttons
                    with solara.Row():
                        if SearchState.replace_text.value:
                            solara.Button("Replace", on_click=find_replace_single_query)
                        else:
                            solara.Button("Search", on_click=find_replace_single_query)
                        solara.Button("Clear", on_click=SearchState.reset_search)

                    # find or find/replace phrases checkbox
                    with solara.Tooltip(class_label_tooltip, color="black"):
                        with solara.Row():
                            solara.Checkbox(label="Annotate matches", value=SearchState.label_matches)
                        with solara.Row():
                            if SearchState.label_matches.value:
                                solara.InputText(label="Annotation", value=SearchState.match_class_label)


                    # find or find/replace phrases checkbox
                    with solara.Tooltip(replace_tooltip, color="black"):
                        with solara.Row():
                            solara.Checkbox(label="Replace", value=SearchState.replace_text)

                    # search case-sensitive checkbox
                    with solara.Tooltip(case_sens_tooltip, color="black"):
                        with solara.Row():
                            solara.Checkbox(label="Case sensitive", value=SearchState.case_sensitive)

                    # ## New results dataset creator
                    # with solara.Tooltip(results_dataset_tooltip, color="black"):
                    #     with solara.Row():
                    #         solara.Checkbox(label="Create results dataset", value=SearchState.create_dataset)
                    #     with solara.Row():
                    #         if SearchState.create_dataset.value:
                    #             solara.InputText(label="Results dataset name", value=SearchState.results_dataset_name)
                    #     with solara.Row():
                    #         if SearchState.create_dataset.value and len(SearchState.results_dataset_name.value.strip()) <= 0:
                    #             solara.Error("You must name the new results dataset.")

def reset_view():
    '''
    Resets the dataset and columns viewed in results and general
    :return:
    '''
    SearchState.chosen_dataframes.value = []
    SearchState.search_keywords.value = None
    SearchState.chosen_columns.set([])
    SearchState.reset_search_view()

def find_replace_single_query():
    '''
    Used to search a dataset for a single search-phrase and potentially replace matching terms.
    This functions differently to the keyword list search functions.
    :return:
    '''
    query = [SearchState.search_query.value]
    case_sens = SearchState.case_sensitive.value
    search_frames = SearchState.chosen_dataframes.value
    rep_text = SearchState.replacement_text.value if SearchState.replace_text.value else None
    label_matches = SearchState.label_matches.value
    match_class = SearchState.match_class_label.value
    matched_dfs = []
    for df_name in search_frames:
        columns = SearchState.get_chosen_columns(df_name).value
        results = find_replace_data(queries=query, case_sensitive=case_sens, df_name=df_name, columns=columns, replacement_text=rep_text)
        if label_matches and len(match_class) > 0:
            results = annotate_matches(dataframe=results, queries=query, case_sensitive=case_sens, columns=columns, class_label=match_class)
        matched_dfs.append((df_name, results))
    SearchState.search_results.set(matched_dfs)


keyword_column = solara.reactive(cast(Optional[str], "-- Pick the keyword column --"))


@solara.component
def KeywordListSearchSideBar():
    chosen_dataframe = State.chosen_dataframe.value
    df = None
    # dff = None
    if chosen_dataframe is not None:
        df = State.get_dataframe(chosen_dataframe)
    dataframes = State.dataframes.value
    dataframe_names = State.dataframe_names.value
    with solara.Sidebar():
        with solara.Card("Upload lists of keywords", margin=1, elevation=1):
            with solara.Row(margin=3):
                if 0 < State.upload_progress.value < 100:
                    solara.ProgressLinear(value=State.upload_progress.value)
                else:
                    solara.ProgressLinear(False)
            with solara.Column():
                with solara.Row():
                    solara.Button("Sample dataset", color="primary", text=True, outlined=True, on_click=State.load_sample, disabled=len(dataframes) > 0)
                    solara.Button("Clear datasets", color="primary", text=True, outlined=True, on_click=State.reset, disabled=len(dataframes) <= 0)
                solara.FileDrop(on_file=SearchState.load_keywords_from_file, on_total_progress=State.upload_progress.set, label=State.path.value)

        with solara.Card("Search Datasets", margin=1, elevation=1):
            if len(dataframes) > 0:
                solara.SelectMultiple("Datasets", all_values=dataframe_names, values=SearchState.chosen_dataframes, on_value=SearchState.reset_column)
            if df is not None:
                columns = df.columns.tolist()
                solara.SelectMultiple("Column", all_values=columns, values=SearchState.chosen_columns)
                with solara.Row(margin=3):
                    solara.Button("Reset data-view", color="primary", text=True,outlined=True,on_click=reset_view)

        with solara.Card("Select search terms", margin=1, elevation=1):
            if SearchState.search_keywords.value is not None:
                with solara.Card():
                    keyword_columns = SearchState.search_keywords.value.columns.tolist()
                    solara.Select("Keyword column", values=keyword_columns, value=keyword_column)
                    def variables_chosen():
                        frames = SearchState.chosen_dataframes.value
                        cols = SearchState.chosen_columns.value
                        return (frames is not None and len(frames) > 0) and (cols is not None and len(cols) > 0)

                    with solara.Row():
                        solara.Button("Search", color="primary", text=True,outlined=True, on_click=search_keyword_list)


def search_keyword_list():
    case_sense = SearchState.case_sensitive.value
    dfs = SearchState.chosen_dataframe.value
    keywords = SearchState.search_keywords.value[keyword_column.value].to_list()
    cols = SearchState.chosen_columns.value
    matched_dfs = find_replace_data(keywords, case_sense, [dfs], replacement_text=None,columns=cols)
    SearchState.search_results.set(matched_dfs)
