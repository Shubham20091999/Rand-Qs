from random import randint
from math import log2,ceil

#Another question
# -> Given A uniform boolean generator make a non uniform boolean generator
#       -> e.g. given 50-50 generator make 20-80 generator

#Raandom Boolean generator
def getRandBool() -> bool:
    return [False,True][randint(0,1)]

#Random number generator if uplim=2**pow
def randpow2(pow):
    ret = 0
    for _ in range(pow):
        ret = ret << 1
        ret += getRandBool()
    return ret

#Random nnumber generator between 0 and n-1 inclusive
def randn(n):
    pow=ceil(log2(n))
    ret = randpow2(pow)
    while ret>=n:
        ret = randpow2(pow)
    return ret


print(randn(4))

