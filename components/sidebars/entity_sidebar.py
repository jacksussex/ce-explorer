from typing import cast, Optional

import solara

from assets.entity_state import EntityState
from components.solara_components.data_upload import DataUpload
from components.solara_components.data_view import DataView
from tools.parse import endpoint
from components.views.entity import ExtractEntities
from tools.parse import *
from tools.web import ping_website

common_entity_name = solara.reactive(cast(Optional[list],None))

entity_fishing_tooltip = "Perform entity fishing for wiki-data annotations when parsing"

wiki_service_down = solara.reactive(cast(Optional[bool], False))
wiki_service_down_error = "It appears the service used to retrieve wiki-data is currently unavailable. The parsing will continue without it."

def EntityExtractSidebar():

    df = None
    if State.chosen_dataframe.value is not None:
        df = State.get_dataframe(State.chosen_dataframe.value)

    with solara.Sidebar():

        # Upload data component
        DataUpload()

        dataframe_names = State.dataframe_names.value
        with solara.Card("Dataset", margin=1, elevation=1):
            if len(dataframe_names) > 0:
                solara.Select("Dataset", values=dataframe_names, value=State.chosen_dataframe,
                              on_value=State.reset_column)
            if df is not None:
                # df = dataframes[dataframe_names.index(chosen_dataframe)]
                columns = df.columns.tolist()
                solara.Select("Column", values=columns, value=State.chosen_column)
                with solara.Row(margin=3):
                    solara.Button("Reset data-view", color="primary", text=True, outlined=True,
                                  on_click=State.reset_view)
                    solara.Button("Extract entities", color="primary", text=True, outlined=True,
                                  on_click=parse_column, disabled=State.chosen_dataframe.value is None)
                with solara.Tooltip(entity_fishing_tooltip):
                    with solara.Row(margin=3):
                        solara.Checkbox(label="Entity fishing", value=EntityState.get_wiki_data)
            if wiki_service_down.value:
                solara.Error(wiki_service_down_error)
            ExtractEntities()
            if parse_data.finished:
                solara.Info("Entities ready to view!")


def CommonEntitiesSidebar():
    with solara.Sidebar():
        if EntityState.common_entities is not None and len(EntityState.common_entities) > 0:
            with solara.Card("Entity breakdown"):
                entity_types = list(EntityState.common_entities.keys())
                solara.Select(label="Entity type", values=entity_types,value=EntityState.chosen_entity_type)


def parse_column():
    get_wiki_data = EntityState.get_wiki_data.value
    ## Check if the service is down before attempting so the parser doesn't hang
    if get_wiki_data:
        get_wiki_data = ping_website(endpoint)
        if not get_wiki_data:
            wiki_service_down.set(True)
            EntityState.get_wiki_data.set(False)
        else:
            wiki_service_down.set(False)
    parse_data(State.chosen_column.value, get_wiki_data)