#coding:utf-8
import random, string

def make_point():
    return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(39))

