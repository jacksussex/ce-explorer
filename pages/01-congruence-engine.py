from ipydatagrid import DataGrid

from css.themes import apply_theme
from assets.state import *
from tools.dataframe import *
from components.sidebars.basic_sidebar import BasicSidebar

import solara
# from solara.lab import theme as theme
# import solara.lab



@solara.component
def Page():

    apply_theme()

    chosen_dataframe = State.chosen_dataframe.value
    df = None
    dff = None
    if chosen_dataframe is not None:
        df = State.get_dataframe(chosen_dataframe)

    datagrid = None

    BasicSidebar()

    if df is not None:

        solara.Markdown(
            f"""
            ## Data viewer
            
            View the chosen dataset and columns

        """
        )
        columns = State.chosen_columns.value
        dff = None
        if len(columns) > 0:
            dff = df[columns]
        with solara.VBox():
            if dff is not None:
                datagrid = DataGrid.element(dataframe=dff, selection_mode="cell", editable=False, base_column_size=200)
                def get_data():
                    return dff.to_csv(index=False)
                def pickle_data():
                    return pickle.dumps(dff)
                with solara.Row(margin=3):
                    solara.FileDownload(get_data, label=f"Download {len(dff):,} csv", filename="selected.csv")
                    solara.FileDownload(pickle_data(), label=f"Download {len(dff):,} data", filename="selected.p")

    def update_df():
        if datagrid is not None:
            datagrid_widget = cast(DataGrid, solara.get_widget(datagrid))
            datagrid_widget.data = dff

    solara.use_effect(update_df, None)
