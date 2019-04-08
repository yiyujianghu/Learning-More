#!/usr/bin/env python 
# encoding: utf-8  
"""
@author: Dong Jun
@file: biTree.py
@time: 2019/4/8 11:09
""" 

from collections import deque

class treeNode():
    """先构建一个树节点"""
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

class Tree():
    """采取从左到右/从上到下的方法依次加入树节点，以构建树"""
    def __init__(self):
        self.root = None
        self.cursor = None
        self.nodeList = []

    def addNode(self, val):
        """增加一个树节点，按照从左到右的顺序，头节点依次加入队列"""
        node = treeNode(val)
        if self.root is None:
            self.root = node
            self.cursor = self.root
            self.nodeList.append(self.cursor)
        else:
            if self.cursor.left is None:
                self.cursor.left = node
                self.nodeList.append(self.cursor.left)
            elif self.cursor.right is None:
                self.cursor.right = node
                self.nodeList.append(self.cursor.right)
                self.nodeList.pop(0)
                self.cursor = self.nodeList[0]

    def tree2dict(self, node):
        """简单的二叉树转字典的函数。二叉树是有顺序的，dict代表层级，list代表有序。"""
        if node.left and node.right:
            dictTree = {}
            dictTree[node.val] = [self.tree2dict(node.left), self.tree2dict(node.right)]
        elif node.left:
            dictTree = {}
            dictTree[node.val] = [self.tree2dict(node.left)]
        elif node.right:
            dictTree = {}
            dictTree[node.val] = [None, self.tree2dict(node.right)]
        else:
            dictTree = node.val
        return dictTree

    def preOrder(self, node):
        """前序遍历"""
        if not node:
            return
        else:
            print(node.val, end=" ")
            self.preOrder(node.left)
            self.preOrder(node.right)

    def inOrder(self, node):
        """中序遍历"""
        if not node:
            return
        else:
            self.inOrder(node.left)
            print(node.val, end=" ")
            self.inOrder(node.right)

    def backOrder(self, node):
        """后序遍历"""
        if not node:
            return
        else:
            self.backOrder(node.left)
            self.backOrder(node.right)
            print(node.val, end=" ")

    def breadthFirstSearch(self, node):
        """宽度优先遍历，层次遍历"""
        if not node:
            return
        else:
            nodeQueue = deque()
            nodeQueue.append(node)
            while nodeQueue:
                cursor = nodeQueue.popleft()
                print(cursor.val, end=" ")
                if cursor.left:
                    nodeQueue.append(cursor.left)
                if cursor.right:
                    nodeQueue.append(cursor.right)

    def depthFirstSearch(self, node):
        """深度优先遍历"""
        if not node:
            return
        else:
            nodeStack = []
            nodeStack.append(node)
            while nodeStack:
                cursor = nodeStack.pop()
                print(cursor.val, end=" ")
                if cursor.right:
                    nodeStack.append(cursor.right)
                if cursor.left:
                    nodeStack.append(cursor.left)

    @staticmethod
    def orderPrint(func):
        orderList = {"preOrder": "前序遍历: ", "inOrder": "中序遍历: ", "backOrder": "后序遍历: ",
                     "breadthFirstSearch": "宽度优先遍历", "depthFirstSearch": "深度优先遍历"}
        print(orderList[func.__name__], end="")
        func(tree.root)
        print("")


def createTree(L):
    """简单的构建一棵完全二叉树"""
    tree = Tree()
    for x in L:
        tree.addNode(x)
    tree.root.left.left.left = treeNode(7)   # 这里简单的加入一个孤立节点
    tree.root.left.right.right = treeNode(10)   # 这里简单的加入一个孤立节点
    return tree


if __name__ == "__main__":
    L = [i for i in range(7)]
    tree = createTree(L)
    print(tree.tree2dict(tree.root))    # 这里可以观察树的内部结构
    Tree.orderPrint(tree.preOrder)
    Tree.orderPrint(tree.inOrder)
    Tree.orderPrint(tree.backOrder)
    Tree.orderPrint(tree.breadthFirstSearch)
    Tree.orderPrint(tree.depthFirstSearch)


