from assets.state import State
import solara
from typing import cast,Optional


class DatasetBuilderState(State):

    # upload fields
    dataset_name = solara.reactive("")
    rename_column = solara.reactive("")
    new_column_name = solara.reactive("")

    # builder fields
    chosen_columns = solara.reactive(cast(Optional[list], []))
    new_data_subset_name = solara.reactive("")
    custom_colour = solara.reactive(State.default_colour)

    # combination fields
    combination_datasets = solara.reactive(cast(Optional[list], []))
    discard_old = solara.reactive(cast(Optional[bool], False))
    combined_data_name = solara.reactive("")
    custom_combined_colour = solara.reactive("")
    key_column = solara.reactive(cast(Optional[str], None))

    # remove dataset fields
    discard_datasets = solara.reactive(cast(Optional[list], []))

    update_flag = solara.reactive(cast(Optional[bool], True))

    @staticmethod
    def signal():
        curr_val = DatasetBuilderState.update_flag.value
        new_val = False if curr_val else True
        DatasetBuilderState.update_flag.set(new_val)
