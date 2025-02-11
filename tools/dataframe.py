from assets.state import State
from functools import reduce
import pandas as pd

def get_corpus_subset(column, row_index):
    dataframe_names = State.dataframe_names.value
    chosen_dataframe = State.chosen_dataframe.value
    dataframes = State.dataframes.value
    dataframe = dataframes[dataframe_names.index(chosen_dataframe)]
    entity = dataframe.iloc[row_index]['Entity']
    entity_index = State.entity_index
    index = entity_index[entity]

def combine_columns(dataframe, columns, output_col):
    print(columns)
    dataframe[output_col] = ""
    # dataframe[output_col] = [dataframe[output_col] + dataframe[column] for column in columns.value if column in dataframe.columns]
    dataframe[output_col] = dataframe[columns].agg(create_join_strings, axis=1)
    return dataframe

def create_join_strings(list_of_obs, delimiter=' '):
    list_of_obs = [str(x) for x in list_of_obs if type(x) is not float]
    return delimiter.join(list_of_obs)


def concatenate_frames(datasets, combine_key=None):
    if combine_key is None:
        return pd.concat(datasets)
    else:
        return reduce(lambda x,y: pd.merge(x,y, on=combine_key, how='outer'), datasets)

