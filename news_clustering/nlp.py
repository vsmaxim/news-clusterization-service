from typing import List, Tuple

import numpy as np
from deeppavlov.models.embedders.elmo_embedder import ELMoEmbedder
import nltk

# TODO: Make local copy
elmo_paraphrase_embedder = ELMoEmbedder("http://files.deeppavlov.ai/deeppavlov_data/elmo_news_wmt11-16-simple_reduce_para_pretrain_fine_tuned_ep1.tar.gz")


def sentence_embedder(text: str) -> List[float]:
    return elmo_paraphrase_embedder(nltk.word_tokenize(text))


def text_embedder(text: str) -> Tuple[List[List[float]], List[str]]:
    sentences = nltk.sent_tokenize(text)
    return elmo_paraphrase_embedder([nltk.word_tokenize(sent) for sent in sentences]), sentences


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


