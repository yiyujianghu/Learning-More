#!/usr/bin/env python
# encoding: utf-8
"""
@author: Dong Jun
@file: Kneser_Ney.py
@time: 2019/8/29 4:14 下午
"""


import json
import numpy as np
from collections import Counter, defaultdict
from copy import deepcopy


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


class BaseNGramProb():
    @classmethod
    def caculateProb(cls, dictStatic, probBF):
        dictProb = {}
        summary = dictStatic.pop("count") if dictStatic["count"] > 0 else 1
        for k in dictStatic.keys():
            dictProb[k] = {"prob": np.log(dictStatic[k]["count"] / summary) + probBF}
            subDict = cls.caculateProb(dictStatic[k], dictProb[k]["prob"])
            if len(subDict) > 0:
                dictProb[k].update(subDict)
        return dictProb


class Kneser_Ney():
    @classmethod
    def staticDict2staticList(cls, staticDict, N):
        def DFS(perfix, subdict, depth):
            if depth == 0:
                counterDict[tuple(perfix)] = subdict["count"]
            elif len(subdict)>1:
                for k, v in subdict.items():
                    if k is not "count":
                        DFS(perfix+[k], v, depth-1)
            else:
                return None

        kgram_counts = []
        for n in range(N, 0, -1):
            counterDict = defaultdict(int)
            DFS([], staticDict, n)
            counterDictCopy = deepcopy(counterDict)
            kgram_counts.append(counterDictCopy)

        return kgram_counts


    @classmethod
    def _get_discount(cls, discounts, count):
        if count > 3:
            return discounts[3]
        return discounts[count]


    @classmethod
    def _calc_discounts(cls, t_nk):
        """Y = n1 / (n1 + 2*n2)
                    D1 = 1 - 2Y * n2 / n1
            D(c)=   D2 = 2 - 3Y * n3 / n2
                    D3+ = 3 - 4Y * n4 / n3
        """
        Y = t_nk[1] / float(t_nk[1] + 2 * t_nk[2])
        discounts = [0]
        for k in range(1, 4):
            if t_nk[k] == 0:
                discount = 0
            else:
                discount = (k - (k + 1) * Y * t_nk[k + 1] / t_nk[k])
            discounts.append(discount)
        return discounts


    @classmethod
    def _calc_unigram_probs(cls, unigrams):    # 只计算1gram的概率值
        """P(wi) = c(wi) / sum(c(wi))"""
        sum_vals = sum(v for v in unigrams.values())
        unigrams = dict((k, float(v) / sum_vals) for k, v in unigrams.items())
        return unigrams


    @classmethod
    def _calc_order_backoff_probs(cls, order):
        num_kgrams_with_count = Counter(
            value for value in order.values() if value <= 4)
        discounts = cls._calc_discounts(num_kgrams_with_count)
        prefix_count_sum = defaultdict(list)  # [key 1 cnt, key 2 cnt, key 3+ cnt] 记录(prefix, *) *计数为count次，有sum种
        prefix_sums = defaultdict(int)  # 记录(prefix, *)的总个数，和 2-grams 类似，但不包含(prefix,end)这种情况
        backoffs = defaultdict(float)
        for key in order.keys():
            prefix = key[:-1]
            count = order[key]
            if prefix in prefix_count_sum:
                sums = prefix_count_sum.get(prefix)
                sums[count - 1 if count < 2 else 2] += 1
            else:
                sums = [0 for i in range(3)]
                sums[count - 1 if count < 2 else 2] += 1
                prefix_count_sum[prefix] = sums
            prefix_sums[prefix] += count
            discount = cls._get_discount(discounts, count)  # D(c(w i i-n+1))
            order[key] -= discount  # reduction


        for key in order.keys():
            prefix = key[:-1]
            order[key] /= float(prefix_sums[prefix])
            backoffs[prefix] = (cls._get_discount(discounts, 1) * prefix_count_sum.get(prefix)[0] +
                                cls._get_discount(discounts, 2) * prefix_count_sum.get(prefix)[1] +
                                cls._get_discount(discounts, 3) * prefix_count_sum.get(prefix)[2]) \
                               / float(prefix_sums[prefix])
        return backoffs


    @classmethod
    def _interpolate(cls, orders, backoffs):
        for last_order, order, backoff in zip(
                reversed(orders), reversed(orders[:-1]), reversed(backoffs[:-1])):
            for kgram in order.keys():
                prefix, suffix = kgram[:-1], kgram[1:]
                order[kgram] += last_order[suffix] * backoff[prefix]


    @classmethod
    def _calc_probs_without_log(cls, orders):
        backoffs = []
        orders[-1] = cls._calc_unigram_probs(orders[-1])  # calculate 1-gram Pkn(wi)
        for order in orders[:-1]:  # 3-grams and 2-grams
            if len(order)==0:
                continue
            backoff = cls._calc_order_backoff_probs(order)
            backoffs.append(backoff)
        backoffs.append(defaultdict(int))
        cls._interpolate(orders, backoffs)
        return orders


    @classmethod
    def updateProbDict(cls, subDict, keys, prob, prob_sum):
        if len(keys) == 1:
            subDict[keys[0]] = {"prob": np.log(prob)+prob_sum}
            return subDict
        else:
            subDict = subDict[keys[0]]
            prob_sum += subDict["prob"]
            return cls.updateProbDict(subDict, keys[1:], prob, prob_sum)


    @classmethod
    def caculateProb(cls, dictStatic, N):
        kgram_counts = Kneser_Ney.staticDict2staticList(dictStatic, N)
        kgram_counts_prob = cls._calc_probs_without_log(kgram_counts)
        dictProb = {}
        for i in range(len(kgram_counts_prob)-1, -1, -1):
            for keys, prob in kgram_counts_prob[i].items():
                cls.updateProbDict(dictProb, keys, prob, 0)
        return dictProb


if __name__ == "__main__":
    context = ["我", "你 我", "他", "我", "你"]
    result = {'<HEAD>': {'count': 5, '我': {'count': 2}, '你': {'count': 2}, '他': {'count': 1}},
              '我': {'count': 3, '<END>': {'count': 3}},
              '<END>': {'count': 5},
              '你': {'count': 2, '我': {'count': 1}, '<END>': {'count': 1}},
              '他': {'count': 1, '<END>': {'count': 1}},
              'count': 16}
    dictProb = Kneser_Ney.caculateProb(result, 2)
    print(json.dumps(dictProb, ensure_ascii=False, indent=4))

