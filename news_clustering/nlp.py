from typing import List, Tuple

import nltk
import numpy as np
# TODO: Make local copy
from deeppavlov.models.embedders.fasttext_embedder import FasttextEmbedder

embedder = FasttextEmbedder(
    "~/.deeppavlov/downloads/embeddings/ft_native_300_ru_wiki_lenta_lower_case.bin"
)


def get_mean_embeddings(tokens: List[List[str]]) -> List[List[float]]:
    return [np.mean(sent_embeddings, axis=0).tolist() for sent_embeddings in embedder(tokens)]


def sentence_embedder(sentence: str) -> List[float]:
    return get_mean_embeddings([nltk.word_tokenize(sentence)])[0]


def text_embedder(text: str) -> Tuple[List[List[float]], List[str]]:
    sentences = nltk.sent_tokenize(text)
    tokens = [nltk.word_tokenize(sentence) for sentence in sentences]
    return get_mean_embeddings(tokens), sentences


def article_sentence_cluster_distances(article_embs, cluster_embs):
    article_min_distances = []

    for article_emb in article_embs:
        min_distance = 1000

        for cluster_emb in cluster_embs:
            article_emb = np.array(article_emb)
            cluster_emb = np.array(cluster_emb)

            distance = np.linalg.norm(article_emb - cluster_emb)

            if distance < min_distance:
                min_distance = distance

        article_min_distances.append(min_distance)

    return article_min_distances
