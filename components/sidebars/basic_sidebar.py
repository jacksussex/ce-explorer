from components.solara_components.data_upload import DataUpload
from components.solara_components.data_view import DataView
from tools.dataframe import *
import css.colour_scheme_classes as colours
import solara

drag_and_drop = "Drag and drop data to be upload or try out the tool with an inbuilt sample."

@solara.component
def BasicSidebar():

    solara.lab.theme.themes.light.primary = colours.SECONDARY

    chosen_dataframe = State.chosen_dataframe.value
    df = None
    if chosen_dataframe is not None:
        df = State.get_dataframe(chosen_dataframe)

    with solara.Sidebar():

            ## Upload data component
            DataUpload()

            ## Choose what to view
            DataView(df, multiselect=True)




