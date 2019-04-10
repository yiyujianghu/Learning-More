#!/usr/bin/env python 
# encoding: utf-8  
"""
@author: Dong Jun
@file: backTracking.py
@time: 2019/4/10 10:39
""" 

class BackTracking():
    """回溯算法的经典思路"""
    def depthFirstSearch(self, node):
        """深度优先遍历：将顶层节点先存入栈内，然后向下遍历，找完该路径之后再返回上一层的节点向下遍历"""
        if not node:
            return
        else:
            result = []
            nodeStack = []
            nodeStack.append(node)
            while nodeStack:
                node = nodeStack.pop()
                result.append(node.val)
                if node.right:
                    nodeStack.append(node.right)
                if node.left:
                    nodeStack.append(node.left)
            return result

    def generateParenthesis(self, n):
        """ 生成有效的括号：只有左右两种括号的添加情况->规则“必须先左后右”，数量“左右余量都为0时触底”，
            步骤： 最终状态->按照数量原则，都为0时触底生成一个括号对；
                   中间状态->分支操作，每一步都可以添加“左”也可以添加“右”，左的条件在于左还有，右的条件在于右多于左；
                   初始状态->用空字符串不断分支，加左/右括号后左/右减一，不断分支不断判断，最终形成符合规则设定的分支可能；"""
        self.result = []
        def DFS(left, right, s):
            if left==0 and right==0:
                self.result.append(s)
            else:
                if left>0:
                    DFS(left-1, right, s+"(")
                if right>left:
                    DFS(left, right-1, s+")")
        DFS(n, n, "")
        return self.result


    def subSet(self, nums):
        """ 求解一个集合所有的子集，类似于括号生成的不断分支问题，看着答案手推代码会清晰很多；
            步骤：  1、所有的生成过程都是类似于裂变的构建过程，故而先弄清楚裂变的方法与条件（参考严蔚敏《数据结构》P150）；
                    2、"""
        ###############################提供另一种迭代解法###########################################
        def subsets(nums):
            result = [[]]                   # 第一个解是空集
            for num in nums:                # 遍历所有的数依次添加
                for s in result[:]:         # 这里注意！！！用result会形成死循环的生成器，加了[:]则先计算再循环
                    current = s[:]          # 这里复制一下的原因是为了扩容而非原地添加
                    current.append(num)
                    result.append(current)
            return result
        #############################################################################################
        self.result = []
        def DFS(nums, subset, index):
            if index == len(nums):
                self.result.append(subset)
                return None
            DFS(nums, subset+[nums[index]], index+1)
            DFS(nums, subset, index+1)
        DFS(nums, [], 0)
        return self.result


    def permute(self, nums):
        """全排列问题"""
        pass


    def eightQueens(self):
        """8皇后问题"""
        pass


if __name__ == "__main__":
    solution = BackTracking()
    print("生成括号:", solution.generateParenthesis(3))
    print("集合子集:", solution.subSet([1, 2, 3]))