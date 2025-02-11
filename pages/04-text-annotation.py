from ipyannotations.text import TextTagger
from ipydatagrid import DataGrid

from components.sidebars.span_annotation_sidebars import SpanAnnotationSidebar
from assets.state import State
from tools.span import create_span_column
from assets.annotation_state import AnnotationState
from typing import Optional, cast

import numpy as np
import solara

from tools.span import annotate_matches

column = solara.reactive(cast(Optional[str], None))
cell_indx = solara.reactive(cast(Optional[int], 0))
cell_value = solara.reactive(cast(Optional[str], ""))
cell_click = solara.reactive(cast(Optional[bool],False))


@solara.component
def Page():

    # Widget initialisation
    value, set_value = solara.use_state(None)
    data_element = None

    # Sidebar
    SpanAnnotationSidebar()

    # Flag monitors to update state when changes occur
    class_change_flag = AnnotationState.span_class_added.value
    cell_click_flag = cell_click.value

    if State.chosen_dataframe.value is not None and State.chosen_column.value is not None:
        df = State.get_dataframe(State.chosen_dataframe.value)
        chosen_column = State.chosen_column.value
        display_data = df[[chosen_column]] if chosen_column is not None else df.copy()

        with solara.Column():
            with solara.Card():
                if len(AnnotationState.span_classes.value) > 0:
                    # Get current span data
                    span_data = []
                    if chosen_column is not None and create_span_column(chosen_column) in df:
                        previous_annotations = df.loc[cell_indx.value, create_span_column(chosen_column)]
                        if isinstance(previous_annotations, list):
                            span_data = previous_annotations[0]
                    # Retrieve and/or instantiate TextTagger
                    tt = TextTagger.element(classes=AnnotationState.span_classes.value, text=str(cell_value.value), data=span_data)
                    set_value(tt)
            # Dataset table
            dg = DataGrid.element(dataframe=display_data, base_column_size=600, selection_mode="cell", editable=True)
            data_element = dg
    else:
        solara.Markdown("Please select both a dataset and column from the sidebar.")

    def update_annotator():
        if value is not None:
            text_widget = cast(TextTagger, solara.get_widget(value))
            ## Any future submit function will need to change this list size check
            if len(text_widget.submission_functions) == 0:
                # Update data callback if it is currently not added - adding it more than once means data is duplicated
                text_widget.on_submit(update_data)
            if text_widget is not None:
                # Add any new class labels
                text_widget.text_widget.classes = AnnotationState.span_classes.value
                text_widget.class_selector.options = AnnotationState.span_classes.value
                # Display the text of the current cell to annotate
                text_widget.text_widget.text = str(cell_value.value)
    # Process updates
    solara.use_effect(update_annotator, None)

    def update_widget():
        if data_element is not None:
            grid_wid = cast(DataGrid, solara.get_widget(data_element))
            if grid_wid is not None:
                # Set the data
                grid_wid.data = display_data
                if chosen_column is not None:
                    # Add cell click value callback
                    grid_wid.on_cell_click(set_cell_values)
    # Process updates
    solara.use_effect(update_widget, None)


def update_data(span_data: list):
    print(type(span_data))
    print(type(span_data[0]))
    print(type(span_data[0][0]))
    print(type(span_data[0][1]))
    if span_data is None:
        return

    col = column.value
    df_name = State.chosen_dataframe.value
    df = State.get_dataframe(df_name)

    annotate_all = AnnotationState.annotate_all.value
    # Add column if it doesn't exist
    if create_span_column(col) not in df.columns:
        df[create_span_column(col)] = None
    # Find and annotate all instances in the corpus
    if annotate_all:
        for span in span_data:
            text_span = cell_value.value[span[0]:span[1]]
            annotate_matches(df, [text_span], False, [col], span[2])
    # Annotate single instance
    else:
        if len(span_data) == 0:
            new_data = None
        else:
            current_data = df.at[cell_indx.value, create_span_column(col)]
            new_data = [span_data + current_data[0]] if current_data is not None else [span_data]
        df.at[cell_indx.value, create_span_column(col)] = new_data


def set_cell_values(cell_dict: dict):
    cell_value.set(cell_dict['cell_value'])
    cell_value.value = cell_dict['cell_value']
    cell_indx.set(cell_dict['row'])
    column.set(cell_dict['column'])
    signal_cell_click()


def signal_cell_click():
    flip = True if not cell_click.value else False
    cell_click.set(flip)
