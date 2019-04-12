#!/usr/bin/env python 
# encoding: utf-8  
"""
@author: Dong Jun
@file: biSearchTree.py
@time: 2019/4/12 16:29
"""

class treeNode():
    """先构建一个树节点"""
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

class BST():
    """构建一棵二叉搜索树"""
    def __init__(self, root):
        self.root = root

    def insert(self, root, val):
        """插入一个val值"""
        if not root:
            root = treeNode(val)
        else:
            if val > root.val:
                root.right = self.insert(root.right, val)
            elif val < root.val:
                root.left = self.insert(root.left, val)
        return root

    def query(self, root, val):
        """查询val是否在树中，返回True或False"""
        if not root:
            return False
        else:
            if root.val > val:
                 return self.query(root.left, val)
            elif root.val < val:
                return self.query(root.right, val)
            else:
                return True

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



def createTree(root, nums):
    """给定一个数组，构建一棵BST"""
    for i in nums:
        root = tree.insert(root, i)


if __name__ == "__main__":
    root = treeNode(5)
    tree = BST(root)
    createTree(tree.root, [1, 2, 8, 9, 6, 7, 4, 3])
    print("二叉树的结构: ", tree.tree2dict(tree.root))  # 这里可以观察树的内部结构，感觉结构颇为怪奇
    print("查询某个数字是否在搜索树中：", tree.query(root, 4))

