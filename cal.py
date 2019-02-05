# -*- coding: utf-8 -*-
import cal
# def predict(pre):
#   aList=['0','1','X','3','4','5','6','7','8','9','(',')','2','/','+','-']
#   pression=""
#   p=[0]*15
#   for i,value in enumerate(pre):
#     if value=='1':
#       p[i]=i
#   for i,value in enumerate(pre):
#     if value=='1':
#       pression=pression+aList[i]
#   #print(pression)
#   return pression

import operator

class Stack:
    def __init__(self): 
        self.items = []
 
    def isEmpty(self):
        return self.items == []
 
    def push(self, item): 
        self.items.append(item)
 
    def pop(self):
        return self.items.pop()
 
    def peek(self):
        return self.items[len(self.items)-1]
 
    def size(self): 
        return len(self.items)
 
    
def postfix_calculate(s):
    stack = Stack()
    for x in s:
        if str(x).isdigit():
            stack.push(x)
        elif x == "+" and stack.size() > 1:
            a = stack.pop()
            b = stack.pop()
            stack.push(float(a)+float(b))
        elif x == "-" and stack.size() > 1:
            a = stack.pop()
            b = stack.pop()
            stack.push(float(b)-float(a))
        elif x == "X" and stack.size() > 1:
            a = stack.pop()
            b = stack.pop()
            stack.push(float(a)*float(b))
        elif x == "/" and stack.size() > 1:
            a = stack.pop()
            b = stack.pop()
            stack.push(float(b)/float(a))
        else :
            return '?'
    #print(stack.peek())
    return stack.peek()

def middle2behind(expression):  
    result = ()            # 结果列表
    stack = []             # 栈
    print(expression)
    item = 0
    while item < len(expression): 
        if expression[item].isnumeric():      # 如果当前字符为数字那么直接放入结果列表
            res = int(expression[item])
            while item+1 < len(expression) and expression[item+1].isnumeric() :
                item = item + 1
                res = res * 10 + int(expression[item])  
#            print(res,item)
#            result.append(res)
            result = result + tuple([res])
        else:                     # 如果当前字符为一切其他操作符
            if len(stack) == 0:   # 如果栈空，直接入栈
                stack.append(expression[item])
            elif expression[item] in 'X/(':   # 如果当前字符为*/（，直接入栈
                stack.append(expression[item])
            elif expression[item] == ')':     # 如果右括号则全部弹出（碰到左括号停止）
                if len(stack):
                    t = tuple(stack.pop())
                else:
                    return False
                while operator.eq(t[0],'(') == False:   
#                    result.append(t)
                    result = result + t
                    if len(stack):
                        t = tuple(stack.pop())
                    else:
                        return False
            # 如果当前字符为加减且栈顶为乘除，则开始弹出
            elif expression[item] in '+-' and stack[len(stack)-1] in 'X/':
                if stack.count('(') == 0:           # 如果有左括号，弹到左括号为止     
                    while stack:
#                        result.append(stack.pop())
                        if len(stack):
                            result = result + tuple(stack.pop())
                        else:
                            return False
                else:                               # 如果没有左括号，弹出所有
                    if len(stack):
                        t = tuple(stack.pop())
                    else:
                        return False
                    while operator.eq(t[0],'(') == False:
#                        result.append(t)
                        result = result + t
                        if len(stack):
                            t = (stack.pop())
                        else:
                            return False  
                    stack.append('(')
                stack.append(expression[item])  # 弹出操作完成后将‘+-’入栈
            else:
                stack.append(expression[item])# 其余情况直接入栈（如当前字符为+，栈顶为+-）
        item = item + 1

    # 表达式遍历完了，但是栈中还有操作符不满足弹出条件，把栈中的东西全部弹出
    while stack:
#        result.append(stack.pop())
        result = result + tuple(stack.pop())
    # 返回字符串
    #print(result)
    return result
#rs=middle2behind("(12+3)X5-1")
def cal(pre):
#pre=['0','1','1','0','0','0','0','0','0','0','0','0','1','0','0','0']
#rs=predict(pre)
  rs="(12+3)X5-1"
  rs=pre
  tp=middle2behind(rs)
  #print(tp)
  res = str(postfix_calculate(tp)) if (rs != False) else '?'
  #print(rs+ "="+ res)
  return rs+ " = "+ res


if __name__ == '__main__':
    ready_to_compute = '(1+3)X6'
    output_result = cal(ready_to_compute)
    print(output_result)
