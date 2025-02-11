from assets.annotation_state import AnnotationState
from assets.state import State
from components.solara_components.annotation import AnnotationClasses, AnnotationReview, AnnotationConfiguration
from components.solara_components.data_upload import DataUpload
from components.solara_components.data_view import DataView
# from tools.dataframe import *
import solara


def SpanAnnotationSidebar():

    chosen_dataframe = State.chosen_dataframe.value
    df = None
    if chosen_dataframe is not None:
        df = State.get_dataframe(chosen_dataframe)

    # Flag monitors to update state when changes occur
    class_change_flag = AnnotationState.span_class_added.value

    with solara.Sidebar():

        # Upload data component
        DataUpload()

        # Choose what to view
        DataView(df)

        # Add annotation classes
        AnnotationClasses()

        # Review annotation classes
        AnnotationReview()

        # Configure annotation
        AnnotationConfiguration()


