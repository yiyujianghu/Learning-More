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

    def getDepth(self, node):
        """求解树的深度"""
        if not node:
            return 0
        else:
            ldepth = self.getDepth(node.left)
            rdepth = self.getDepth(node.right)
            return 1+max(ldepth, rdepth)

    def tree2dict(self, node):
        """简单的二叉树转字典的函数。"""
        if node.left and node.right:
            dictTree = {}
            dictTree[node.val] = {"left": self.tree2dict(node.left), "right": self.tree2dict(node.right)}
        elif node.left:
            dictTree = {}
            dictTree[node.val] = {"left": self.tree2dict(node.left)}
        elif node.right:
            dictTree = {}
            dictTree[node.val] = {"right": self.tree2dict(node.right)}
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

    def preSearch(self):
        """前序遍历的非递归方法"""
        node = self.root
        if not node:
            return
        else:
            nodeStack = []
            result = []
            while node or nodeStack:
                while node:
                    result.append(node.val)
                    nodeStack.append(node)
                    node = node.left
                node = nodeStack.pop()
                node = node.right
            return result


    def inSearch(self):
        """中序遍历的非递归方法"""
        node = self.root
        if not node:
            return
        else:
            nodeStack = []
            result = []
            while node or nodeStack:
                while node:
                    nodeStack.append(node)
                    node = node.left
                node = nodeStack.pop()
                result.append(node.val)
                node = node.right
            return result

    def backSearch(self):
        """后序遍历的非递归方法"""
        node = self.root
        if not node:
            return
        else:
            nodeStack1 = []
            nodeStack2 = []
            result = []
            while node or nodeStack1:
                while node:
                    nodeStack1.append(node)
                    nodeStack2.append(node)
                    node = node.right
                node = nodeStack1.pop()
                node = node.left
            while nodeStack2:
                result.append(nodeStack2.pop().val)
            return result


    def breadthFirstSearch(self):
        """宽度优先遍历，层次遍历：利用队列的先入先出来弹出node节点"""
        node = self.root
        if not node:
            return
        else:
            result = []
            nodeQueue = deque()
            nodeQueue.append(node)
            while nodeQueue:
                node = nodeQueue.popleft()
                result.append(node.val)
                if node.left:
                    nodeQueue.append(node.left)
                if node.right:
                    nodeQueue.append(node.right)
            return result

    def depthFirstSearch(self):
        """深度优先遍历：利用栈的后入先出来弹出node节点"""
        node = self.root
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

    @staticmethod
    def orderPrint(func):
        orderList = {"preOrder": "前序遍历: ", "inOrder": "中序遍历: ", "backOrder": "后序遍历: "}
        searchList = {"breadthFirstSearch": "宽度优先遍历: ", "depthFirstSearch": "深度优先遍历: ",
                      "preSearch": "前序(非递归): ", "inSearch": "中序(非递归): ", "backSearch": "后序(非递归): "}
        if func.__name__ in orderList:
            print(orderList[func.__name__], end="")
            func(tree.root)
            print(" ")
        elif func.__name__ in searchList:
            print(searchList[func.__name__], end="")
            re = func()
            print(" ".join([str(x) for x in re]))
        else:
            print("没有找到这种遍历方法！")


def createTree(L):
    """简单的构建一棵完全二叉树"""
    tree = Tree()
    for x in L:
        tree.addNode(x)
    # tree.root.left.left.left = treeNode(7)   # 这里简单的加入一个孤立节点
    tree.root.right.right.right = treeNode(14)   # 这里简单的加入一个孤立节点
    return tree


if __name__ == "__main__":
    L = [i for i in range(10)]
    tree = createTree(L)
    print("二叉树的结构: ", tree.tree2dict(tree.root))    # 这里可以观察树的内部结构
    print("二叉树的深度: {}层".format(tree.getDepth(tree.root)))
    print("\n-----三种遍历的递归方法-----")
    Tree.orderPrint(tree.preOrder)
    Tree.orderPrint(tree.inOrder)
    Tree.orderPrint(tree.backOrder)
    print("\n-----五种遍历的非递归方法-----")
    Tree.orderPrint(tree.preSearch)
    Tree.orderPrint(tree.inSearch)
    Tree.orderPrint(tree.backSearch)
    Tree.orderPrint(tree.breadthFirstSearch)
    Tree.orderPrint(tree.depthFirstSearch)

