# -*- coding: UTF-8 -*-

'''
      32-47:空格 ! " # $ % & ' ( ) * + , - . /
      48-57:0-9
      58-64:: ; < = > ? @
      65-90:A-Z
      91-96:[ 反斜杠 ] ^ _ ` 
      97-122:a-z
      123-126:{ | } ~
'''
import itertools
import random
from scipy.special import comb, perm

'''
这个方法比较方便快捷，但是比较消耗内存，内存不大，会内存溢出
'''
def products(length=5):
	chars=''.join([chr(i) for i in range(32,127)])
	for i in itertools.product(chars, repeat = length):
		string = ''.join(i)
		print(string)
'''
这个方法运行速度快，但是容易遗漏
'''
def random_str(code_len=5):
    chars=''.join([chr(i) for i in range(32,127)])
    code_count=int(comb(len(chars),code_len))
    count= 0
    while count < code_count:
        checkcode= ''
        for i in range(code_len):
            j=random.randint(0,len(chars)-1)
            checkcode+= chars[j]
        print(checkcode)
        count+=1
'''
这个方法综合前两种，内存消耗不大，运行速度一般
'''
def sub_list(length=5):
    chars = [chr(j) for i in range(length) for j in range(32,127)]
    for i in range(1 << len(chars)):
        combo_list = []
        for j in range(len(chars)):
            if i & (1 << j):
                combo_list.append(chars[j])
        sub_list_len = len(combo_list)
        if sub_list_len != length: 
            continue
        else:
            sub_str = ''.join(combo_list)
            print(sub_str)

def main():
	products()
    random_str()
    sub_list()

if __name__ == '__main__':
    main()

    
