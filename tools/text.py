from pandas import DataFrame, Series
import pandas as pd
from assets.state import State
import numpy as np
import fields,re

# Used to discover fuzzy matches in text
# When needing exact matching use the spacy wrapper
# def fuzzy_match_text(text, match_strings, sim_threshold=0.9):


def text_contains(dataframe: DataFrame, queries: list, case_sensitive:bool=False, column_subset:list=None, replacement_text:str=None) -> DataFrame:
    columns = column_subset if column_subset else dataframe.columns.to_list()
    results = [dataframe[column].astype(str).str.contains(regex_queries(queries), na=False, case=case_sensitive, regex=True) for column in columns]
    mask = np.column_stack(results)
    results_df = dataframe.loc[mask.any(axis=1)]
    return results_df[columns]


def regex_queries(queries:list) -> str:
    return "|".join(queries)

# def regex_queries_group(queries, name=_keyword_search):
#     return r'(?P<' + name + '>' + regex_queries(queries) + ")"


def replace_text(dataframe: DataFrame, query: str, case_sensitive: bool=False, column_subset: list=None, replacement_text: str=None) -> DataFrame:
    query = query if case_sensitive else '(?i)' + query
    if column_subset:
        dataframe = dataframe[column_subset].replace(query, replacement_text, regex=True,inplace=False)
    else:
        dataframe = dataframe.replace(query, replacement_text, regex=True, inplace=False)
    return dataframe


def replace_rows(original_df: DataFrame, replacement_df: DataFrame, columns: list=None) -> DataFrame:
    print(original_df.index.to_list())
    print(replacement_df.index.to_list())
    print(replacement_df['description'])
    if columns:
        dataframe = original_df.loc[original_df.isin(replacement_df), columns] = replacement_df[columns]
    else:
        dataframe = dataframe.loc[replacement_df.index] = replacement_df
    return dataframe

# def search_corpora(column: str, row_index: int):
#     entity_df = State.entity_dataframe
#     entity = entity_df[column][row_index]
#     State.search_query.value = entity
#     find_replace_query()


# def find_replace_query():
#     query = State.search_query.value.strip()
#     find_replace_data([query])


def find_replace_data(queries, case_sensitive, df_name, replacement_text=None, columns=None):
    # case_sensitive = State.case_sensitive.value
    # use_regex = State.use_regex.value
    # df_names = State.dataframe_names.value
    # replacement_text = None
    # if replacement_text is not None:
    #     replacement_text = State.replacement_text.value
    # num_dfs = len(df_names)
    # for i in range(0, num_dfs):
    # df_name = df_names[i]
    dataframe = State.get_dataframe(df_name)
    matched_df = text_contains(dataframe, queries, case_sensitive, column_subset=columns)
    # replace the text in the search results
    # replace the core dataframe and results dataframe with the outputs
    if replacement_text is not None:
        replacement_df = replace_text(query=queries[0],dataframe=matched_df, case_sensitive=case_sensitive, column_subset=columns, replacement_text=replacement_text)
        dataframe = replace_rows(dataframe, replacement_df)
        matched_df = replace_rows(matched_df, replacement_df)
        State.dataframes.value[State.dataframe_names.value.index(df_name)] = dataframe
    # matched_dfs.append([df_name,matched_df])
    # State.search_results.value = matched_dfs
    # State.set_search_view()
    return matched_df


### Cleaning functions
def remove_links(text: str) -> str:
    clean_txt = re.sub(r'http\S+', '', text)
    return re.sub(r'www.\S+', '', clean_txt)


def remove_mentions(text: str) -> str:
    return re.sub("@[a-zA-Z0-9_]+", r'', text)


def remove_hashtags(text: str) -> str:
    return text.replace("#", '')


def concatenate_column_prefix(dataframe: DataFrame, column: str, prefix: str, delimiter: str="_", keep_original: bool=False) -> DataFrame:
    if keep_original:
        dataframe[create_original_column_name(column)] = dataframe[column]
    dataframe[column] = dataframe[column].apply(lambda x: add_prefix(x,prefix,delimiter))
    return dataframe


def concatenate_column_suffix(dataframe: DataFrame, column: str, suffix: str, delimiter: str="_", keep_original: bool=False) -> DataFrame:
    if keep_original:
        dataframe[create_original_column_name(column)] = dataframe[column]
    dataframe[column] = dataframe[column].apply(lambda x: add_suffix(x,suffix,delimiter))
    return dataframe


def create_original_column_name(column_name: str, suffix: str="_original") -> str:
    return column_name + suffix


def add_prefix(text: str, prefix: str, delimiter: str="_") -> str:
    new_str = None
    if text is not None:
        new_str = str(prefix) + str(delimiter) + str(text)
    return new_str


def add_suffix(text: str, suffix: str, delimiter: str="_") -> str:
    new_str = None
    if text is not None:
        new_str = str(text) + str(delimiter) + str(suffix)
    return new_str


def clean_text(text: str) -> str:
    clean_txt = remove_links(text)
    clean_txt = remove_mentions(clean_txt)
    clean_txt = remove_hashtags(clean_txt)
    return clean_txt.strip()


def clean_docs(dataframe: DataFrame, doc_col: str) -> DataFrame:
    dataframe[fields._cleaned_text] = dataframe[doc_col].apply(lambda x: clean_text(x))
    return dataframe

