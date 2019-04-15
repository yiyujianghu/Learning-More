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

    def sortedArrayToBST(self, nums):
        """将数组转化为平衡二叉树：先将数组有序排列，然后类似于二分查找从中间构建根节点，然后不断递归"""
        if not nums:
            return None
        else:
            nums.sort()
            root = treeNode(nums[len(nums)//2])
            root.left = self.sortedArrayToBST(nums[0: len(nums)//2])
            root.right = self.sortedArrayToBST(nums[len(nums)//2+1: len(nums)])
            return root

    def findMin(self, root):
        """查询树中的最小值的节点，最小值一定在左子树中"""
        if root.left:
            return self.findMin(root.left)
        else:
            return root

    def findMax(self, root):
        """查询树中的最大的节点，最大值一定在右子树中"""
        if root.right:
            return self.findMax(root.right)
        else:
            return root


    def clearTree(self):
        """清除树的各个节点"""
        self.root.left = self.root.right = None
        self.root.val = None



def createTree(root, nums):
    """给定一个数组，按照insert方法构建一棵BST"""
    for i in nums:
        root = tree.insert(root, i)


if __name__ == "__main__":
    tree = BST(treeNode(5))
    createTree(tree.root, [1, 2, 8, 9, 6, 7, 4, 3])
    print("二叉树的结构: ", tree.tree2dict(tree.root))  # 这里可以观察树的内部结构
    tree.clearTree()
    tree.root = tree.sortedArrayToBST([1, 2, 8, 9, 5, 6, 7, 4, 3])
    print("二叉树的结构: ", tree.tree2dict(tree.root))  # 这里可以观察树的内部结构
    print("查询某个数字是否在搜索树中：", tree.query(tree.root, 6))
    print("寻找树中最大值：", tree.findMax(tree.root).val)
    print("寻找树中最小值：", tree.findMin(tree.root).val)
