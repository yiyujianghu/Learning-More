#!/usr/bin/env python 
# encoding: utf-8  
"""
@author: Dong Jun
@file: arraySort.py
@time: 2019/4/4 9:50
"""
import datetime
import random
from collections import deque

class ArraySort():
    """根据Sedgewick的《算法》第2章中排序的部分，将Java代码改写为python代码"""

    def bubbleSort(self, array):
        """冒泡排序：比较相邻两个数的大小来分配交换顺序"""
        for i in range(len(array)):
            for j in range(1, len(array)):
                if array[j-1] > array[j]:
                    array[j-1], array[j] = array[j], array[j-1]
                else:
                    continue
        return array

    def selectionSort(self, array):
        """选择排序：依次找到最小值并交换到序列的开头"""
        for i in range(len(array)):
            minIndex = i
            for j in range(i+1, len(array)):
                if array[j] < array[minIndex]:
                    minIndex = j
            array[i], array[minIndex] = array[minIndex], array[i]
        return array

    def insertionSort(self, array):
        """插入排序：模仿整牌的方法，将后一个插入到前边有序数组的指定位置"""
        for i in range(len(array)-1):
            for j in range(i+1, 0, -1):
                if array[j] < array[j-1]:
                    array[j], array[j-1] = array[j-1], array[j]
                else:
                    break
        return array

    def shellSort(self, array):
        """希尔排序：基于插入排序，设定某个阈值后分段排序"""
        k = 3
        while k > 0:
            if k >= len(array):
                continue
            else:
                for x in range(0, k):
                    for y in range(x, len(array)-k, k):
                        for z in range(y+k, 0, -k):
                            if array[z] < array[z-k]:
                                array[z], array[z-k] = array[z-k], array[z]
                            else:
                                break
            k -= 1
        return array


    def mergeSort(self, array):
        """ 归并排序：采用分治算法的思路，二分数组，不断递归，排序后再合并；
            目前没想到太好的办法，采用了双端队列来pop左端数值"""
        sortedArray = []
        N = len(array)
        if N == 1:
            return array
        elif N > 1:
            sortedArray1 = self.mergeSort(array[0: N//2])
            sortedArray2 = self.mergeSort(array[N//2: N])
            sortedDeque1 = deque(sortedArray1)
            sortedDeque2 = deque(sortedArray2)
            while sortedDeque1 and sortedDeque2:
                if sortedDeque1[0] < sortedDeque2[0]:
                    sortedArray.append(sortedDeque1.popleft())
                else:
                    sortedArray.append(sortedDeque2.popleft())
            while sortedDeque1 and not sortedDeque2:
                sortedArray.append(sortedDeque1.popleft())
            while sortedDeque2 and not sortedDeque1:
                sortedArray.append(sortedDeque2.popleft())
            return sortedArray
        else:
            return []


    def quickSort(self, array):
        """ 快速排序：依然采用分治算法的思路，由一个基准值将数组一分为二，然后对左右分别递归二分"""
        stack1 = []
        stack2 = []
        if len(array) == 1:
            return array
        elif len(array) > 1:
            value = array[0]
            for j in range(1, len(array)):
                if array[j] < value:
                    stack1.append(array[j])
                else:
                    stack2.append(array[j])
            stack = self.quickSort(stack1)
            stacktemp = self.quickSort(stack2)
            stack.append(value)
            stack.extend(stacktemp)
            return stack
        else:
            return []



    def stackSort(self, array):
        """
        堆排序：
        """
        pass


    def isSorted(self, array):
        """
        :param array:要检测的数组；
        :return:True-已排序，False-未排序；
        """
        for i in range(1, len(array)):
            if array[i] < array[i-1]:
                return False
        return True

    @staticmethod
    def resultPrint(func, exam):
        """将时间计算及信息打印部分打包成一个函数"""
        # 用于计算某种算法的时间
        time = datetime.timedelta(0)
        judge = True
        for i in range(5000):
            random.shuffle(exam)    # 将测试用例随机打乱再排序，可增加统计效果
            curr1 = datetime.datetime.now()
            result = func(exam)
            curr2 = datetime.datetime.now()
            judge = judge & a.isSorted(result)
            time += (curr2-curr1)

        # 用于打印相关信息
        print("#function:", func.__name__)
        print("--time consumed is:", time)
        print("--is sorted?", judge)

if __name__ == "__main__":
    # 初始化及定义测试用例
    a = ArraySort()
    example = [i for i in range(100)]

    # 比较各种方法的优劣
    ArraySort.resultPrint(sorted, example)
    ArraySort.resultPrint(a.bubbleSort, example)
    ArraySort.resultPrint(a.selectionSort, example)
    ArraySort.resultPrint(a.insertionSort, example)
    ArraySort.resultPrint(a.shellSort, example)
    ArraySort.resultPrint(a.mergeSort, example)
    ArraySort.resultPrint(a.quickSort, example)



    # x = [i for i in range(10)]
    # random.shuffle(x)
    # re = a.quickSort([5, 7, 6, 1, 2, 3, 8, 4, 9, 0])
    # print("result", re)