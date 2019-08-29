#!/usr/bin/env python
# encoding: utf-8
"""
@author: Dong Jun
@file: Kneser_Ney.py
@time: 2019/8/29 4:14 下午
"""


import json
import numpy as np
from ngram import NGram


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



class Kneser_Ney():
    @classmethod
    def _calc_discounts(self, t_nk):
        """通过输入的统计字典来计算discount值，计算公式如下，n的取值在[1,N]之间，对于一个n值有一组discounts值：
            Y = n1 / (n1 + 2*n2)
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





if __name__ == "__main__":
    context = ["我", "你 我", "他", "我", "你"]
    result = NGram.data2dictStatic(context, 2, "front")
    result_back = NGram.data2dictStatic(context, 2, "back")
    print(json.dumps(result, ensure_ascii=False, indent=4, cls=NpEncoder))




