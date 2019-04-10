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
        """深度优先遍历：将顶层节点先存入栈内，然后向下遍历，找完路径之后再返回上一层的节点"""
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
        """生成有效的括号"""
        pass

    def subSet(self):
        """求解一个集合所有的子集"""
        pass

    def eightQueens(self):
        """8皇后问题"""
        pass


if __name__ == "__main__":
    solution = BackTracking()
    