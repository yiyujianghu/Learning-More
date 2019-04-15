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
        if not node.left and not node.right:
            dictTree = node.val
        else:
            dictTree = {}
            if node.left and node.right:
                dictTree[node.val] = {"left": self.tree2dict(node.left), "right": self.tree2dict(node.right)}
            elif node.left:
                dictTree[node.val] = {"left": self.tree2dict(node.left)}
            elif node.right:
                dictTree[node.val] = {"right": self.tree2dict(node.right)}
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

    def findNode(self, root, val):
        """找到val值对应的相应节点，注意当val值不在二叉树中时应当返回一个空节点"""
        if not self.query(root, val):
            return treeNode(None)
        else:
            if root.val == val:
                return root
            elif root.val > val:
                return self.findNode(root.left, val)
            elif root.val < val:
                return self.findNode(root.right, val)

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

    def getDepth(self, node):
        """求解树的深度"""
        if not node:
            return 0
        else:
            ldepth = self.getDepth(node.left)
            rdepth = self.getDepth(node.right)
            return 1+max(ldepth, rdepth)

    def isBalanced(self, root):
        """判断一棵树是否为平衡二叉树"""
        if not root:
            return True
        else:
            ldepth = self.getDepth(root.left)
            rdepth = self.getDepth(root.right)
            return abs(ldepth-rdepth) <= 1 and self.isBalanced(root.left) and self.isBalanced(root.right)

    def isValidBST(self, root, left=None, right=None):
        """ 判断树是否为二叉搜索树：
            思路1：树的中序遍历为升序，思路常规，按照中序遍历依次即可
            思路2：依次比较左右节点和根节点的大小，本方法想法笨拙但代码犀利"""
        if not root:
            return True
        elif (left and left.val >= root.val) or (right and right.val <= root.val):
            return False
        return self.isValidBST(root.left, left, root) and self.isValidBST(root.right, root, right)

    def deleteNode(self, root, key):
        """ 删除树中的指定节点，
            思路：1、先找到该节点，方法是递归搜索；
                  2、如果该值节点仅仅右左子树或者右子树，则删除该节点并指向左/右节点；
                  3、如果同时有左节点与右节点，则关键在于从右子树中删除找到最小值节点（具体方法见图示）；"""
        if not root:
            return None
        else:
            if root.val > key:
                root.left = self.deleteNode(root.left, key)
            elif root.val < key:
                root.right = self.deleteNode(root.right, key)
            else:
                if not root.left or not root.right:
                    root = root.left if root.left else root.right
                else:
                    root.val = self.findMin(root.right).val
                    root.right = self.deleteNode(root.right, root.val)
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
    print("*"*50)
    print("*****按照insert方式插入节点*****")
    createTree(tree.root, [1, 2, 8, 9, 6, 7, 4, 3])
    print("二叉树的结构: ", tree.tree2dict(tree.root))  # 这里可以观察树的内部结构
    print("这棵树是否为二叉搜索树？ ", tree.isValidBST(tree.root))
    print("这棵树是否为平衡二叉树？ ", tree.isBalanced(tree.root))
    tree.clearTree()
    print("*****按照排序方式插入节点*****")
    tree.root = tree.sortedArrayToBST([1, 2, 8, 9, 5, 6, 7, 4, 3])
    print("二叉树的结构: ", tree.tree2dict(tree.root))  # 这里可以观察树的内部结构
    print("这棵树是否为二叉搜索树？ ", tree.isValidBST(tree.root))
    print("这棵树是否为平衡二叉树？ ", tree.isBalanced(tree.root))
    print("*"*50)
    print("*****查询二叉树中的指定节点*****")
    print("查询某个数字是否在搜索树中：", tree.query(tree.root, 6))
    print("查询某个数字是否在搜索树中：", tree.findNode(tree.root, 6).val)
    print("寻找树中最大值：", tree.findMax(tree.root).val)
    print("寻找树中最小值：", tree.findMin(tree.root).val)
    print("*****删除二叉树中的指定节点*****")
    print("删除树中的某个节点", end=" --> ")
    tree.deleteNode(tree.root, 8)
    print("二叉树的结构: ", tree.tree2dict(tree.root))  # 这里可以观察树的内部结构
