#!/usr/bin/env python 
# encoding: utf-8  
"""
@author: Dong Jun
@file: backTracking.py
@time: 2019/4/10 10:39
""" 

class BackTracking():
    """回溯算法的经典思路"""
    def depthFirstSearch(self, node):
        """深度优先遍历：将顶层节点先存入栈内，然后向下遍历，找完该路径之后再返回上一层的节点向下遍历"""
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

    def generateParenthesis(self, n):
        """ 生成有效的括号：只有左右两种括号的添加情况->规则“必须先左后右”，数量“左右余量都为0时触底”，
            步骤： 最终状态->按照数量原则，都为0时触底生成一个括号对；
                   中间状态->分支操作，每一步都可以添加“左”也可以添加“右”，左的条件在于左还有，右的条件在于右多于左；
                   初始状态->用空字符串不断分支，加左/右括号后左/右减一，不断分支不断判断，最终形成符合规则设定的分支可能；"""
        self.result = []
        def DFS(left, right, s):
            if left==0 and right==0:
                self.result.append(s)
            else:
                if left>0:
                    DFS(left-1, right, s+"(")
                if right>left:
                    DFS(left, right-1, s+")")
        DFS(n, n, "")
        return self.result


    def subSet(self, nums):
        """ 求解一个集合所有的子集，类似于括号生成的不断分支问题，看着答案手推代码会清晰很多；
            步骤：  1、所有的生成过程都是类似于裂变的构建过程，故而先弄清楚裂变的方法与条件（参考严蔚敏《数据结构》P150）；
                    （1）此问题裂变的过程是加入/不加入新的元素，裂变的条件无，即完全裂变；括号生成问题裂变的条件为左大于右；
                    （2）裂变的过程用递归控制，裂变的条件用条件语句if控制
                    2、弄清裂变的终止条件，即无法再发生裂变为止，遍历到深度最深的地方，一般用if语句计数判断，返回None终止递归；
                    3、一般来说裂变过程可看作类似并行、互不干扰的过程，故而结果result是在最终裂变结束的地方添加每个结果，
                       故而可设置全局self.result，在条件终止处添加每一个终止结果，如果手推代码会清晰很多；"""
        ###############################提供另一种迭代解法###########################################
        def subsets(nums):
            result = [[]]                   # 第一个解是空集
            for num in nums:                # 遍历所有的数依次添加
                for s in result[:]:         # 这里注意！！！用result会形成死循环的生成器，加了[:]则先计算再循环
                    current = s[:]          # 这里复制一下的原因是为了扩容而非原地添加
                    current.append(num)
                    result.append(current)
            return result
        #############################################################################################
        self.result = []
        self.nums = nums
        def DFS(subset, index):
            if index == len(self.nums):
                self.result.append(subset)
                return None
            DFS(subset+[self.nums[index]], index+1)
            DFS(subset, index+1)
        DFS([], 0)
        return self.result


    def permute(self, nums):
        """全排列问题：裂变过程，采用for遍历，但是只加入不重复的元素"""
        self.result = []
        N = len(nums)
        def DFS(nums, per):
            if len(per)==N:
                self.result.append(per)
            else:
                for i in range(len(nums)):
                    DFS(nums[:i]+nums[i+1:], per+[nums[i]])
        DFS(nums, [])
        return self.result

    def combine(self, n, k):
        """组合问题：输入[1,2,3,4]和2，返回所有升序的两个数的组合"""
        self.result = []
        def DFS(nums, com):
            if len(com)==k:
                self.result.append(com)
            else:
                for i in range(len(nums)):
                    DFS(nums[i+1:], com+[nums[i]])
        nums = [x+1 for x in range(n)]
        DFS(nums, [])
        return self.result

    def combinationSum(self, candidates, target):
        """组合总和问题：输入候选=[2,3,6,7]和总和=7，返回能求和的组合总数"""
        def DFS(target, comb, start):
            for i in range(start, len(candidates)):
                diff = target - candidates[i]
                if diff == 0:
                    self.result.append(comb+[candidates[i]])
                elif diff > 0:
                    DFS(diff, comb+[candidates[i]], i)
        self.result = []
        candidates.sort()
        DFS(target, [], 0)
        return self.result

    def eightQueens(self, n):
        """ 8皇后问题：记录一下踩过的坑
            1、 首先分裂过程很简单，以4皇后为例，1分4->4分16->16分64->64分256即终止，n皇后摆放完毕即终止；
            2、 剪枝规则，不能（1）同行（2）同列（3）同斜，首先摆放时按行依次摆放，即可满足条件（1）；
                接着条件（2）判定j1!=j2，条件（2）判定(i1-j1)!=(i2-j2),(i1+j1)!=(i2+j2)；
                满足终止条件则停止向下进展，否则则继续探索；
            3、 调试过程中出了许多bug，故而化繁为简，N皇后化简为4皇后，4皇后化简为2皇后；
                2皇后的条件为不同行（1）不同列（2），只有四种分裂情况，并且只有两种正确解法，手推画图都很简单；
                首先考虑DFS函数，按行依次摆放满足条件（1），在解空间中判定条件（2）来考虑是否递归，很快搞定了；
            4、 将4皇后的条件（3）加入判定后出了很多问题：
                首先是判定终止是跳出循环还是直接return跳出函数？递归是写在判定循环中还是判定循环外？
                结果发现都不行，最后想了想加入一个判定函数来解决，把判定条件打包都扔进去，返回bool类型，
                只要当前分支没有违背规则就继续执行，一旦违背规则也就终端这条路径，这样就很简单地处理了这个问题了。"""
        def DFS(index, sol):
            if index == n:
                self.result.append(sol)
            else:
                for i in range(n):
                    rowi = (index, i)
                    if judge(rowi, sol):
                        DFS(index + 1, sol + [rowi])

        def judge(rowi, sol):
            for j in sol:
                if rowi[1] == j[1] or (rowi[0]-rowi[1]) == (j[0]-j[1]) or (rowi[0]+rowi[1]) == (j[0]+j[1]):
                    return False
            return True

        self.result = []
        DFS(0, [])
        return self.result


if __name__ == "__main__":
    solution = BackTracking()
    print("生成括号:", solution.generateParenthesis(3))
    print("集合子集:", solution.subSet([1, 2, 3]))
    print("全排列:  ", solution.permute([1, 2, 3]))
    print("组合问题:", solution.combine(4, 2))
    print("组合总和问题:", solution.combinationSum([2, 3, 6, 7], 7))
    print("8皇后问题:", solution.eightQueens(4))
