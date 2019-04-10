#!/usr/bin/env python 
# encoding: utf-8  
"""
@author: Dong Jun
@file: test.py
@time: 2019/4/10 11:57
"""


class Solution:
    def subsets(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        self.results = []
        def search(nums, S, index):
            if index == len(nums):
                self.results.append(S)
                return

            search(nums, S + [nums[index]], index + 1)
            search(nums, S, index + 1)
        search(nums, [], 0)
        return self.results





if __name__ == "__main__":
    s = Solution()
    print(s.subsets([2,3,1]))