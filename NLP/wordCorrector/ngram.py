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
5、----->已加入字形修正的方法，并增加trie树匹配字形修正中正确的字；
        改进：扩充trie树，订正错别字字典；
        可采用时间评估来计算每个模块消耗的时间，发现主要消耗在候选词的选取上，编辑距离的多层循环比较耗时，尽量杜绝用多层循环；
'''

import jieba
import numpy as np
import json
import copy
import os, sys, time, gc
from datetime import datetime
from memory_profiler import profile
from PinyinCorrector import PinyinCorrector
from MistakeCorrector import MistakeCorrector


class NGram():
    def __init__(self, sentence):
        self.sentence = sentence
        self.base_ngram_path = "data/"
        self.stopword_path = "data/stopword.txt"
        self.stopList = self.loadStopList(self.stopword_path)
        self.stopLocation = []                      # 将停用词的位置信息记录下来，用于最后还原原句
        self.thresholdList = []                     # 对不同位置的阈值，可采用统计方法获得，然后写入list中保存
        self.displayList = ["原始语句："+sentence]   # 用于打印修正过程
        self.userdict_load = False
        self.userdict_path = ""                     # 用于后边向Trie树中添加字典的标识及路径
        self.before_time = datetime.now()
        self.after_time = datetime.now()


    @classmethod
    def loadModel(self, ngram_path):
        with open(ngram_path, "r", encoding="utf-8") as f:
            ngram_dict = json.load(f)
        return ngram_dict


    def delta_time_calculate(self):
        self.after_time = datetime.now()
        delta_time = self.after_time - self.before_time
        self.before_time = datetime.now()
        return delta_time


    def load_userdict(self, file_path, tokenizer_only=True):
        jieba.load_userdict(file_path)
        if tokenizer_only == False:
            self.userdict_load = True
            self.userdict_path = file_path


    def sentencePreprocessed(self):
        self.sentenceList = []
        sentenceCutList = jieba.lcut(self.sentence)
        for i in range(len(sentenceCutList)):
            if sentenceCutList[i] not in self.stopList:
                self.sentenceList.append(sentenceCutList[i])
            else:
                self.stopLocation.append({"word": sentenceCutList[i], "index": i})
        self.sentenceList.insert(0, "<HEAD>")
        self.sentenceList.append("<END>")


    def sentenceRestore(self, sentence_update):
        sentence_restore = copy.deepcopy(sentence_update)
        sentence_restore.pop()
        sentence_restore.pop(0)
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
        word_candidate = []
        # 加入拼音纠正的候选词
        pinyin_corrector = PinyinCorrector(error_word)
        pinyin_corrector.wordCandidate()
        word_candidate.extend(pinyin_corrector.word_candidate)

        # 加入字形等错别字纠正的候选词
        mistake_corrector = MistakeCorrector(error_word)
        mistake_corrector.userdict_load = self.userdict_load
        mistake_corrector.userdict_path = self.userdict_path
        mistake_corrector.wordCandidate()
        word_candidate.extend(mistake_corrector.word_candidate)

        word_candidate_score = []
        for word in word_candidate:
            wordList[-1] = word
            probability = self.probSearch(dictProb[wordList[0]], wordList[1:])
            word_candidate_score.append({"word": word, "score": probability})
        word_candidate_score.sort(key=lambda x: x["score"], reverse=True)
        return word_candidate_score[0]


    def detectERROR(self, N=3, threshold=-50, direction="front"):
        if direction=="bi_direction":
            self.detectERROR(N, threshold, "front")
            self.detectERROR(N, threshold, "back")
            return None
        try:
            dictProb = self.loadModel(self.base_ngram_path+"{}_{}gram.model".format(direction, N))
        except:
            return None
        self.sentencePreprocessed()
        directionInformation = "*** 正向检测 >>>" if direction=="front" else "*** 反向检测 >>>"
        sentenceList4detect = self.sentenceList if direction=="front" else list(reversed(self.sentenceList))
        self.displayList.append(directionInformation)
        length = len(self.sentenceList)
        for i in range(len(sentenceList4detect) - N):
            index4update = (i+N)-1 if direction=="front" else length-(i+N)          # 考虑到正方两种顺序错误词的标号不同
            errorDisplay = copy.deepcopy(self.sentenceList)
            wordList = sentenceList4detect[i: i + N]
            if wordList[0] not in dictProb:
                # errorDisplay[i] = "\033[0;31m{}\033[0m".format(self.sentenceList[i])
                continue
            probability = self.probSearch(dictProb[wordList[0]], wordList[1:])
            if probability < threshold:
                wordERROR = self.sentenceList[index4update]
                errorDisplay[index4update] = "\033[0;31m{}\033[0m".format(self.sentenceList[index4update])
                self.displayList.append("\033[0;31m{}\033[0m".format("发现错误：")+self.sentenceRestore(errorDisplay))
                corrected_word_item = self.correctERROR(wordList, wordERROR, dictProb)
                if corrected_word_item["score"] > threshold:
                    sentenceList4detect[i+N-1] = corrected_word_item["word"]
                    self.sentenceList[index4update] = corrected_word_item["word"]
                else:
                    continue
                rightDisplay = copy.deepcopy(self.sentenceList)
                rightDisplay[index4update] = "\033[0;36m{}\033[0m".format(self.sentenceList[index4update])
                self.displayList.append("\033[0;36m{}\033[0m".format("错误改正：")+self.sentenceRestore(rightDisplay))
        self.sentence = self.sentenceRestore(self.sentenceList)
        self.sentenceList.clear()
        self.stopLocation.clear()


    def display(self):
        for line in self.displayList:
            print(line)
        print(">>> 检测完毕 ***")


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
    def addLine(cls, currNode, wordList_line, N):
        for i in range(len(wordList_line)):
            cls.addNode(currNode, wordList_line[i:], N)


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
    def data2dictStatic(cls, data_input, N, direction):
        data = cls.rmStopword(data_input)
        for i in range(len(data)):
            data[i].insert(0, "<HEAD>")
            data[i].append("<END>")
            if direction == "back":
                data[i] = data[i][::-1]
        dictStatic = {}
        for line in data:
            cls.addLine(dictStatic, line, N)
        dictStatic["count"] = cls.calOneCount(dictStatic)
        return dictStatic


    @classmethod
    def file2dictStatic(cls, file_path, N, direction, need_cut):
        dictStatic = {}
        stopList = cls.loadStopList("data/stopword.txt")
        line_count = 0
        file_list = []
        if os.path.isfile(file_path):  # 如果是单个文件则当作list处理
            file_list.append(file_path)
        elif os.path.isdir(file_path):  # 如果单个文件太大，内存不够，则拆分成多个文件放在文件夹中，依次写入数据
            for fname in os.listdir(file_path):
                file_list.append(file_path + "/" + fname)
        file_num = len(file_list)
        for i in range(file_num):
            if file_num > 1:
                print("file_name：{}，已完成转换行数：{}万，已完成转换进度：{}%".format(file_list[i], line_count // 10000,
                                                                    (100 * i) // file_num))
                print("查看dictStatic内存占用：{}".format(sys.getsizeof(dictStatic)))
            with open(file_list[i], "r", encoding="utf-8") as file:
                for line in file:
                    if len(line) <= 1:
                        continue
                    else:
                        line_count += 1
                        if need_cut == True:
                            line_data = [w for w in jieba.cut(line.replace("\n", "")) if w not in stopList]
                        else:
                            line_data = cls.rmStopword([line.replace("\n", "")])[0]
                        line_data.insert(0, "<HEAD>")
                        line_data.append("<END>")
                        if direction == "back":
                            line_data = line_data[::-1]
                        cls.addLine(dictStatic, line_data, N)
        dictStatic["count"] = cls.calOneCount(dictStatic)
        return dictStatic


    @classmethod
    def train(cls, data_input, N, direction="front"):
        dictStatic = cls.data2dictStatic(data_input, N, direction)
        dictProbability = {"prob": 0}
        dictProbability = cls.caculateProb(dictStatic, dictProbability["prob"])
        with open("data/{}_{}gram.model".format(direction, N), "w", encoding="utf-8") as f:
            f.write(json.dumps(dictProbability, ensure_ascii=False))
        return dictProbability


    @classmethod
    # @profile
    def train_from_file(cls, file_path, N, direction="front", need_cut=True):
        """ direction：正向还是反向训练ngram；
            need_cut： 输入语句是否需要做分词处理，need_cut==True时，文件中的语句需要做分词处理；
            @profile： 用于打印内存状况的装饰器；
        """
        dictStatic = cls.file2dictStatic(file_path, N, direction, need_cut)
        dictProbability = {"prob": 0}
        dictProbability = cls.caculateProb(dictStatic, dictProbability["prob"])
        dictStatic.clear()
        with open("data/{}_{}gram.model".format(direction, N), "w", encoding="utf-8") as f:
            f.write(json.dumps(dictProbability, ensure_ascii=False))
        return dictProbability


if __name__ == "__main__":
    # 模型训练
    context = ["为了祖国，为了胜利，向我开炮！向我开炮！",
            "记者：你怎么会说出那番话，我只是觉得",
            "我只是觉得，对准我自己打"]
    context = [" ".join(jieba.lcut(e)) for e in context]
    x = NGram.train(context, 3, "front")
    # NGram.train(context, 3, "back")

    y = NGram.train_from_file("data/ngram_test", 3, direction="front", need_cut=True)
    print("x==y", x==y)

    # NGram.train_from_file("data/wiki_jieba_test", 3, direction="front", need_cut=False)
    # NGram.train_from_file("data/wiki_jieba", 3, direction="back", need_cut=False)


    # 错误检测
    # sentence = "推动传统流通企业创新转型升级。"
    # example = NGram(sentence)
    # example.load_userdict("data/dict.txt")
    # example.detectERROR(3, -50, "bi_direction")
    # example.display()
