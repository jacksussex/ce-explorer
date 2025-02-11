from typing import Optional, cast
import solara


class EmbeddingState:

    # Embedding download fields
    embedding_columns = solara.reactive(cast(Optional[list], []))
