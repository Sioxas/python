# -*- coding: utf-8 -*-
def g():
    a=0
    while True:
        a+=1
        a = yield a
        print 'g:%d' % (a)


it = g()
print it.next()
print it.send(5)
print it.send(10)
print it.send(-1)
