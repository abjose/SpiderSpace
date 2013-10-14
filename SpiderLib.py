import random
import math
import Image
import numpy as np
import random as r
import copy



# ALGORITHM EVOLUTION #

def EvolveAlgorithm (arr):
	
	# Passed an array-algorithm, changes elements based on local
	#	probabilities
	# Passes elements to external EvolveComponent, which may either delete,
	#	modify, or add extra actions
	newAlg = []
	
	for n in range(len(arr)):
		# pop, evolve, and replace
		newAction = EvolveComponent([arr[n]])
		for action in newAction:
			newAlg.append(action)
		
	return newAlg
		
def EvolveComponent (list):
	# Passed list of tuples (algorithm components), potentially modifies them
	#	in the following ways:
	#	  - Delete action   (deletes action and arg entirely)
	#	  - Change argument (arg changed like gaussian of previous)
	#	  - Add    action   (insert another action with random valid arg)
	
	# modification probabilities (will modify if var > random number):
	chgProb = .12
	delProb = .02
	addProb	= .08
	
	# ugly and hardcoded...use a function-calling dictionary? or list?
	# only justification is that there probably won't be other actions...
	
	#potentially change arg
	if (r.random() < chgProb):
		#print "modified action!"
		list.append(GetAction(list.pop()))
	
	#potentially delete:
	if (r.random() < delProb):
		#print "deleted action!"
		list.pop()		# can assume only action is last action
		
	#potentially add
	if (r.random() < addProb):
		#print "added action!"
		list.append(GetAction(None))
	
	return list	
	
def GetAction (currAct):
	# Argument is potential action list (i.e. word and argument)
	# If an argument is passed, returns that action w/ new argument from gaussian
	# Else returns a tuple defining a new, valid action based on below definitions
	
	actions	= ['mur', 'mdl', 'w']	# list of allowable arguments
	#actions	= ['w']
	rules 	= [500, 500, 360]	# max vals for above actions
	
	if currAct == None:
		actIndex 	= math.trunc(len(actions) * r.uniform(0, .999))
		chosenAct 	= actions[ actIndex ]
		chosenArg	= math.trunc(rules[ actIndex ] * r.random())
	else:
		chosenAct = currAct[0]
		chosenArg = GetGaussian(currAct[1])
	
	return [chosenAct, chosenArg]	
	
def GetGaussian (num):
	# Returns a pseudorandom number following a gaussian distribution around num
	
	sd = num*.25	# standard deviation of gaussian is 1/4 arg...
	return math.trunc(r.gauss(num, sd))
	
def GetNewAlg ():
	# return a new semirandom algorithm
	
	initialEvolution = 40
	
	arr = [GetAction(None),GetAction(None),GetAction(None),GetAction(None)]
	for i in range(0,initialEvolution):
		arr = EvolveAlgorithm(arr)
	
	return arr

	
# WEB BUILDING AND MODIFICATION #

def InitWeb (w, h):
	# makes and returns a new web array of size w by h
	#  web initially a 2-d array of black rgb tuples

	data = np.zeros( (w,h,3), dtype=np.uint8)
	return data

def DisplayWeb (web, name):
	# converts a web to a .png and saves it as name.png
	img = Image.fromarray(web)
	name = 'images/' + name + '.png'
	img.save(name)

def DrawLine ((x,y), (x2,y2), web, ID):
	# STOLEN FROM: 
	# http://snipplr.com/view.php?codeview&id=22482
	# But similar to (in case that link dies):
	# http://rosettacode.org/wiki/Bitmap/Bresenham's_line_algorithm
	# passed start and end coordinate tuples, a web to draw in, and an ID to draw
	#  draws a line of IDs in the web from one point to your mother
	#  UNLESS it intersects another line...
	xMax,yMax,depth = web.shape
	xMax -= 2
	yMax -= 2
	steep = 0
	zero = [0,0,0]
	currID = [web[x,y][0],web[x,y][1],web[x,y][2]]
	pos = -1,-1
	dx = abs(x2 - x)
	if (x2 - x) > 0: sx = 1
	else: sx = -1
	dy = abs(y2 - y)
	if (y2 - y) > 0: sy = 1
	else: sy = -1
	if dy > dx:
		steep = 1
		x,y = y,x
		dx,dy = dy,dx
		sx,sy = sy,sx
	d = (2 * dy) - dx
	for i in range(0,dx+1):
		if steep:
			broken = not np.array_equal(zero, web[y,x]) and not np.array_equal(currID, web[y,x]) 
			web[y,x] = ID
			pos = y,x
			if broken:
				break
		else: 
			broken = not np.array_equal(zero, web[x,y]) and not np.array_equal(currID, web[x,y]) 
			web[x,y] = ID
			pos = x,y
			if broken:
				break
		while d >= 0 and y < yMax:
			y = y + sy
			# begin modified - so 8-way connected...if undesired, delete
			if steep:
				broken = not np.array_equal(zero, web[y,x]) and not np.array_equal(currID, web[y,x]) 
				web[y,x] = ID
				pos = y,x
				if broken:
					break
			else:
				broken = not np.array_equal(zero, web[x,y]) and not np.array_equal(currID, web[x,y]) 
				web[x,y] = ID
				pos = x,y
				if broken:
					break
			# end modified
			d = d - (2 * dx)
		x = x + sx
		d = d + (2 * dy)
	return web, pos
	
