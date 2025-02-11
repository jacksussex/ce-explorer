from assets.dataset_builder_state import DatasetBuilderState
from components.solara_components.data_upload import DataUpload
from components.solara_components.data_view import DataView
from tools.dataframe import *
import reacton.ipywidgets as w
import solara

rename_dataset_tooltip = "Rename the chosen dataset and select a custom colour"
rename_column_tooltip = "Rename specific columns in the chosen dataset"
# rename_column_tooltip

@solara.component
def UploadSidebar():

    chosen_dataframe = DatasetBuilderState.chosen_dataframe.value
    flag = DatasetBuilderState.update_flag.value
    # current_colour = DatasetBuilderState.custom_colour.value

    df = None
    if chosen_dataframe is not None:
        df = State.get_dataframe(chosen_dataframe)
        # current_colour = State.colour_mapping.value[chosen_dataframe]
    # dataframes = State.dataframes.value
    # dataframe_names = State.dataframe_names.value

    with solara.Sidebar():

        ## Upload data component
        DataUpload()

        ## Choose what to view
        DataView(df, multiselect=True)

        # with solara.Card("Data view", margin=1, elevation=1):
        #     if len(dataframes) > 0:
        #         solara.Select("Dataset", values=dataframe_names, value=State.chosen_dataframe, on_value=State.reset_column)
        #     if df is not None:
        #         columns = df.columns.tolist()
        #         solara.Select("Column", values=columns, value=State.chosen_column)
        #         with solara.Row(margin=3):
        #             solara.Button("Reset data-view", color="primary", text=True,outlined=True,on_click=State.reset_view)

        with solara.Tooltip(rename_dataset_tooltip):
            with solara.Card("Configure dataset", margin=1, elevation=1):
                if chosen_dataframe is not None:
                    # Change name
                    solara.Markdown(chosen_dataframe)
                    with solara.Row():
                        solara.InputText("Rename dataset", value=DatasetBuilderState.dataset_name)
                    with solara.Row():
                        colourPicker = w.ColorPicker(
                                concise=False,
                                description='Pick a color',
                                disabled=False,
                                on_value=update_custom_dataset_colour,
                                value=DatasetBuilderState.custom_colour.value
                            )
                    with solara.Row():
                        solara.Button("Update dataset", on_click=update_dataset)

        with solara.Tooltip(rename_column_tooltip):
            with solara.Card("Rename columns", margin=1, elevation=1):
                if df is not None:
                    solara.Select("Column", values=df.columns.tolist(), value=DatasetBuilderState.rename_column)
                    solara.InputText("New name", value=DatasetBuilderState.new_column_name)
                    with solara.Row():
                        solara.Button("Update columns", on_click=update_column)

def CreateDatasetSidebar():

    chosen_dataframe = State.chosen_dataframe.value

    df = None
    current_colour = None
    if chosen_dataframe is not None:
        df = State.get_dataframe(chosen_dataframe)
        current_colour = State.colour_mapping.value[chosen_dataframe]

    dataframes = State.dataframes.value
    dataframe_names = State.dataframe_names.value

    with solara.Sidebar():
        with solara.Card("Create data subset", margin=1, elevation=1):
            if len(dataframes) > 0:
                solara.Select("Dataset", values=dataframe_names, value=State.chosen_dataframe, on_value=State.reset_column)
                if df is not None:
                    with solara.Row():
                        solara.InputText("Name dataset", value=DatasetBuilderState.new_data_subset_name)
                    with solara.Row():
                        colourPicker2 = w.ColorPicker(
                            concise=False,
                            description='Pick a color',
                            disabled=False,
                            on_value=update_custom_dataset_colour,
                            value=current_colour if current_colour is not None else State.default_colour
                        )
                    with solara.Row():
                        solara.SelectMultiple("Columns", all_values=df.columns.to_list(), values=State.chosen_columns)
                    with solara.Row():
                        solara.Button("Create subset", on_click=create_subset)

        with solara.Card("Combine datasets", margin=1, elevation=1):
            solara.SelectMultiple("Datasets to combine", all_values=State.dataframe_names.value, values=DatasetBuilderState.combination_datasets)
            with solara.Row():
                matched_columns = get_common_rows()
                if len(matched_columns) <= 0:
                    solara.Warning("There are no matching columns between the chosen datasets. Combining them now will only concatenate them.")
                else:
                    solara.Select("Combination key", values=matched_columns, value=DatasetBuilderState.key_column)
            solara.InputText("Dataset name", value=DatasetBuilderState.combined_data_name)
            with solara.Row():
                colourPicker3 = w.ColorPicker(
                    concise=False,
                    description='Pick a color',
                    disabled=False,
                    on_value=update_combined_dataset_colour,
                    value=State.default_colour
                )
            # with solara.Row():
            #     solara.Checkbox(label="Discard combined datasets", value=DatasetBuilderState.discard_old)
            with solara.Row():
                solara.Button("Combine", on_click=combine_datasets)


