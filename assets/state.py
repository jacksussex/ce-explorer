from typing import Optional, cast

import logging

import pandas
import pandas as pd
import pickle
import solara
from pandas import DataFrame

try:
    df_sample = pd.read_csv("data/example_data/nms_science_and_technology_sample.csv")
except:
    df_sample = pd.DataFrame()
    logging.error("Example data file not found.")


class State:

    default_colour = '#000000'

    # The colour mapping between dataset_names
    colour_mapping = solara.reactive(cast(Optional[dict], {}))

    # General data fields
    dataframes = solara.reactive(cast(Optional[list], []))
    dataframe_names = solara.reactive(cast(Optional[list], []))
    chosen_dataframe = solara.reactive(cast(Optional[str], None))
    chosen_dataframes = solara.reactive(cast(Optional[list], []))
    chosen_column = solara.reactive(cast(Optional[str], None))
    chosen_columns = solara.reactive(cast(Optional[list], []))
    # Annotation fields
    column_choices = solara.reactive(cast(Optional[list], None))

    data = solara.reactive(cast(Optional[list],None))

    # Data upload fields
    drag_placeholder = "Drag file here"
    sample_name = "sample"
    path = solara.reactive(cast(Optional[str], drag_placeholder))
    upload_progress = solara.reactive(cast(Optional[int], 0))

    global_error = solara.reactive(cast(Optional[str], None))

    @staticmethod
    def load_sample():
        State.colour_mapping.value[State.sample_name] = State.default_colour
        State.dataframe_names.value = [State.sample_name]
        State.dataframes.value = [df_sample]
        State.chosen_dataframe.value = State.sample_name


    @staticmethod
    def load_from_file(file):
        # State.error.value = None
        df = None
        frame_name = None
        if file['name'].endswith('csv'):
            df = pd.read_csv(file["file_obj"])
            frame_name = file["name"].replace('.csv', '')
        elif file['name'].endswith('.p'):
            df = pickle.load(file['file_obj'])
            frame_name = file["name"].replace('.p', '')
        else:
            solara.Error("The uploading file-type needs to be csv or pickle .p")
        return df, frame_name

    @staticmethod
    def load_data_from_file(file):
        df, frame_name = State.load_from_file(file)
        if df is not None:
            State.colour_mapping.value[frame_name] = State.default_colour
            if State.dataframe_names is not None:
                names = State.dataframe_names.value
                names.append(frame_name)
                State.dataframe_names.value = names
            else:
                State.dataframe_names.value = [frame_name]
            if State.dataframes.value is not None:
                dfs = State.dataframes.value
                dfs.append(df)
                State.dataframes.value = dfs
            else:
                State.dataframes.value = [df]
            State.chosen_dataframe.value = frame_name
            State.path.value = State.drag_placeholder

    @staticmethod
    def reset():
        State.chosen_dataframe.value = None
        State.dataframes.value = []
        State.dataframe_names.value = []
        State.path.value = State.drag_placeholder

    @staticmethod
    def reset_column(dataframe):
        State.chosen_columns.value = []

    @staticmethod
    def get_dataframe(chosen_dataframe: str) -> DataFrame:
        dataframes = State.dataframes.value
        dataframe_names = State.dataframe_names.value
        try:
            output_df = dataframes[dataframe_names.index(chosen_dataframe)]
        except ValueError:
            output_df = pandas.DataFrame()
            State.global_error.set("Dataframe name: {} not found in list of known dataframes".format(chosen_dataframe))
        return output_df

    @staticmethod
    def set_dataframe(column: str, dataframe: DataFrame):
        dataframes = State.dataframes.value
        dataframe_names = State.dataframe_names.value
        index = dataframe_names.index(column)
        dataframes[index] = dataframe
        State.dataframes.set(dataframes)

    @staticmethod
    def reset_view():
        State.chosen_column.set(None)

    @staticmethod
    def add_dataset(dataframe: DataFrame, name: str, colour: str):
        State.dataframe_names.value.append(name)
        State.colour_mapping.value[name] = colour
        State.dataframes.value.append(dataframe)
        State.chosen_dataframe.set(name)

    @staticmethod
    def remove_dataset(name: str):
        State.dataframe_names.value.remove(name)
        State.colour_mapping.value.pop(name)
        State.dataframes.value.remove(State.get_dataframe(name))

    @staticmethod
    def get_dataset_columns(dataset_name: str) -> list:
        dataset = State.get_dataframe(dataset_name)
        columns = dataset.columns.to_list() if dataset is not None else []
        return columns