def MakeThread (pos, web, angle, ID):
	# passed position tuple, absolute angle, web data array, and ID
	#  draws line passing through pos
	#  and constrained to edges of web
	
	# NOTE: something is fucked up when near the edge - like for (0,0), 180,
	#  has different result from (0,1), 180...
	
	angle = angle % 360	# just go with it...
	
	initX,initY = pos
	# web bounds
	xMin, yMin = 1,1
	xMax, yMax, depth = web.shape
	xMax -= 2
	yMax -= 2
	# spider location
	currX, currY = pos
	xInt,yInt = 0,0
	
	# this is a terribly ugly way to do this
	if angle == 0:
		xInt = xMax
		yInt = currY
	elif angle == 90:
		xInt = currX
		yInt = yMin
	elif angle == 180:
		xInt = xMin
		yInt = currY
	elif angle == 270:
		xInt = currX
		yInt = yMax
	else:
		tan = math.tan(math.radians(angle))
		quad = angle / 90 + 1
		if quad == 1:
			xInt = currX + currY/tan
			yInt = currY - (xMax - currX)*tan
		elif quad == 2:
			xInt = currX + currY/tan
			yInt = currY + currX*tan
		elif quad == 3:
			xInt = currX - (yMax - currY)/tan
			yInt = currY + currX*tan
		else:	#if quad == 4
			xInt = currX - (yMax - currY)/tan
			yInt = currY - (xMax - currX)*tan
		
	xInt = max(xMin, xInt)
	yInt = max(yMin, yInt)
	
	xInt = min(xInt, xMax)
	yInt = min(yInt, yMax)
	
	xInt = int(round(xInt))
	yInt = int(round(yInt))
	
	#print (xInt, yInt)
		
	web, pos = DrawLine(pos, (xInt,yInt), web, ID)
	x,y = pos
	
	finalDist = int(math.sqrt(abs(initX - x)**2 + abs(initY - y)**2))
	
	return web, pos, finalDist
	
def CountThreads (pos, web, radius):
	# count the number of threads in a space centered at loc
	#  in a square with side length side
	
	IDList = []
	zero = [0,0,0]
	
	xMax,yMax,depth = web.shape
	x,y = pos
	xMax -= 2
	yMax -= 2
	
	x1 = x - radius/2
	y1 = y - radius/2
	
	x2 = x1 + radius
	y2 = y1 + radius
	
	x1 = max(x1, 0)
	y1 = max(y1, 0)
	
	x2 = min(x2, xMax)
	y2 = min(y2, yMax)
	
	for i in range(x1, x2):
		for j in range(y1, y2):
			if not np.array_equal(zero, web[i,j]):
				# bullshitty fix
				tempList = [web[i,j][0],web[i,j][1],web[i,j][2]]
				try:
					IDList.index(tempList)
				except ValueError:
					IDList.append(tempList)
					
	return len(IDList)

def BreakThread (pos, web):
	# should have pos and ID, or just ID, instead of pos?
	# given position, checks ID - if non-zero, flood fills through rest of 
	#  thread and replaces with zeros
	
	x,y = pos
	xMax,yMax,depth = web.shape
	zero = [0,0,0]
	
	if not np.array_equal(zero, web[x,y]):
		blacklist = []
		blacklist.append(pos)
		ID = [web[x,y][0],web[x,y][1],web[x,y][2]]
		
		# only need to do four direction because lines are 4-way connective...
		# also feeling lazy
		while len(blacklist) > 0:
			x,y = blacklist.pop()	# get next spot
			web[x,y] = zero			# blacken
			# and check surroundings...inelegantly... Should short circuit.
			if 	InBound((x+1,y), web) and np.array_equal(web[x+1,y], ID):
				blacklist.append((x+1,y))
			if 	InBound((x-1,y), web) and np.array_equal(web[x-1,y], ID):
				blacklist.append((x-1,y))
			if 	InBound((x,y+1), web) and np.array_equal(web[x,y+1], ID):
				blacklist.append((x,y+1))
			if 	InBound((x,y-1), web) and np.array_equal(web[x,y-1], ID):
				blacklist.append((x,y-1))
	return web

