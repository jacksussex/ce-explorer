import re

from pandas import DataFrame


# common class label for text search
_keyword_search = "keyword"


def get_datagrid_span(datagrid_span):
    row = datagrid_span['r']
    column = datagrid_span['c']
    return [row,column]


def create_span_column(column : str):
    return column + "_" + "span_annotations"


def annotate_matches(dataframe: DataFrame, queries: list, case_sensitive: bool, columns: list=None, class_label: str=_keyword_search) -> DataFrame:
    # results_df = dataframe[columns] if columns else dataframe
    columns = columns if columns else dataframe.columns.to_list()
    pattern = create_re_group(queries)
    flags = re.IGNORECASE if not case_sensitive else None
    for column in columns:
        span_column = create_span_column(column)
        if span_column in dataframe.columns:
            # dataframe[span_column] = dataframe[span_column] + dataframe[column].astype(str).apply(lambda text: search_and_annotate(text=text, pattern=pattern, class_label=class_label,flags=flags))
            dataframe[span_column] = dataframe[column].astype(str).apply(lambda text: [search_and_annotate(text=text, pattern=pattern, class_label=class_label,flags=flags)])
        else:
            dataframe[span_column] = dataframe[column].astype(str).apply(lambda text: [search_and_annotate(text=text, pattern=pattern, class_label=class_label,flags=flags)])
    return dataframe


def create_annotation_column(column: str, class_label: str) -> str:
    return class_label + "_" + column


def search_and_annotate(text: str, pattern: str, class_label: str, flags: int=None) -> list:
    # span_list = [create_span(x.start(), x.end(), class_label) for x in re.finditer(pattern, text, flags)]
    return [create_span(x.start(), x.end(), class_label) for x in re.finditer(pattern, text, flags)]


def remove_annotations(span_annotations: list, class_label: str) -> list:
    edited_annotations = None
    if span_annotations is not None:
        edited_annotations = [x for x in span_annotations if not span_is_class(x, class_label)]
    return edited_annotations


def span_is_class(span_annotation: tuple, class_label: str) -> bool:
    return span_annotation[1] == class_label


def create_re_group(queries:list) -> str:
    return r"("+'|'.join(queries)+r")"


def create_span(start: int, end: int, label:  str=_keyword_search) -> tuple:
    return (start, end, label)
