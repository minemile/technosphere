import numpy as np

def dcg(scores, k=None):
    assert scores.ndim == 1
    if k is not None:
        scores = scores[:k]
    gain = (2 ** scores - 1)
    discount = np.log2(np.arange(scores.shape[0]) + 2)
    return np.sum(gain / discount)

def idcg(scores, k=None):
    sorted_scores = np.sort(scores)[::-1]
    return dcg(sorted_scores)

def ndcg(scores, k=None):
    return dcg(scores, k) / idcg(scores, k)