def InBound (pos, web):
	# checks to see if pos is inside web's boundaries
	xMin,yMin = 1,1
	xMax,yMax,depth = web.shape
	xMax -= 2
	yMax -= 2
	x,y = pos
	
	if xMin <= x < xMax:
		if yMin <= y < yMax:
			return True
	
	return False
	
def BreakThreadGroup(loc, radius, web):
	# same argument as CountThreads for ease of use
	#  breaks all the threads in a specific square
	xMin,yMin = 1,1
	xMax,yMax,depth = web.shape
	xMax -= 2
	yMax -= 2
	x,y = loc
	
	x1 = x - radius/2
	y1 = y - radius/2
	
	x2 = x1 + radius
	y2 = y1 + radius
	
	x1 = max(x1, xMin)
	y1 = max(y1, yMin)
	
	x2 = min(x2, xMax)
	y2 = min(y2, yMax)
	
	for i in range(x1, x2):
		for j in range(y1, y2):
			BreakThread((i,j),web)
					
	return web
	
def GetID (IDList):
	# generates valid ID not in use, returns ID and new IDList
	
	zero = [0,0,0]
	ID = zero
	valid = 0
	
	while valid == 0:
		ID = zero
		while ID == zero:
			# make sure it's semi-visible...red biased
			# so IDs with r value below 100 are 'reserved' (can be used elsewhere)
			ID = [r.randrange(100,255),r.randrange(0,255),r.randrange(0,255)]
		try:
			IDList.index(ID)
		except ValueError:
			IDList.append(ID)
			valid = 1
			
	return ID, IDList

def ThrowFood (web):
	# throws food onto a random location on the spider web
	#  returns web and point value (0 if breaks through)
	points = 0
	xMin,yMin = 1,1
	xMax,yMax,depth = web.shape
	xMax -= 2
	yMax -= 2
	minFood = 5
	maxFood = 25
	radiusMultiplier = 3
	weightDivisor = 3	# radius/divisor = number threads necessary to catch...?
	
	x,y = r.randrange(xMin,xMax), r.randrange(yMin,yMax)
	foodRadius = radiusMultiplier * r.randrange(minFood,maxFood)
	# point value = foodRadius for now
	
	# break if web not strong enough, otherwise add points
	if CountThreads((x,y), web, foodRadius) >= int(foodRadius/weightDivisor):
		points = foodRadius^2	# play with this value!
	else:
		web = BreakThreadGroup((x,y), foodRadius, web)
	
	return web, points

def ThrowRock (web):
	# throw a rock - bounces off if web strong enough, break through otherwise
	#  returns web and points (always 0)
	
	web,points = ThrowFood(web)
	
	return web, 0

def ThrowItem (web):
	# randomly decides if and what to throw
	#  returns web and points
	#  probability set to 1 for 'two stage' model, should lower for simultaneous
	#  building and throwing
	
	points = 0
	throwChance = 1.0
	rockChance = 0.2
	
	# throw anything?
	if r.random() < throwChance:
		#throw rock?
		if r.random() < rockChance:
			web,points = ThrowRock(web)
		else:
			web,points = ThrowFood(web)
	
	return web,points


# SPIDER MOVEMENT AND STUFF

def MoveUpRight (pos, web, dist):
	# only tries to move up or right (up,right are...relative)
	xMax,yMax,depth = web.shape
	xMax -= 2
	yMax -= 2
	zero = [0,0,0]
	prevPos = (-1,-1)
	initDist = dist
	
	while prevPos != pos and dist > 0:
		x,y = pos
		x1 = x+1 
		y1 = y+1
		dist -= 1
		prevPos = pos
		
		if x1 < xMax:
			if not np.array_equal(zero, web[x1,y]):
				pos = (x1,y)
		if y1 < yMax:
			if not np.array_equal(zero, web[x,y1]):
				pos = (x,y1)
	
	totalDist = initDist - dist
	return pos,totalDist

def MoveDownLeft (pos, web, dist):
	# only tries to move down or left (down/left are...relative, but different from
	#  up/right)
	xMin,yMin = 1,1
	zero = [0,0,0]
	prevPos = (-1,-1)
	initDist = dist
	
	while prevPos != pos and dist > 0:
		x,y = pos
		x1 = x-1 
		y1 = y-1
		dist -= 1
		prevPos = pos
		
		if x1 >= xMin:
			if not np.array_equal(zero, web[x1,y]):
				pos = (x1,y)
		if y1 >= yMin:
			if not np.array_equal(zero, web[x,y1]):
				pos = (x,y1)
	
	totalDist = initDist - dist
	return pos,totalDist

