#!/usr/bin/python
# -*- coding: UTF-8 -*-


'''
author:navysummer
class：Sdbmhash
function:hash_sdbm
'''

class Sdbmhash(object):
    def __init__(self, strs):
        self.strs = strs

    # equ <<
    def int_overflow(self, val):
        maxint = 2147483647
        if not -maxint-1 <= val <= maxint:
            val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
        return val

    # equ >>>
    def unsigned_right_shitf(self, n, i):
        # 数字小于0，则转为32位无符号uint
        if n<0:
            n = ctypes.c_uint32(n).value
        # 正常位移位数是为正数，但是为了兼容js之类的，负数就右移变成左移好了
        if i<0:
            return -self.int_overflow(n << abs(i))
        return self.int_overflow(n >> i)
    
    # sdbm hash
    def hash_sdbm(self):
        hash = 0
        for i in range(len(self.strs)):
            hash = ord(self.strs[i]) + (self.int_overflow(hash << 6)) + (self.int_overflow(hash << 16)) -hash
        val = self.unsigned_right_shitf(hash,0)
        return val

        