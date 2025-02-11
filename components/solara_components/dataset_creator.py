from typing import cast, Optional

import solara

from assets.state import State

import reacton.ipywidgets as w

search_result_dataset_name = solara.reactive(cast(Optional[str],None))
custom_colour = solara.reactive(cast(Optional[str],State.default_colour))

@solara.component
def DatasetCreator(df):
    def update_custom_dataset_colour(colour_val):
        custom_colour.set(colour_val)
    def add_dataset():
        State.add_dataset(df, search_result_dataset_name.value, custom_colour.value)

    with solara.Card("Create new dataset"):
        with solara.Row():
            solara.InputText(label="New dataset name", value=search_result_dataset_name)
        with solara.Row():
            colourPicker = w.ColorPicker(
                concise=False,
                description='Pick a color',
                disabled=False,
                on_value=update_custom_dataset_colour,
                value=custom_colour.value
            )
        with solara.Row():
            solara.Button(label="Create", on_click=add_dataset)


