import regex as re

from keywords_extraction import raw_extraction, latent_proba_mmr
from filters import filter_ner, filter_pos

sbert_model = "distiluse-base-multilingual-cased-v1"

def read_txt_file(file_path):
    f = open(file_path,'r', encoding='utf-8')
    doc = f.read()
    return doc

def clean_doc(doc):
    doc = re.sub(r'\n+', '\n', doc)
    doc = re.sub(r',', '.\n', doc)
    doc = re.sub(r"[\([{})\]]", ".\n", doc)
    doc  = re.sub(r'«', '', doc)
    doc = re.sub(r'»', '', doc)
    return doc
    
def split_in_chunks(doc):
    out = []
    threshold = 512
    text = re.split('[.?]', doc)
    for chunk in text:
        if out and len(chunk)+len(out[-1]) < threshold:
            out[-1] += ' '+chunk+'.'
        else:
            out.append(chunk+'.')
    return out

def split_in_sentences(chunk):
    text = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', chunk)
    list_sentences = []
    for sentence in text:
        list_sentences.append(sentence)
    return list_sentences 

# Pipeline
def processing(text):
    text = clean_doc(text)
    chunk = split_in_chunks(text)
    result = []
    ner = []
    for i in range(0,len(chunk)):
        list_sentences = split_in_sentences(chunk[i])
        out = filter_ner(list_sentences)
        list_keywords = raw_extraction(list_sentences=list_sentences, stops=out[1])
        list_keywords = filter_pos(list_keywords)
        last_list = latent_proba_mmr(chunk=chunk[i], key_list=list_keywords, n=2, sbert_model=sbert_model, diversity_ratio=0.3)
        #last_list = keywords_extraction.keywords_extraction(chunk=chunk[i], list_keywords=list_keywords, sbert_model=sbert_model, n1=20, n2=2)
        result.extend(last_list)
        #result.extend(out[1])
        ner.extend(out[1])
    return list(set(ner)), list(set(result))