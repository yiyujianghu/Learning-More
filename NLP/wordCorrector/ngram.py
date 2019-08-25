#!/usr/bin/env python
# encoding: utf-8
"""
@author: Dong Jun
@file: ngram.py
@time: 2019/8/22 21:00
"""

'''
待改进的几个地方：
1、由于是ngram向后检测，对于开头的词汇无法改进，考虑是否用反向ngram，当正向修改失败时方向修改错误；也可考虑循环ngram，即也考虑两边对中间的影响；
2、对于分词的依赖：未登录词无法分出，譬如将双字分开成两个单字，这样拼音修正只更改其中一个字，就会继续错下去；
   论文中对此的修正办法是采用5gram的字级别扫描； 
3、拼音改正之外的其他方法，譬如LSTM或其他深度学习的方法，原理也是计算局部概率的异常点，然后提供候选词，然后重新计算更正；还可以加入一些规则辅助之类的；
4、容错处理机制：对于一些未见过的词，根据上下文判断是特有名词之类的，然后不错错误处理，比如看到姓氏猜测此处是姓名；
5、对于汉字的拼写错误，偏旁错误等无法用拼音纠正完全覆盖到；
'''

import jieba
import numpy as np
import json
import copy
from PinyinCorrector import PinyinCorrector


class NGram():
    def __init__(self, sentence):
        self.sentence = sentence
        self.base_ngram_path = "data/"
        self.stopword_path = "data/stopword.txt"
        self.stopList = self.loadStopList(self.stopword_path)
        self.stopLocation = []
        self.thresholdList = []


    @classmethod
    def loadModel(self, ngram_path):
        with open(ngram_path, "r", encoding="utf-8") as f:
            ngram_dict = json.load(f)
        return ngram_dict


    def sentencePreprocessed(self):
        self.sentenceList = []
        sentenceCutList = jieba.lcut(self.sentence)
        for i in range(len(sentenceCutList)):
            if sentenceCutList[i] not in self.stopList:
                self.sentenceList.append(sentenceCutList[i])
            else:
                self.stopLocation.append({"word": sentenceCutList[i], "index": i})


    def sentenceRestore(self, sentence_update):
        sentence_restore = copy.deepcopy(sentence_update)
        for item in self.stopLocation:
            sentence_restore.insert(item["index"], item["word"])
        return "".join(sentence_restore)


    def probSearch(self, subDict, wordList):
        try:
            if len(wordList) == 0:
                return subDict["prob"]
            else:
                return self.probSearch(subDict[wordList[0]], wordList[1:])
        except:
            return -100


    def correctERROR(self, wordList, error_word, dictProb):
        corrector = PinyinCorrector(error_word)
        corrector.wordCandidate()
        word_candidate = corrector.word_candidate
        word_candidate_score = []
        for word in word_candidate:
            wordList[-1] = word
            probability = self.probSearch(dictProb[wordList[0]], wordList[1:])
            word_candidate_score.append({"word": word, "score": probability})
        word_candidate_score.sort(key=lambda x: x["score"], reverse=True)
        return word_candidate_score[0]


    def detectERROR(self, N, threshold, direction):
        self.sentencePreprocessed()
        sentenceList4detect = self.sentenceList if direction=="front" else list(reversed(self.sentenceList))
        length = len(self.sentenceList)
        dictProb = self.loadModel(self.base_ngram_path+"{}_{}_gram.model".format(direction, N))
        for i in range(len(sentenceList4detect) - N):
            index4update = (i+N)-1 if direction=="front" else length-(i+N)
            errorDisplay = copy.deepcopy(self.sentenceList)
            wordList = sentenceList4detect[i: i + N]
            if wordList[0] not in dictProb:
                # errorDisplay[i] = "\033[0;31m{}\033[0m".format(self.sentenceList[i])
                continue
            probability = self.probSearch(dictProb[wordList[0]], wordList[1:])
            if probability < threshold:
                wordERROR = self.sentenceList[index4update]
                errorDisplay[index4update] = "\033[0;31m{}\033[0m".format(self.sentenceList[index4update])
                print("\033[0;31m{}\033[0m".format("发现错误："), self.sentenceRestore(errorDisplay))
                corrected_word_item = self.correctERROR(wordList, wordERROR, dictProb)
                if corrected_word_item["score"] > threshold:
                    sentenceList4detect[i+N-1] = corrected_word_item["word"]
                    self.sentenceList[index4update] = corrected_word_item["word"]
                else:
                    continue
                rightDisplay = copy.deepcopy(self.sentenceList)
                rightDisplay[index4update] = "\033[0;36m{}\033[0m".format(self.sentenceList[index4update])
                print("\033[0;36m{}\033[0m".format("拼音改正："), self.sentenceRestore(rightDisplay))
        self.sentence = self.sentenceRestore(self.sentenceList)
        self.sentenceList.clear()
        self.stopLocation.clear()



    @classmethod
    def rmStopword(cls, data_input):
        data_output = []
        stopList = cls.loadStopList("data/stopword.txt")
        for i in range(len(data_input)):
            line = []
            for w in data_input[i].split(" "):
                if w not in stopList:
                    line.append(w)
            data_output.append(line)
        return data_output


    @classmethod
    def loadStopList(cls, stopword_path):
        stopList = []
        with open(stopword_path, "r", encoding="utf-8") as f:
            for line in f.readlines():
                stopList.append(line.replace("\n", ""))
        return stopList


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
    def train(cls, data_input, N, direction):
        data = cls.rmStopword(data_input)
        if direction == "back":
            data = [line[::-1] for line in data]
        dictStatic = {}
        for line in data:
            cls.addLine(dictStatic, line, N)
        dictStatic["count"] = cls.calOneCount(dictStatic)
        dictProbability = {"prob": 0}
        dictProbability = cls.caculateProb(dictStatic, dictProbability["prob"])
        with open("data/{}_{}_gram.model".format(direction, N), "w", encoding="utf-8") as f:
            f.write(json.dumps(dictProbability, ensure_ascii=False))


if __name__ == "__main__":
    # 模型训练
    context = ["为了祖国，为了胜利，向我开炮！向我开炮！",
            "记者：你怎么会说出那番话，我只是觉得",
            "我只是觉得，对准我自己打"]
    context = [" ".join(jieba.lcut(e)) for e in context]
    NGram.train(context, 3, "front")
    NGram.train(context, 3, "back")

    # 错误检测
    sentence = "为了祖国，为了审理，向我凯跑！向我开炮！"
    print("原始语句：", sentence)
    example = NGram(sentence)
    example.detectERROR(3, -50, "back")
    example.detectERROR(3, -50, "front")
