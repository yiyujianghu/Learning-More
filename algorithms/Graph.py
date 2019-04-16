#!/usr/bin/env python 
# encoding: utf-8  
"""
@author: Dong Jun
@file: Graph.py
@time: 2019/4/16 16:45
""" 

import pandas as pd

class Vertex():
    """构建一个基本的顶点，包含id值、相连接的其它顶点以及边的权重"""
    def __init__(self, key):
        self.id = key
        self.connectedTo = {}       # dict，key为每个顶点的对象指针，value为指向该顶点的权重值

    def addNeighbor(self, nbr, weight=0):
        self.connectedTo[nbr] = weight

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getWeight(self, nbr):
        return self.connectedTo[nbr]


class Graph():
    """ 采用邻接表的方法构建一张基本的图
        1、基本属性：顶点列表与顶点数量
        2、基本方法：增加顶点-> 按照key增加顶点，并使得顶点数量加1
                     获取顶点-> 查询顶点是否在顶点列表中，返回该顶点或者None
                     增加边  -> 输入起始顶点、终止顶点与权重值，如果顶点不在图中则先增加顶点，然后构建两个顶点的关系
                     矩阵表示-> 用邻接矩阵可视化表示这张图
    """
    def __init__(self):
        self.vertList = {}      # dict，key为每个顶点的id值，value为每个顶点的对象指针
        self.numVertices = 0

    def addVertex(self, key):
        self.numVertices += 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self, Vn):
        if Vn in self.vertList:
            return self.vertList[Vn]
        else:
            return None

    def addEdge(self, Vstart, Vend, cost=0):
        if Vstart not in self.vertList:
            self.addVertex(Vstart)
        if Vend not in self.vertList:
            self.addVertex(Vend)
        self.vertList[Vstart].addNeighbor(self.vertList[Vend], cost)

    def getVertices(self):
        return self.vertList.keys()

    def adjacencyMatrix(self):
        """由邻接表构造一个邻接矩阵的图表示，并用DataFrame的格式存储起来"""
        vertex = self.getVertices()
        self.matrix = pd.DataFrame(index=vertex, columns=vertex)
        for k in self.getVertices():
            for v in self.vertList[k].getConnections():
                self.matrix[v.id].ix[k] = self.vertList[k].getWeight(v)
        self.matrix = self.matrix.fillna(0)
        return self.matrix

    def clear(self):
        """清空图中的顶点，变成一张空图"""
        self.vertList.clear()
        self.numVertices = 0

def createGraph():
    """构建一张简单的图，加入6个顶点与一些边之间的关系"""
    for i in range(6):
        g.addVertex(i)
    g.addEdge(0, 1, 5)
    g.addEdge(0, 5, 2)
    g.addEdge(1, 2, 4)
    g.addEdge(2, 3, 9)
    g.addEdge(3, 4, 7)
    g.addEdge(3, 5, 3)
    g.addEdge(4, 0, 1)
    g.addEdge(5, 4, 8)
    g.addEdge(5, 2, 1)


if __name__ == "__main__":
    g = Graph()
    createGraph()
    print("*"*15, "构造一张图并用邻接矩阵表示", "*"*15)
    print(g.adjacencyMatrix())      # 构造一张图并用邻接矩阵表示

