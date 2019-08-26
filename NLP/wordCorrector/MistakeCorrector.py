#!/usr/bin/env python
# encoding: utf-8
"""
@author: Dong Jun
@file: mistakeCorrector.py
@time: 2019/8/24 17:00
"""

import json
from TrieTree import Trie

class MistakeCorrector():
    def __init__(self, word):
        self.word = word
        self.word_candidate = []
        self.mistake_dict_path = "data/mistake.model"
        self.mistake_dict = self.loadModel(self.mistake_dict_path)


    @classmethod
    def loadModel(cls, mistake_dict_path):
        with open(mistake_dict_path, "r", encoding="utf-8") as f:
            mistake_dict = json.load(f)
        return mistake_dict


    def word_edit(self, word):
        trie_tree = Trie()
        word_edit_list = []
        for i in range(len(word) - 1):
            word_transposition = word[0:i] + word[i + 1] + word[i] + word[i + 2:]
            if trie_tree.search(word_transposition):
                word_edit_list.append(word_transposition)
        return word_edit_list


    def wordCandidate(self):
        trie_tree = Trie()
        mistake_list = []
        word_candidate_list = []
        for w in self.word:
            mistake_list.append(set(self.mistake_dict.get(w, w)))

        # 用深度遍历求候选拼音的排列组合
        N = len(mistake_list)
        def DFS(per, depth):
            if depth == N:
                if trie_tree.search(per):
                    word_candidate_list.append(per)
            else:
                for w in mistake_list[depth]:
                    DFS(per + w, depth + 1)
        DFS("", 0)
        self.word_candidate.extend(word_candidate_list)
        for word in word_candidate_list:
            self.word_candidate.extend(self.word_edit(word))


if __name__ == "__main__":
    example = MistakeCorrector("白天")
    example.wordCandidate()
    print(example.word_candidate)

