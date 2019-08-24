#!/usr/bin/env python
# encoding: utf-8
"""
@author: Dong Jun
@file: ngram.py
@time: 2019/8/22 21:00
"""

import jieba
import numpy as np
import json
import copy
from PinyinCorrector import PinyinCorrector


class NGram():
    def __init__(self, sentence):
        self.sentence = sentence


    def loadModel(self, ngram_path):
        with open(ngram_path, "r", encoding="utf-8") as f:
            ngram_dict = json.load(f)
        return ngram_dict


    def probSearch(self, subDict, wordList):
        try:
            if len(wordList) == 0:
                return subDict["prob"]
            else:
                return self.probSearch(subDict[wordList[0]], wordList[1:])
        except:
            return -100


    def correctERROR(self, error_word, index, N, dictProb):
        wordList = self.sentenceList[index: index + N]
        corrector = PinyinCorrector(error_word)
        corrector.wordCandidate()
        word_candidate = corrector.word_candidate
        word_candidate_score = []
        for word in word_candidate:
            wordList[N-1] = word
            probability = self.probSearch(dictProb[wordList[0]], wordList[1:])
            word_candidate_score.append({"word": word, "score": probability})
        word_candidate_score.sort(key=lambda x: x["score"], reverse=True)
        return word_candidate_score[0]["word"]


    def detectERROR(self, dictProb, N, threshold):
        stopList = ["，", "。", "！", "："]
        self.sentenceList = [word for word in jieba.cut(self.sentence) if word not in stopList]
        print("原始语句：", " ".join(self.sentenceList))
        for i in range(len(self.sentenceList)-N):
            errorDisplay = copy.deepcopy(self.sentenceList)
            wordList = self.sentenceList[i: i+N]
            if wordList[0] not in dictProb:
                errorDisplay[i] = "\033[0;31m{}\033[0m".format(self.sentenceList[i])
                continue
            probability = self.probSearch(dictProb[wordList[0]], wordList[1:])
            if probability < threshold:
                wordERROR = self.sentenceList[i + N - 1]
                errorDisplay[i+N-1] = "\033[0;31m{}\033[0m".format(self.sentenceList[i+N-1])
                print("\033[0;31m{}\033[0m".format("发现错误："), " ".join(errorDisplay))
                corrected_word = self.correctERROR(wordERROR, i, N, dictProb)
                self.sentenceList[i+N-1] = corrected_word
                rightDisplay = copy.deepcopy(self.sentenceList)
                rightDisplay[i+N-1] = "\033[0;36m{}\033[0m".format(self.sentenceList[i+N-1])
                print("\033[0;36m{}\033[0m".format("拼音改正："), " ".join(rightDisplay))


    @classmethod
    def rmStopword(cls, data):
        stopList = ["，", "。", "！", "："]
        for i in range(len(data)):
            line = []
            for w in data[i].split(" "):
                if w not in stopList:
                    line.append(w)
            data[i] = line
        return data


    @classmethod
    def loadStopList(cls):
        pass


    @classmethod
    def addLine(cls, currNode, wordList, N):
        for i in range(len(wordList)):
            cls.addNode(currNode, wordList[i:], N)


    @classmethod
    def addNode(cls, currNode, wordList, N):
        if wordList[0] not in currNode:
            currNode[wordList[0]] = {"count": 1}
        else:
            currNode[wordList[0]]["count"] += 1
        if len(wordList[1:N]) > 0:
            cls.addNode(currNode[wordList[0]], wordList[1:N], N - 1)


    @classmethod
    def calOneCount(cls, dictStatic):
        oneCountList = [dictStatic[k]["count"] for k in dictStatic.keys()]
        oneCount = np.array(oneCountList).sum()
        return oneCount


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


    @classmethod
    def train(cls, data, N):
        data = cls.rmStopword(data)
        dictStatic = {}
        for line in data:
            cls.addLine(dictStatic, line, N)
        dictStatic["count"] = cls.calOneCount(dictStatic)
        dictProbability = {"prob": 0}
        dictProbability = cls.caculateProb(dictStatic, dictProbability["prob"])
        with open("data/ngram.model", "w", encoding="utf-8") as f:
            f.write(json.dumps(dictProbability, ensure_ascii=False))


if __name__ == "__main__":
    # 模型训练
    data = ["为了祖国，为了胜利，向我开炮！向我开炮！",
            "记者：你怎么会说出那番话，我只是觉得",
            "我只是觉得，对准我自己打"]
    data = [" ".join(jieba.lcut(e)) for e in data]
    NGram.train(data, 3)

    # 错误检测
    sentence = "为了祖国，为了审理，向我来到！向我开炮！"
    example = NGram(sentence)
    dictProbability = example.loadModel("data/ngram.model")
    example.detectERROR(dictProbability, 3, -50)
