# coding : utf-8

import jieba
import numpy as np


class NGram():
    def __init__(self, sentence):
        self.sentence = sentence


    def probSearch(self, subDict, wordList):
        print("subDict, wordList, subDict['prob']", subDict, wordList, subDict["prob"])
        try:
            if len(wordList) == 0:
                return subDict["prob"]
            else:
                return self.probSearch(subDict[wordList[0]], wordList[1:])
        except:
            return -100


    def detectERROR(self, dictProb, N, threshold):
        stopList = ["，", "。", "！", "："]
        self.sentenceList = [word for word in jieba.cut(self.sentence) if word not in stopList]
        print(" ".join(self.sentenceList))
        errIndex = []
        for i in range(len(self.sentenceList)-N):
            wordList = self.sentenceList[i: i+N]
            if wordList[0] not in dictProb:
                errIndex.append(i)
                self.sentenceList[i] = "\033[0;31m{}\033[0m".format(self.sentenceList[i])
                continue
            probability = self.probSearch(dictProb[wordList[0]], wordList[1:])
            print(self.sentenceList[i+N-1], probability)
            if probability < threshold:
                errIndex.append(i+N-1)
                self.sentenceList[i+N-1] = "\033[0;31m{}\033[0m".format(self.sentenceList[i+N-1])
                print(self.sentenceList[i+N-1], probability)
        print(" ".join(self.sentenceList))
        return errIndex


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
        return dictProbability


if __name__ == "__main__":
    data = ["为了祖国，为了胜利，向我开炮！向我开炮！",
            "记者：你怎么会说出那番话，我只是觉得",
            "我只是觉得，对准我自己打"]
    data = [" ".join(jieba.lcut(e)) for e in data]
    dictProbability = NGram.train(data, 3)
    sentence = "为了祖国，为了自由，向我开炮！向我开炮！"
    example = NGram(sentence)
    example.detectERROR(dictProbability, 3, -30)