def get_common_rows():
    columns = [set(x.columns.to_list()) for x in [State.get_dataframe(y) for y in DatasetBuilderState.combination_datasets.value]]
    if columns is not None and len(columns) > 0:
        columns = list(set.intersection(*columns))
    else:
        columns = []
    return columns


def combine_datasets():
    colour = DatasetBuilderState.custom_combined_colour
    name = DatasetBuilderState.combined_data_name.value
    datasets = [State.get_dataframe(x) for x in DatasetBuilderState.combination_datasets.value]
    combine_key = DatasetBuilderState.key_column.value
    State.add_dataset(concatenate_frames(datasets, combine_key), name, colour)
    if DatasetBuilderState.discard_old.value:
        for dataset in DatasetBuilderState.combination_datasets.value:
            State.remove_dataset(dataset)


def update_dataset():
    new_name = DatasetBuilderState.dataset_name.value
    current_name = State.chosen_dataframe.value
    if new_name in State.dataframe_names.value:
        solara.Error("This name already exists in the collection of data names.")
    elif (new_name is not None and len(new_name) > 0) and current_name is not None:
        upate_colour_mapping(current_name, new_name)
        State.dataframe_names.value[State.dataframe_names.value.index(current_name)] = new_name
        State.chosen_dataframe.value = new_name
    change_dataset_colour(DatasetBuilderState.custom_colour.value)
    DatasetBuilderState.dataset_name.set("")
    DatasetBuilderState.signal()

def upate_colour_mapping(old_data_name, new_data_name):
    colour_mapping = State.colour_mapping.value
    if old_data_name in colour_mapping:
        colour_mapping[new_data_name] = colour_mapping.pop(old_data_name)
    State.colour_mapping.set(colour_mapping)


def update_custom_colour(colour_val):
    DatasetBuilderState.custom_colour.set(colour_val)


def change_dataset_colour(colour_val):
    dataframe = State.chosen_dataframe.value
    colour_mapping = State.colour_mapping.value
    colour_mapping[dataframe] = colour_val
    State.colour_mapping.set(colour_mapping)


def update_custom_dataset_colour(colour_val):
    DatasetBuilderState.custom_colour.set(colour_val)


def update_combined_dataset_colour(colour_val):
    DatasetBuilderState.custom_combined_colour.set(colour_val)


def update_column():
    new_column = DatasetBuilderState.new_column_name.value
    current_column = DatasetBuilderState.rename_column.value
    dataframe = State.get_dataframe(State.chosen_dataframe.value)
    if new_column in dataframe:
        solara.Error("A column with this namer already exists in the current dataframe")
    elif (new_column is not None and len(new_column) > 0) and current_column is not None:
        dataframe.rename(columns={current_column : new_column}, inplace=True)
        solara.Info("Column name updated")
        if current_column in State.chosen_columns.value:
            columns = State.chosen_columns.value
            columns.remove(current_column)
            columns.append(new_column)
            State.chosen_columns.set(columns)
    DatasetBuilderState.new_column_name.set(None)
    DatasetBuilderState.rename_column.set(None)
    DatasetBuilderState.signal()


def create_subset():
    if State.chosen_dataframe.value is not None:
        df = State.get_dataframe(State.chosen_dataframe.value)
        name = DatasetBuilderState.new_data_subset_name.value
        colour = DatasetBuilderState.custom_colour.value
        columns = State.chosen_columns.value
        if name is not None:
            if name not in State.dataframe_names.value:
                if len(columns) > 0:
                    State.add_dataset(df[columns], name, colour)
            else:
                solara.Error("A dataset with this name is already present in the collection.")