def DoAction (action, web, pos, IDList):
	# given an action array...does the associated action
	#  returns web, new spider position, action time consumption, and IDList
	
	time = 0
	
	if action != None:
		act = action[0]
		arg = action[1]
		
		# make sure to update these if the actions change (see GetAction)
		if act == 'mur':
			# move up'n'right
			pos,time = MoveUpRight(pos, web, arg)
		elif act == 'mdl':
			# move down'n'left
			pos,time = MoveDownLeft(pos, web, arg)
		elif act == 'w':
			# shoot web
			ID,IDList = GetID(IDList)
			web,pos,time = MakeThread(pos, web, arg, ID)
			
	return web,pos,time,IDList

def InsertCross (web,pos):
	# UNTESTED
	# inserts a cross at the given position
	#  know things with red value below 100 are 'reserved'...
	
	color1 = [100,255,255]
	color2 = [99,255,255]
	color3 = [98,255,255]
	color4 = [97,255,255]
	
	web,newPos,finalDist = MakeThread(pos,web,0,color1)
	web,newPos,finalDist = MakeThread(pos,web,0,color2)
	web,newPos,finalDist = MakeThread(pos,web,0,color3)
	web,newPos,finalDist = MakeThread(pos,web,0,color4)
	
	return web

# POPULATION MANAGEMENT STUFF

def GeneratePopulation (size):
	# creates a list of web algorithms of the given length
	
	pop = []
	
	for i in range(0,size):
		pop.append(GetNewAlg())
		
	return pop

def EvalSpider (alg, steps, avg):
	# returns score of the given algorithm
	#  Generate a new web, spawn the spider in the middle?
	#  avg is the number of times we try throwing stuff at the initial web
	
	webEdge = 500
	initPos = webEdge/2
	startThrow = steps/2
	zero = [0,0,0]
	
	web = InitWeb(webEdge,webEdge)
	pos = initPos,initPos
	pause = 0
	dead = 0
	index = 0
	points = 0
	throws = 10
	IDList = []
	
	
	# commented out build-and-throw model, now two-stage
	while steps > 0:
		steps -= 1
		pause -= 1
		
		#if steps < startThrow:
			#print 'threw something!'
			#web,tempPoints = ThrowItem(web)
			#points += tempPoints
		
		#if pause <= 0:
		if True:
			print 'did action ' + str(steps)
			web,pos,pause,IDList = DoAction(alg[index],web,pos,IDList)
			index = (index+1) % len(alg) 
		else:
			print 'waited'
		
		#x,y = pos
		#if np.array_equal(zero, web[x,y]):
		#	print 'spider died! :('
		#	points -= 10
		#	break	# SPIDER DIE!
		
	for i in range(0,avg):
		webCopy = copy.copy(web)	# so that we can see un-broken web
		tempThrows = throws
		while tempThrows > 0:
			print 'did throw ' + str(tempThrows)
			tempThrows -= 1
			webCopy,tempPoints = ThrowItem(webCopy)
			points += tempPoints
			
	#DisplayWeb(webCopy, 'thrownWeb')
	#raw_input("Press Enter to continue...")
	
	return web,int(points/avg)

def TestPopulation (pop, top, steps, simsPer, children):
	# given a list of algorithms (pop) and a 'success limit' (top), the number of
	#  times to test each algorithm (simsPer) and the number of children each
	#  algorithm should generate (children), will generate a new list of 
	#  len(pop) * children + len(pop) (to account for initial adults being included)
	#  and then run EvalSpiderAvg(alg,steps,simsPer) on each algorithm, aggregating
	#  the best in an array of max length (top)
	
	# generate mutant population
	mutantPop = []
	for alg in pop:
		mutantPop.append(alg)
		for i in range(0,children):
			mutantPop.append(EvolveAlgorithm(alg))
	
	# now evaluate entire mutant population, accumulate top best
	bestList = []
	for alg in mutantPop:
		web,score = EvalSpider(alg,steps,simsPer)
		spiderTuple = (alg,score)
		bestList.append(spiderTuple)
		if len(bestList) > top:
			# sort by score and take off worst one
			bestList = sorted(bestList, key=lambda spider: spider[1], reverse=True)
			bestList.pop()	# sorry bro
			
	# should probably use list comprehension here...
	returnPop = []
	for spider in bestList:
		returnPop.append(spider[0])	# append spider's algorithm
	
	return returnPop

def EvolvePopulations (popSize, gens):
	pop = GeneratePopulation(popSize)
	top = 15
	steps = 2500
	simsPer = 5
	children = 10
	
	for i in range(0,gens):
		print 'ON GENERATION ' + str(i)
		pop = TestPopulation(pop,top,steps,simsPer,children)
		
	# then display the best...
	i = 1
	for alg in pop:
		name = 'best_' + str(i)
		web,points = EvalSpider(alg, steps, simsPer)
		DisplayWeb(web,name)
		i += 1
		
	return None
	
# to help count down remaining spiders...
#  know exactly how many there will be, so just print "x of y" before simulating?
#  also, could save images every certain number of times...although would take time
#  (could just be every generation...always save top best?)

# should also add small population of 'new' algorithms each generation?