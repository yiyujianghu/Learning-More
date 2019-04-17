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
        3、其他方法：矩阵表示-> 用邻接矩阵可视化表示这张图
                     优先遍历-> 广度优先遍历（BFS）与深度优先遍历（DFS）
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

    def BFS(self, root):
        """广度优先遍历，从指定节点开始访问，依次访问其邻接节点，并将访问过和已在队列的节点都做标记"""
        visited = []
        result = []
        def bfs():
            while dq:
                node = dq.pop(0)
                result.append(node.id)
                visited.append(node)
                for k in node.connectedTo.keys():
                    if k not in visited and k not in dq:
                        dq.append(k)
        if not root:
            return None
        else:
            dq = [root]
            bfs()
            return result

    def DFS(self, root):
        """深度优先遍历，好像比广度还简单一点，只要标记了访问节点就可以一直递归遍历"""
        visited = []
        result = []
        def dfs(root):
            result.append(root.id)
            visited.append(root)
            for k in root.connectedTo.keys():
                if k not in visited:
                    dfs(k)
        if not root:
            return None
        else:
            dfs(root)
            return result

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
        g.addVertex(i+1)
    g.addEdge(1, 2, 5)
    g.addEdge(1, 6, 2)
    g.addEdge(2, 3, 4)
    g.addEdge(3, 4, 9)
    g.addEdge(4, 5, 7)
    g.addEdge(4, 6, 3)
    g.addEdge(5, 1, 1)
    g.addEdge(6, 5, 8)
    g.addEdge(6, 3, 1)


if __name__ == "__main__":
    g = Graph()
    createGraph()
    print("*"*15, "构造一张图并用邻接矩阵表示", "*"*15)
    print(g.adjacencyMatrix())      # 构造一张图并用邻接矩阵表示
    print("*" * 18, "广度优先与深度优先遍历", "*" * 18)
    print("广度优先遍历：", g.BFS(g.vertList[list(g.vertList.keys())[0]]))
    print("深度优先遍历：", g.DFS(g.vertList[list(g.vertList.keys())[0]]))

