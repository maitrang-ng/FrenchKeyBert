import numpy as np
import pandas as pd
import sklearn

from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

sbert_model = "distiluse-base-multilingual-cased-v1"
#sbert_model = "./augSbert"

def raw_extraction(list_sentences, stops):
    # Extract raw keywords which contain 2 words
    ngram = (2,3)
    list_keywords = []
    for sentence in list_sentences:
        try:
            #count = CountVectorizer(ngram_range=ngram).fit([sentence])
            count = TfidfVectorizer(ngram_range=ngram, stop_words=stops).fit([sentence])
            key = count.get_feature_names_out()
        except ValueError: 
            pass
        else:
            list_keywords.extend(key)
    return list_keywords
    
def keywords_extraction(chunk, list_keywords, sbert_model=sbert_model, n1=20, n2=5):
    model = SentenceTransformer(sbert_model)
    
    # From chunk of document, we will choose n1 keywords that have max cosine similarity with the chunk of document
    # From n1 best match keywords, we will choose n2 keywords which has min cosine similarity for diversitification
    # Last result will return n2 keywords
    chunk_embedding = model.encode([chunk])
    keys_embedding = model.encode(list_keywords)
    cosine_1 = cosine_similarity(chunk_embedding, keys_embedding)
    keys_1 = [list_keywords[index] for index in cosine_1.argsort(axis=1)[0][-n1:]]
    keys_1_embed = model.encode(keys_1)
    cosine_2 = cosine_similarity(keys_1_embed, keys_1_embed)

    a = pd.DataFrame(index=np.arange(len(cosine_2)), columns=np.arange(n2+1))
    for i in range(len(cosine_2)):
        s = sum(cosine_2[i][j] for j in cosine_2.argsort(axis=1)[i][:n2])
        a.loc[i] = np.append(cosine_2.argsort(axis=1)[i][:n2],s)
        a_min = a[a[:][n2]==min(a[n2])]
        #keys_2 = [keys_1[int(j)] for j in a_min]

    #return keys_2
    return [keys_1[int(j)] for j in a_min]


# Diversifying founded keywords with Maximal Marginal Relevance
def latent_proba_mmr(chunk, key_list, n=5, sbert_model=sbert_model, diversity_ratio=0.5):
    model = SentenceTransformer(sbert_model)
    
    # Create embedding from chunk & key_list
    chunk_embed = model.encode([chunk])
    key_list_embed = model.encode(key_list)

    # Extract cosine similarity chunk/key, key/key
    distances_1 = cosine_similarity(key_list_embed, chunk_embed)
    distances_2 = cosine_similarity(key_list_embed, key_list_embed)

    # Best keywords
    keywords_idx = [np.argmax(distances_1)]
    candidates_idx = [i for i in range(len(key_list)) if i != keywords_idx[0]]

    for _ in range(n-1):
        # Extract similarities within candidates and
        # between candidates and selected keywords/phrases
        sim_1 = distances_1[candidates_idx,:]
        sim_2 = np.max(distances_2[candidates_idx][:, keywords_idx], axis=1)

        # Calcul MMR
        plmmr = (1-diversity_ratio) * sim_1 - diversity_ratio * sim_2.reshape(-1, 1)
        plmmr_idx = candidates_idx[np.argmax(plmmr)]

        # Update keywords & candidates
        keywords_idx.append(plmmr_idx)
        candidates_idx.remove(plmmr_idx)

    return [str(key_list[idx]) for idx in keywords_idx]