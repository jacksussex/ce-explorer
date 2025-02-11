from assets.entity_state import EntityState
from assets.state import State
import fields
import solara
from solara.lab import task
# from components.views.view_select import DataView
from spacy import displacy
from tools.spacy_wrapper import SpaCyWrapper, endpoint
from tools.spacy_wrapper import spacy_doc_col
import pandas as pd
from tools.web import ping_website

@task
def parse_data(column, get_wiki_date):
    dataframe_names = State.dataframe_names.value
    chosen_df = State.chosen_dataframe.value
    i = dataframe_names.index(chosen_df)
    dataframe = State.dataframes.value[i]
    spacy = SpaCyWrapper(include_fishing=get_wiki_date)
    if spacy_doc_col(column) not in dataframe.columns:
        dataframe = spacy.nlp_dataframe(dataframe=dataframe, text_column=column, progress=parse_data)
    dataframe[[rendered_entities(column),rendered_dependency(column)]] = dataframe.apply(lambda row: update_entities(row.name, row[spacy_doc_col(column)],column), axis=1, result_type='expand')
    State.dataframes.value[i] = dataframe
    return dataframe

def display_cell(cell):
    ent_html = "<body>" + displacy.render(cell, style="dep", jupyter=False) + " </body>"
    solara.HTML(tag="html", unsafe_innerHTML=ent_html)

def rendered_entities(val : str) -> str:
    val = val + '_' + fields._entities
    return val

def update_entities(index,spacy_doc,column):
    update_common_entities(index,spacy_doc)
    return {rendered_entities(column) : displacy_render_objects(spacy_doc,"ent"), rendered_dependency(column) : displacy_render_objects(spacy_doc,'dep')}

def update_common_entities(index, spacy_doc):
    common_entities = EntityState.common_entities
    entity_index = EntityState.entity_index
    entity_wiki = EntityState.entity_wiki
    for ent in spacy_doc.ents:
        common_entities[ent.label_].update([ent.text])
        entity_index[ent.text].append(index)
        if EntityState.get_wiki_data.value:
            if ent.text not in entity_wiki:
                entity_wiki[ent.text] = (ent._.url_wikidata, ent._.kb_qid, ent._.nerd_score, ent._.description) if ent._.url_wikidata else None

def displacy_render_objects(doc, style="ent"):
    ent_html = displacy.render(doc, style=style, jupyter=False, page=False, minify=True)
    return ent_html

def rendered_dependency(val):
    val = val + '_' + fields._pos_tags
    return val

def create_entity_doc_df(counter):
    keys = list(counter.keys())
    print(keys)
    entity_index = EntityState.entity_index
    entity_dict = {"Entity": keys, "Document #" : [counter[x] for x in keys], "Corpus #": [len(entity_index[x]) for x in keys ]}
    if EntityState.get_wiki_data.value:
        entity_dict.update(organise_wiki_data(keys))
    df = pd.DataFrame.from_dict(entity_dict)
    # print([State.entity_wiki[x] for x in keys])
    return df

def organise_wiki_data(keys):
    output_dict = {'wiki-data-link':[], 'wiki-data-id':[],'wiki-data-score':[],'wiki-data-desc':[]}
    for key in keys:
        wiki = EntityState.entity_wiki[key]
        if wiki is not None:
            output_dict['wiki-data-link']=wiki[0]
            output_dict['wiki-data-id']=wiki[1]
            output_dict['wiki-data-score']=wiki[2]
            output_dict['wiki-data-desc']=wiki[3]
    return output_dict
