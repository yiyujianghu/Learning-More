#!/usr/bin/env python 
# encoding: utf-8  
"""
@author: Dong Jun
@file: test.py
@time: 2019/4/8 14:06
"""


class Node(object):
    def __init__(self, number):
        self.number = number
        self.lchild = None
        self.rchild = None


class Tree(object):
    lis = []

    def __init__(self):
        self.root = None

    def add(self, number):
        node = Node(number)

        if self.root == None:
            self.root = node
            Tree.lis.append(self.root)
            print("Tree.lis, root", Tree.lis, "node", node.number)
        else:
            while True:
                point = Tree.lis[0]

                if point.lchild == None:
                    point.lchild = node
                    Tree.lis.append(point.lchild)
                    print("Tree.lis, left", Tree.lis, "node", node.number)
                    return
                elif point.rchild == None:
                    point.rchild = node
                    Tree.lis.append(point.rchild)
                    Tree.lis.pop(0)
                    print("Tree.lis right", Tree.lis, "node", node.number)
                    return



if __name__=='__main__':
    t=Tree()
    L = [1,2,3,4,5,6,7]
    for x in L:
        print("x", x)
        t.add(x)