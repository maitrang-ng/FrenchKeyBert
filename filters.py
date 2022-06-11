import spacy
import jellyfish
import regex as re

#spacy download fr_core_news_lg
#spacy download fr_dep_news_trf

from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop

nlp = spacy.load('fr_core_news_lg',exclude=['attribute_ruler','lemmatizer'])
#'morphologizer'
def filter_ner(list_sentences):
    ner = []
    fr_stop_words = list(fr_stop)
    for sentence in nlp.pipe(list_sentences):
        ent_ = ([ent.text for ent in sentence.ents])
        if ent_ is not []:
            ner.extend(ent_)
            fr_stop_words.extend(ent_)
    return fr_stop_words, ner

def filter_pos(list_keywords):
    out=[]
    from spacy.matcher import Matcher
    patterns = [
        [{'POS': 'PROPN'}, {'POS': 'VERB'}, {'POS': 'VERB'}],
        [{'POS': 'NOUN'}, {'POS': 'VERB'}, {'POS': 'NOUN'}],
        [{'POS': 'VERB'}, {'POS': 'NOUN'}],
        [{'POS': 'ADJ'}, {'POS': 'ADJ'}, {'POS': 'NOUN'}],  
        [{'POS': 'NOUN'}, {'POS': 'VERB'}],
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'NOUN'}],
        [{'POS': 'ADJ'}, {'POS': 'NOUN'}],
        [{'POS': 'ADJ'}, {'POS': 'NOUN'}, {'POS': 'NOUN'}, {'POS': 'NOUN'}],
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'ADV'}, {'POS': 'PROPN'}],
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'VERB'}],
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}],
        [{'POS': 'NOUN'}, {'POS': 'NOUN'}],
        [{'POS': 'ADJ'}, {'POS': 'PROPN'}],
        [{'POS': 'PROPN'}, {'POS': 'ADP'}, {'POS': 'PROPN'}],
        [{'POS': 'PROPN'}, {'POS': 'ADJ'}, {'POS': 'NOUN'}],
        [{'POS': 'PROPN'}, {'POS': 'VERB'}, {'POS': 'NOUN'}],
        [{'POS': 'NOUN'}, {'POS': 'ADP'}, {'POS': 'NOUN'}],
        [{'POS': 'PROPN'}, {'POS': 'NOUN'}, {'POS': 'PROPN'}],
        [{'POS': 'VERB'}, {'POS': 'ADV'}],
        [{'POS': 'PROPN'}, {'POS': 'NOUN'}]
        ]
    matcher = Matcher(nlp.vocab)
    matcher.add("pos-matcher", patterns)
    # Create Spacy object
    for key in nlp.pipe(list_keywords):
    # Iterate through the matches
        matches = matcher(key)
    # If matches is not empty, it means that at least a match is found
        if len(matches)>0:
            out.append(key)
    return out

# Using Damerau-Levenshtein distance to fuzzy string matching
def fuzzy_string_matching(key_list, threshold=4):
  remove = []
  for i in range(len(key_list)):
    for j in range(i+1,len(key_list)):
      if (jellyfish.levenshtein_distance(key_list[i], key_list[j]) <= threshold) == True:
        remove.append(key_list[i])
  setA = set(key_list)
  setB = set(remove)
  new_set =  setA.difference(setB)
  return list(new_set)