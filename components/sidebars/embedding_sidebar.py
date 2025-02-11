from tempfile import TemporaryFile

from assets.embedding_state import EmbeddingState
from components.solara_components.data_upload import DataUpload
from tools.spacy_wrapper import *
from tools.text import *
from tools.dataframe import *
from tools.embeddings import *

import solara

clean_data_tooltip = "Remove URLS, #tags and @mentions"
remove_stopwords_tooltip = "Remove a standard list of English low information stop-words ('at', 'in', 'of' etc...)"
combine_only_tooltip = "Combine the text columns for download, but do not create embeddings"

@solara.component
def EmbeddingSidebar():

    custom_stopwords, set_custom_stopwords = solara.use_state("")

    clean_data, set_clean_data = solara.use_state(True)
    remove_stopwords, set_remove_stopwords = solara.use_state(False)
    keep_annotations, set_keep_annotations = solara.use_state(False)
    combine_only, set_combine_only = solara.use_state(False)

    processing, set_processing = solara.use_state(False)

    dataframes = State.dataframes.value
    dataframe_names = State.dataframe_names.value

    if State.chosen_dataframe.value is not None:
        df = State.get_dataframe(State.chosen_dataframe.value)
        data_subset, set_data = solara.use_state(df)


        def create_embeddings():
            set_processing(True)
            spacy = SpaCyWrapper(custom_stopwords=custom_stopwords.split(","))
            stopwords = spacy.get_stopwords()
            # print(State.embedding_columns.value)
            set_data(combine_columns(dataframe=data_subset, columns=EmbeddingState.embedding_columns.value,
                                     output_col=fields._cleaned_text))
            # print(data_subset[fields._cleaned_text].to_list())
            solara.Markdown("   Pre-processing data....     ")
            if remove_stopwords:
                set_data(replace_text(dataframe=data_subset, query=stopwords, case_sensitive=False,
                                      column_subset=[fields._cleaned_text], replacement_text=""))
            if clean_data:
                set_data(clean_docs(dataframe=data_subset, doc_col=fields._cleaned_text))
            solara.Markdown("   Creating embeddings....     ")
            # print(data_subset[fields._cleaned_text].to_list())
            if not combine_only:
                create_sentence_embeddings(data_subset, fields._cleaned_text, set_processing)
            if create_sentence_embeddings.finished:
                if keep_annotations:
                    set_data(create_sentence_embeddings.value)
                else:
                    sub_colummns = EmbeddingState.embedding_columns.value + [fields._cleaned_text,
                                                                    fields._embedding] if not combine_only else [
                        fields._cleaned_text, fields._embedding]
                    set_data(create_sentence_embeddings.value[sub_colummns])

        def create_numpy_dump(doc_embeddings):
            outfile = TemporaryFile()
            np.save(file=outfile, arr=np.array(doc_embeddings))
            return outfile

    with solara.Sidebar():

        DataUpload()

        df = None
        if State.chosen_dataframe.value is not None:
            df = State.get_dataframe(State.chosen_dataframe.value)

            # data_subset, set_data = solara.use_state(df)
        solara.ProgressLinear(value=processing)
        with solara.Card("Data selection:"):
            if len(dataframes) > 0:
                solara.Select("Dataset", values=dataframe_names, value=State.chosen_dataframe,
                              on_value=State.reset_column)
            with solara.Row():
                with solara.Tooltip(clean_data_tooltip):
                    solara.Checkbox(label="Clean data", value=clean_data, on_value=set_clean_data)
                with solara.Tooltip(remove_stopwords_tooltip):
                    solara.Checkbox(label="Remove stopwords", value=remove_stopwords, on_value=set_remove_stopwords)
                # solara.Checkbox(label="Keep all annotations", value=keep_annotations, on_value=set_keep_annotations)
                with solara.Tooltip(combine_only_tooltip):
                    solara.Checkbox(label="Combine only", value=combine_only, on_value=set_combine_only)
            with solara.Row():
                solara.InputText("Custom stopwords - 'comma separated values'", value=custom_stopwords,
                                 on_value=set_custom_stopwords)
            if df is not None:
                with solara.Row():
                    solara.SelectMultiple(label="Column select", values=EmbeddingState.embedding_columns,
                                          all_values=df.columns.to_list())
                solara.Button(label="Create embeddings", margin=3, on_click=create_embeddings,
                              disabled=len(EmbeddingState.embedding_columns.value) <= 0)

            if (create_sentence_embeddings.finished and data_subset is not None and fields._embedding in data_subset.columns.to_list()):
                with solara.Card("Download"):
                    with solara.Row(margin=3):
                        solara.FileDownload(create_numpy_dump(data_subset[fields._embedding].to_list()),
                                            label="Download embeddings", filename="embeddings.npy")
                    with solara.Row(margin=3):
                        cols = EmbeddingState.embedding_columns.value
                        dff = df[cols]
                        solara.FileDownload(dff.to_csv(), label="Download data", filename="data.csv")

