from typing import Optional, cast
from assets.search_state import SearchState

import solara
import numpy as np


dataset_picker_tooltip = "Pick which datasets and columns to search within."
new_dataset = solara.reactive(cast(Optional[str], None))


def DatasetPicker():

    # The number of dataset objects to produce
    all_datasets = SearchState.dataframe_names.value
    chosen_datasets = SearchState.chosen_dataframes.value
    other_available_dataframes = np.setdiff1d(all_datasets, chosen_datasets).tolist()

    with solara.Tooltip(dataset_picker_tooltip, color="black"):
        with solara.Card("Search datasets"):

            # enumerate currently chosen datasets and columns
            for index, dataset in enumerate(chosen_datasets):
                with solara.Row():
                    solara.Markdown(dataset)
                with solara.Row():
                    columns = SearchState.get_dataset_columns(dataset)
                    current_columns = SearchState.search_columns.value[dataset]
                    solara.SelectMultiple(label="Columns to search", values=current_columns, all_values=columns)
                with solara.Row():
                    solara.Button(label="Remove dataset", on_click=remove_dataset)

            ## Add a new dataset to search
            with solara.Row():
                solara.Select(label="Add dataset", values=other_available_dataframes, value=new_dataset)
            with solara.Row():
                if new_dataset.value is not None:
                    all_columns = SearchState.get_dataset_columns(new_dataset.value)
                    current_columns = SearchState.get_chosen_columns(new_dataset.value)
                    solara.SelectMultiple(label="Columns to search", values=current_columns, all_values=all_columns)
                    with solara.Row():
                        solara.Button(label="Add dataset", on_click=add_dataset)


def add_dataset():
    chosen_dataframes = SearchState.chosen_dataframes.value
    chosen_dataframes.append(new_dataset.value)
    SearchState.chosen_dataframes.set(chosen_dataframes)
    new_dataset.set(None)

def remove_dataset():
    return





