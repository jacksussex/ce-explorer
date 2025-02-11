import logging
from enum import Enum

from assets.annotation_state import AnnotationState
from assets.dataset_builder_state import DatasetBuilderState

from ipydatagrid import DataGrid
from typing import cast

from assets.state import State
from components.sidebars.dataset_builder_sidebar import UploadSidebar, CreateDatasetSidebar
from components.sidebars.annotation_sidebar import AnnotationSideBar

import solara
import pickle


class SidebarType(Enum):
    UPLOAD = 0
    CREATE = 1
    PREFIXSUFFIX = 2


@solara.component
def Page():

    chosen_dataframe = DatasetBuilderState.chosen_dataframe.value
    # chosen_column = DatasetBuilderState.chosen_column.value

    # forces a page re-load
    DatasetBuilderState.update_flag.value

    df = None
    df1 = None
    df2 = None
    df3 = None
    datagrid = None
    datagrid2 = None
    datagrid3 = None

    side_bar_type, set_type = solara.use_state(SidebarType.UPLOAD)

    def change_sidebar(signal):
        new_sidebar = SidebarType(signal)
        set_type(new_sidebar)

    if chosen_dataframe is not None:
        df = DatasetBuilderState.get_dataframe(chosen_dataframe)
        colours = DatasetBuilderState.colour_mapping.value
        df_colour = colours[chosen_dataframe]
        solara.Markdown(md_text=chosen_dataframe, style={"color": "white", "background-color": df_colour})

    with solara.lab.Tabs(on_value=change_sidebar):
        with solara.lab.Tab("Upload data"):

            if side_bar_type == SidebarType.UPLOAD:
                UploadSidebar()
            if side_bar_type == SidebarType.CREATE:
                CreateDatasetSidebar()
            if side_bar_type == SidebarType.PREFIXSUFFIX:
                AnnotationSideBar()

            if df is not None:
                chosen_columns = State.chosen_columns.value
                if len(chosen_columns) > 0:
                    df1 = df[chosen_columns]
                    dg = DataGrid.element(dataframe=df1, selection_mode="cell",
                                                base_column_size=500, auto_fit_columns=True, vertical_stripes=True)
                    datagrid = dg

                    def pickle_data():
                        return pickle.dumps(df1)

                    with solara.Row(margin=3):
                        # solara.FileDownload(get_data, label=f"Download {len(dff):,} csv", filename="selected.csv")
                        solara.FileDownload(pickle_data(), label=f"Download {len(df1):,} data", filename="selected.p")
        def update_df():
            if datagrid is not None and df1 is not None:
                datagrid_widget = cast(DataGrid, solara.get_widget(datagrid))
                datagrid_widget.data = df1
        solara.use_effect(update_df, None)

        with solara.lab.Tab("Create dataset", disabled=df is None):

            if df is not None:
                columns = State.chosen_columns.value
                if len(columns) > 0:
                    df2 = df[columns]
                    dg2 = DataGrid.element(dataframe=df2, selection_mode="cell", editable=False, base_column_size=500)
                    datagrid2 = dg2

            def update_df2():
                if df2 is not None and datagrid2 is not None:
                    datagrid_widget2 = cast(DataGrid, solara.get_widget(datagrid2))
                    datagrid_widget2.data = df2
            solara.use_effect(update_df2, None)

            if df2 is not None:
                # def get_data():
                #     return dff.to_csv(index=False)

                def pickle_data():
                    return pickle.dumps(df2)

                with solara.Row(margin=3):
                    # solara.FileDownload(get_data, label=f"Download {len(dff):,} csv", filename="selected.csv")
                    solara.FileDownload(pickle_data(), label=f"Download {len(df2):,} data", filename="selected.p")

        with solara.lab.Tab("Add prefix and suffixes"):
            if AnnotationState.annotated_df.value:
                logging.info(msg="data annotated")

            if df is not None:
                column = DatasetBuilderState.chosen_column.value
                df3 = df[[column]] if column else df.copy()
                dg3 = DataGrid.element(dataframe=df3, selection_mode="cell", editable=False, base_column_size=500)
                datagrid3 = dg3
            else:
                solara.Info("Please choose a dataset to work with using the sidebar")

            def update_df3():
                if df3 is not None and datagrid3 is not None:
                    datagrid_widget3 = cast(DataGrid, solara.get_widget(datagrid3))
                    datagrid_widget3.data = df3

            solara.use_effect(update_df3, None)






