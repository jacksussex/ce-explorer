from enum import Enum
from typing import cast, Optional

import solara
import solara.lab
from ipydatagrid import DataGrid

from assets.search_state import SearchState
from components.sidebars.search_sidebar import FindReplaceSidebar, KeywordListSearchSideBar
from components.solara_components.dataset_creator import DatasetCreator
from tools.text import *


class SidebarType(Enum):
    FIND_REPLACE = 0
    KEYWORD_LIST = 1


sidebar_type = solara.reactive(cast(Optional[SidebarType], SidebarType.FIND_REPLACE))


@solara.component
def Page():

    search_results = None
    df = None
    if SearchState.search_results.value is not None and len(SearchState.search_results.value) > 0:
        search_results = SearchState.search_results.value

    if State.chosen_dataframe.value is not None:
        df = State.get_dataframe(State.chosen_dataframe.value)

    if sidebar_type.value == SidebarType.FIND_REPLACE:
        FindReplaceSidebar()
    elif sidebar_type.value == SidebarType.KEYWORD_LIST:
        KeywordListSearchSideBar()

    if search_results is not None:
        with solara.lab.Tabs(on_value=change_sidebar):
            with solara.lab.Tab("Find replace"):
                with solara.Row():
                    solara.Markdown("Search datasets")
                with solara.Column():
                    ## Iterate over each search outcome -> create a datagrid for each one and present -> provide option to save and colour pick as new dataset
                    # if df is not None:
                    columns = SearchState.chosen_columns.value
                    dff = df[columns] if len(columns) > 0  else df
                    find_rep_df = DataGrid.element(dataframe=dff,
                                               selection_mode="cell", editable=False, auto_fit_columns=True)

                if search_results is not None:
                    with solara.Row():
                        solara.Markdown("Search results")
                    with solara.Row():
                        for results_set in search_results:
                            with solara.Columns([2,1]):
                                with solara.Column():
                                    solara.Markdown(results_set[0])
                                    results = results_set[1]
                                    columns = SearchState.get_chosen_columns(results_set[0]).value
                                    filter_df = results[columns] if columns else results.copy()
                                    solara.DataFrame(filter_df, items_per_page=20)

                                with solara.Column():
                                    DatasetCreator(results_set[1])


                    def update_rp_df():
                        try:
                            datagrid_widget = cast(DataGrid, solara.get_widget(find_rep_df))
                            datagrid_widget.data = df
                        except:
                            print("")

                    solara.use_effect(update_rp_df, None)

            with solara.lab.Tab("Keyword list search"):
                # with solara.Column():
                if df is not None:
                    keyword_list_df = DataGrid.element(dataframe=df,
                                               selection_mode="cell", editable=False, auto_fit_columns=True)

                    def update_kw_df():
                        try:
                            datagrid_widget = cast(DataGrid, solara.get_widget(keyword_list_df))
                            datagrid_widget.data = df
                        except :
                            print("")

                    solara.use_effect(update_kw_df, None)


def change_sidebar(signal):
    new_sidebar = SidebarType(signal)
    sidebar_type.set(new_sidebar)

