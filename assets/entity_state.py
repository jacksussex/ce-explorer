from collections import defaultdict, Counter
from typing import Optional, cast
from assets.state import State
import solara


class EntityState(State):

    # Entity discovery fields
    entity_dataframe = None
    entity_cell = solara.reactive(cast(Optional[dict],None))
    common_entities = defaultdict(Counter)
    entity_index = defaultdict(list)
    entity_wiki = defaultdict(str)
    # search_results = solara.reactive(cast(Optional[list],[]))
    chosen_entity_type = solara.reactive(cast(Optional[str], None))
    get_wiki_data = solara.reactive(cast(Optional[bool], True))

    @staticmethod
    def reset_entity_view():
        EntityState.entity_cell.value = None
        EntityState.common_entities = defaultdict(Counter)
        EntityState.entity_index = defaultdict(list)
        EntityState.search_results = solara.reactive(cast(Optional[list], []))