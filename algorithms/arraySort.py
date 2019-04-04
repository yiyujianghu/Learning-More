#!/usr/bin/env python 
# encoding: utf-8  
"""
@author: Dong Jun
@file: arraySort.py
@time: 2019/4/4 9:50
"""
import datetime

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
    curr1 = datetime.datetime.now()
    for i in range(10000):
        func(exam)
    curr2 = datetime.datetime.now()

    # 用于打印相关信息
    re = a.selectionSort(exam)
    print("#function:", func.__name__)
    print("--time assumme is:", curr2-curr1)
    print("--is sorted?", a.isSorted(re))

if __name__ == "__main__":
    # 初始化及定义测试用例
    a = ArraySort()
    example = [1,4,2,8,7,6,9,3,5]

    # 比较各种方法的优劣
    result(a.selectionSort, example)