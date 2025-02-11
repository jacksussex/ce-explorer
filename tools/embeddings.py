from sentence_transformers import SentenceTransformer
from solara.lab import task
import fields

try:
    # embeddings model
    model = "all-MiniLM-L6-v2"
    sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
except:
    print("can't load model")


@task
def create_sentence_embeddings(dataframe,column, progress_callback):
    corpus_length = len(dataframe)
    create_sentence_embeddings.progress = 0
    dataframe[fields._embedding] = dataframe[column].apply(lambda x:create_embedding_doc(x,corpus_length, progress_callback))
    return dataframe

def create_embedding_doc(text_doc, corpus_length, progress_callback):
    create_sentence_embeddings.progress = create_sentence_embeddings.progress + 1
    embedding = sentence_model.encode(text_doc, show_progress_bar=False)
    progress = (create_sentence_embeddings.progress/corpus_length) * 100
    progress_callback(progress)
    return embedding
