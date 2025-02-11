from typing import cast, Optional

import solara

from tools.span import *

from assets.annotation_state import AnnotationState

annotate_all_tooltip = "Annotate all matching spans in the chosen column with the selected class label"
annotation_class_tooltips = "Add annotation class labels"
annotation_review_tooltip = "Review annotation class labels"
annotation_review_remove_data_tooltip = "Remove the class labels from the entire dataset"
include_keyword_classes = "Include keyword and search classes"

current_class = solara.reactive(cast(Optional[str], ""))


@solara.component
def AnnotationClasses():
    with solara.Card(title="Annotation classes"):
        with solara.Tooltip(annotation_class_tooltips):
            solara.Markdown(", ".join(AnnotationState.span_classes.value))
            with solara.Row():
                solara.InputText(label="Span labels", value=current_class)
            with solara.Row():
                solara.Button("Submit label", on_click=add_class)


@solara.component
def AnnotationReview():
    with solara.Card(title="Annotation review"):
        with solara.Tooltip(annotation_review_tooltip):
            solara.Select(label="Class label", values=AnnotationState.span_classes.value, value=AnnotationState.removal_class)
            with solara.Tooltip(annotation_review_remove_data_tooltip):
                solara.Checkbox(label="Remove from dataset", value=AnnotationState.remove_from_dataset)
            with solara.Row():
                solara.Button(label="Remove class", on_click=remove_class)


@solara.component
def AnnotationConfiguration():
    with solara.Card(title="Annotation configuration"):
        with solara.Tooltip(annotate_all_tooltip):
            with solara.Row():
                solara.Checkbox(label="Annotate all spans", value=AnnotationState.annotate_all)
        # with solara.Tooltip(include_keyword_classes):
        #     with solara.Row():
        #         solara.Checkbox(label="Include search classes", value=AnnotationState.include_keywords)


def add_class():
    if current_class.value is not None and len(current_class.value) > 0:
        classes = AnnotationState.span_classes.value
        new_class = current_class.value
        if new_class not in classes:
            classes.append(current_class.value)
        AnnotationState.span_classes.set(classes)
        current_class.set("")
        signal_class_change()


def remove_class():
    remove_from_data = AnnotationState.remove_from_dataset.value
    class_to_remove = AnnotationState.removal_class.value
    span_column = create_annotation_column("", class_to_remove)
    annotation_classes = AnnotationState.span_classes.value
    annotation_classes.remove(class_to_remove)
    df = AnnotationState.get_dataframe(AnnotationState.chosen_dataframe.value)
    if remove_from_data and (df is not None and span_column in df.columns.to_list()):
        df[span_column] = df[span_column].apply(lambda x: remove_annotations(x, class_to_remove))
    AnnotationState.span_classes.set(annotation_classes)
    signal_class_change()


def signal_class_change():
    flip = True if not AnnotationState.span_class_added.value else False
    AnnotationState.span_class_added.set(flip)