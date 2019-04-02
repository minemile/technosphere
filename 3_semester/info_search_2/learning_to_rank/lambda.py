import xgboost as xgb
from sklearn.datasets import load_svmlight_file
import numpy as np
from xgboost import DMatrix
import tqdm
import logging
from utils import dcg, idcg, ndcg

class LambdaMART(object):
    def __init__(self, eta=0.1, num_boost=2, max_depth=3, sigma=1):
        self.eta = eta
        self.max_depth = max_depth
        self.sigma = sigma
        self.num_boost = num_boost
        self.query_s = {}
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.DEBUG)


    def eval_ro(self, q_group, q_pred):
        q_group_size = q_group.size
        ro_i_j = np.zeros((q_group_size, q_group_size))
        for i in range(q_group_size):
            for j in range(q_group_size):
        #         num = -sigma * Z_i_j_g[i, j]
                den = (1 + np.exp(self.sigma * (q_pred[i] - q_pred[j])))
                ro_i_j[i, j] = 1 / den
        return ro_i_j

    def eval_s(self, q_group):
        q_group_size = q_group.size
        S_i_j = np.empty((q_group_size, q_group_size), dtype='int64')
        for i in range(q_group_size):
            for j in range(q_group_size):
                if (q_group[i] == q_group[j]):
                    S_i_j[i, j] = 0
                elif (q_group[i] > q_group[j]):
                    S_i_j[i, j] = 1
                elif (q_group[i] < q_group[j]):
                    S_i_j[i, j] = -1
        return S_i_j

    def eval_groups(self, y):
        group_iter = 0
        query_s = {}
        self.log.debug("Started eval group")
        for i, group_size in tqdm.tqdm(enumerate(self.query_groups_sizes)):
            q_group = y[group_iter:group_iter + group_size]
            query_s[i] = self.eval_s(q_group)
            group_iter += group_size
        self.log.debug("Finished eval group")
        return query_s

    def eval_z(self, q_group):
        q_group_size = q_group.size
        Z_i_j = np.zeros((q_group_size, q_group_size))
        idcg_score = idcg(q_group)
        for i in range(q_group_size):
            for j in range(q_group_size):
                if i == j: continue
                delta = np.abs((2**q_group[i] - 2**q_group[j]) * (1 / np.log2(i + 2) - 1 / np.log2(j + 2)))
                Z_i_j[i, j] = delta / idcg_score
        return Z_i_j


    def objective(self, pred, dtrain):
        labels = dtrain.get_label()
        grad = np.ones_like(pred)
        hess = np.ones_like(pred)
        group_iter = 0
        for i, group_size in enumerate(self.query_groups_sizes):
            q_labels = labels[group_iter:group_iter + group_size]
            q_pred = pred[group_iter:group_iter + group_size]
            if np.unique(q_labels).size == 1:
                group_iter += group_size
                continue

            if i % 100 == 0: self.log.debug(f"{i}\titeration")


            S_i_j = self.query_s[i]
            Z_i_j = self.eval_z(q_labels)
            ro_i_j = self.eval_ro(q_labels, q_pred)

            grad[group_iter:group_iter + group_size] = (-self.sigma * Z_i_j * S_i_j * ro_i_j).sum(axis=1)
            hess[group_iter:group_iter + group_size] = (self.sigma**2 * Z_i_j * S_i_j * ro_i_j * (1 - ro_i_j)).sum(axis=1)

            group_iter += group_size
        return grad, hess


    def fit(self, X, y, q_ids):
        self.log.debug("Start fitting...")
        self.query_groups_sizes = np.unique(q_ids, return_counts=True)[1]
        self.query_s = self.eval_groups(y)

        dtrain = xgb.DMatrix(X, label=y)
        param = {"max_depth": self.max_depth, "eta": self.eta, "eval_metric": "ndcg@5"}
        watchlist = [(dtrain, 'train')]
        bst = xgb.train(param, dtrain, self.num_boost, watchlist, obj=self.objective, verbose_eval=True)


if __name__ == '__main__':
    X, y, q_id = load_svmlight_file("train.txt", query_id=True)
    lm = LambdaMART()
    lm.fit(X, y, q_id)
