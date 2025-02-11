from typing import Optional, cast

from pandas import DataFrame

from assets.state import State
import solara


class AnnotationState(State):

    annotated_df = solara.reactive(cast(Optional[bool], False))
    span_class_added = solara.reactive(cast(Optional[bool], False))

    # span class labels to annotate text
    span_classes = solara.reactive(cast(Optional[list], []))

    # The column to annotate
    # column = solara.reactive(cast(Optional[str], "-- please select --"))

    # The prefix to apply to a column
    prefix = solara.reactive(cast(Optional[str], ""))
    pre_delim = solara.reactive(cast(Optional[str], "_"))
    pre_keep_orig = solara.reactive(cast(Optional[bool], False))

    # The suffix to apply to a column
    suffix = solara.reactive(cast(Optional[str], ""))
    suff_delim = solara.reactive(cast(Optional[str], "_"))
    suff_keep_orig = solara.reactive(cast(Optional[bool], False))

    # Annotate all matching spans
    annotate_all = solara.reactive(cast(Optional[bool], False))
    # Include keyword classes
    include_keywords = solara.reactive(cast(Optional[bool], False))
    # Remove the span annotation from the entire dataset
    remove_from_dataset = solara.reactive(cast(Optional[bool], True))
    # Class for removal
    removal_class = solara.reactive(cast(Optional[str], ""))

    # The core dataset
    data = solara.reactive(cast(Optional[DataFrame], None))

