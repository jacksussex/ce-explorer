from typing import Optional, cast
from collections import defaultdict

from solara import Reactive

from assets.state import State
from pandas import DataFrame
import solara


class SearchState(State):

    # Text edit fields
    apply_to_all = solara.reactive(cast(Optional[bool], True))
    annotate_span = solara.reactive(cast(Optional[bool], False))
    # Search fields
    search_keywords = solara.reactive(cast(Optional[DataFrame], None))
    search_results = solara.reactive(cast(Optional[list], None))

    # Search fields
    find_replace_keywords = solara.reactive(cast(Optional[str], None))
    search_query = solara.reactive(cast(Optional[str], None))
    case_sensitive = solara.reactive(cast(Optional[bool], False))
    chosen_dataframes = solara.reactive(cast(Optional[list], []))
    chosen_columns = solara.reactive(cast(Optional[list], []))

    # Results dataset name
    create_dataset = solara.reactive(cast(Optional[bool], False))
    results_dataset_name = solara.reactive(cast(Optional[str], ""))

    # Find replace fields
    replace_text = solara.reactive(cast(Optional[bool], False))
    replacement_text = solara.reactive(cast(Optional[str], None))

    # Number of datasets being searched.
    number_datasets = solara.reactive(cast(Optional[int], 1))

    #Search columns for each searching dataset
    search_columns = solara.reactive(cast(Optional[dict], {}))

    # Label matches
    label_matches = solara.reactive(cast(Optional[bool], False))
    match_class_label = solara.reactive(cast(Optional[str], ""))

    @staticmethod
    def get_chosen_columns(dataset: str) -> Reactive[list]:
        all_choices = SearchState.search_columns.value
        column_choices = None
        if dataset in all_choices:
            column_choices = all_choices[dataset]
        else:
            column_choices = solara.reactive(cast(Optional[list],[]))
            all_choices[dataset] = column_choices
        SearchState.search_columns.set(all_choices)
        return column_choices

    @staticmethod
    def load_keywords_from_file(file):
        df, frame_name = State.load_from_file(file)
        if df is not None:
            SearchState.search_keywords.set(df)

    @staticmethod
    def reset_search():
        SearchState.search_results.value = []

    @staticmethod
    def reset_search_view():
        SearchState.search_results.set([])
        SearchState.search_keywords.set(None)
