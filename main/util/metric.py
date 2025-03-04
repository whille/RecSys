#! /usr/bin/python3
# coding=utf-8
"""
    评分
"""
import math
from operator import itemgetter


def RMSE(records):
    """计算RMSE
        @param records: 预测评价与真实评价记录的一个list
        @return: RMSE
    """
    numerator = sum([(pred_rating - actual_rating)**2
                     for pred_rating, actual_rating in records])
    denominator = float(len(records))
    return math.sqrt(numerator / denominator)


def MSE(records):
    """计算MSE
        @param records: 预测评价与真实评价记录的一个list
        @return: MSE
    """
    numerator = sum([(pred_rating - actual_rating)**2
                     for pred_rating, actual_rating in records])
    denominator = float(len(records))
    return numerator / denominator


def precision(recommends, tests):
    """计算Precision
    :param recommends: dict
        给用户推荐的商品，recommends为一个dict，格式为 { userID : 推荐的物品 }
    :param tests: dict
        测试集，同样为一个dict，格式为 { userID : 实际发生事务的物品 }
    :return: float
        Precision
    """
    n_union = 0.
    test_sum = 0.
    for uid, items in recommends.items():
        recommend_set = set(items)
        test_set = set(tests[uid])
        n_union += len(recommend_set & test_set)
        test_sum += len(test_set)

    return n_union / test_sum


def recall(recommends, tests):
    """
        计算Recall
        @param recommends:   给用户推荐的商品，recommends为一个dict，格式为 { userID : 推荐的物品 }
        @param tests:  测试集，同样为一个dict，格式为 { userID : 实际发生事务的物品 }
        @return: Recall
    """
    n_union = 0.
    recommend_sum = 0.
    for uid, items in recommends.items():
        recommend_set = set(items)
        test_set = set(tests[uid])
        n_union += len(recommend_set & test_set)
        recommend_sum += len(recommend_set)

    return n_union / recommend_sum


def precision_recall(recommends, tests):
    """
        同时计算Precision and Recall
        @param recommends:   给用户推荐的商品，recommends为一个dict，格式为 { userID : 推荐的物品 }
        @param tests:  测试集，同样为一个dict，格式为 { userID : 实际发生事务的物品 }
        @return: float, float
    """
    n_union = 0.
    test_sum = 0.
    recommend_sum = 0.
    for uid, items in recommends.items():
        recommend_set = set(items)
        test_set = set(tests[uid])
        n_union += len(recommend_set & test_set)
        test_sum += len(test_set)
        recommend_sum += len(recommend_set)
    return n_union / test_sum, n_union / recommend_sum


def Precision_Recall(train, test, N, recommend_f):
    hit, all_t, all_ = 0., 0, 0
    for u in train:
        tu = test[u]
        rank = recommend_f(u, N)
        for i, _ in rank:
            if i in tu:
                hit += 1
        all_t += len(tu)
        all_ += N
    return hit / (all_t), hit / all_


def Coverage(train, N, recommend_f):
    recommend_items = set()
    all_items= set()
    for u in train:
        for i in train[u]:
            all_items.add(i)
        rank = recommend_f(u, N)
        for i, _ in rank:
            recommend_items.add(i)
    return 1. * len(recommend_items) / len(all_items)


def Popularity(train, N, recommend_f):
    item_pop = {}
    for u, items in train.items():
        for i in items:
            item_pop[i] = item_pop.setdefault(i, 0) + 1
    ret = 0
    n = 0
    for u in train:
        rank = recommend_f(u, N)
        for i, _ in rank:
            ret += math.log(1 + item_pop[i])
            n += 1
    return 1. * ret / n


def coverage(recommends, all_items):
    """
        计算覆盖率
        @param recommends : dict形式 { userID : Items }
        @param all_items :  所有的items，为list或set类型
    """
    recommend_items = set()
    for _, items in recommends.items():
        for item in items:
            recommend_items.add(item)
    return 1. * len(recommend_items) / len(all_items)


def popularity(item_popular, recommends):
    """计算流行度
        @param item_popular:  商品流行度　dict形式{ itemID : popularity}
        @param recommends :  dict形式 { userID : Items }
        @return: 平均流行度
    """
    pop = 0.  # 流行度
    n = 0.
    for items in recommends.values():
        for item in items:
            pop += math.log(1. + item_popular.get(item, 0.))
            n += 1
    return pop / n


def entrophy(item_popular):
    ent = 0.
    for pi in item_popular.values():
        ent += pi * math.log(pi)
    return - ent


def GiniIndex(item_popular):
    j = 1
    n = len(item_popular)
    G = 0
    for item, weight in sorted(item_popular.items(), key=itemgetter(1)):
        G += (2 * j - n - 1) * weight
    return G / float(n - 1)


def diversity(recommends, sim):
    # TODO, sim: similarity function or data of item i and j
    D, Du = 0., 0.
    for uid, Ru in recommends.items():
        sum_d = 0.
        for items in recommends.values():
            for i in items:
                for j in items:
                    if i == j:
                        continue
                    sum_d += sim(i, j)
        Du = 1 - sum_d / (0.5 * len(recommends) * (len(recommends) - 1))
        D += Du
    return D / len(recommends)
