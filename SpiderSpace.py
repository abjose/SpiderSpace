from SpiderLib import *
import numpy as np
import random as r

w,h = 512,512
web = InitWeb(w,h)
#web[256,256] = [100,255,100]

ID = [0,255,0]
#start = (60, 100)
#end = (100, 10)
#web, pos = DrawLine(start, end, web, ID)
#print pos

spider = (10,10)
#MakeThread((1,10 ),0,web,ID)

'''
for i in range(0, 1500):
	angle = r.randrange(0,360)
	spider = (r.randrange(0,512),r.randrange(0,512))
	ID = [r.randrange(0,255),r.randrange(0,255),r.randrange(0,255)]
	#angle = i
	web, pos = MakeThread(spider,angle,web,ID)
	#web, pos = MakeThread((1,i), 0, web, [0, 255-i,0])

DisplayWeb(web, "web4")
radius = 80

for i in range(0,10):
	web,points = ThrowItem(web)
	print points
#threads = CountThreads (spider, radius, web)
#print threads


angle = -45
spider = 10,10
ID = [0,255,255]
web, pos, dist = MakeThread(spider,angle,web,ID)
print dist

dist = 50
pos,endDist = MoveDownLeft(spider,web,dist)
print 'one way:'
print pos
print endDist
pos,endDist = MoveUpRight(spider,web,dist)
print 'the other:'
print pos
print endDist

a = GetNewAlg()
print a

DisplayWeb(web, "web6")
'''

steps = 2500
alg = GetNewAlg()

#alg = [['w',127],['mur',30],['w',36],['mdl',200]]
#print alg
web,points = EvalSpider(alg,steps,1)
#print points
DisplayWeb(web, "webExample4")


#EvolvePopulations(50,50)