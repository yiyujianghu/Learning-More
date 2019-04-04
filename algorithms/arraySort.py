#!/usr/bin/env python 
# encoding: utf-8  
"""
@author: Dong Jun
@file: arraySort.py
@time: 2019/4/4 9:50
根据Sedgewick的《算法》第2章中排序的部分，将Java代码改写为python代码
"""
import datetime
import random

class ArraySort():
    def selectionSort(self, array):
        """
        选择排序：依次找到最小值并交换到序列的开头
        """
        for i in range(len(array)):
            minIndex = i
            for j in range(i+1, len(array)):
                if array[j] < array[minIndex]:
                    minIndex = j
            array[i], array[minIndex] = array[minIndex], array[i]
        return array

    def insertionSort(self, array):
        """
        插入排序：
        """

    def isSorted(self, array):
        """
        :param array:要检测的数组；
        :return:True-已排序，False-未排序；
        """
        for i in range(1, len(array)):
            if array[i] < array[i-1]:
                return False
        return True

def result(func, exam):
    """将时间计算及信息打印部分打包成一个函数"""
    # 用于计算某种算法的时间
    time = datetime.timedelta(0)
    for i in range(1000):
        random.shuffle(exam)    # 将测试用例随机打乱再排序，可增加统计效果
        curr1 = datetime.datetime.now()
        func(exam)
        curr2 = datetime.datetime.now()
        time += (curr2-curr1)

    # 用于打印相关信息
    print("#function:", func.__name__)
    print("--time assumme is:", time)
    print("--is sorted?", a.isSorted(func(exam)))

if __name__ == "__main__":
    # 初始化及定义测试用例
    a = ArraySort()
    example = [i for i in range(100)]

    # 比较各种方法的优劣
    result(sorted, example)
    result(a.selectionSort, example)