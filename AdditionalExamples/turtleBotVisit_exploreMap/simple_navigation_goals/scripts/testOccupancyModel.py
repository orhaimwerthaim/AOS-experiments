#!/usr/bin/python
import datetime
import rospy
import pymongo
import operator
import traceback
import time
from geometry_msgs.msg import Point, Pose
from simple_navigation_goals.srv import move, moveResponse
from nav_msgs.msg import OccupancyGrid
import sys

IS_REAL_OCCUPANCY = True
if len(sys.argv)>1:
    if sys.argv[1].lower()=='sim':
        IS_REAL_OCCUPANCY=False

if IS_REAL_OCCUPANCY:
    print('printing real occupancy grid')
else:
    print('printing simulated occupancy grid')

aosDbConnection = pymongo.MongoClient("mongodb://localhost:27017/")
aosDB = aosDbConnection["AOS"]
BeliefStates = aosDB["BeliefStates"]

filter1 = {"ActionSequnceId": 4}

# belief = BeliefStates.find_one(filter1)

# real = belief["BeliefeState"]["occupancyGrid"]
# realSim = belief["BeliefeState"]["occupancyGrid2"]

map_width=None
def printByActionId(id):
    global map_width
    filter1 = {"ActionSequnceId": id}
    belief = BeliefStates.find_one(filter1)
    simName = 'occupancyGrid2'
    if id % 2 == 0:
        simName = 'occupancyGrid1'
    map_width = belief["BeliefeState"][0]["map_width"]
    robX = belief["BeliefeState"][0]["robotGridLocX"]
    robY = belief["BeliefeState"][0]["robotGridLocY"]
    real = belief["BeliefeState"][0]["occupancyGrid"]
    sim = belief["BeliefeState"][0][simName]
    orientation = belief["BeliefeState"][0]["orientation"]

    if IS_REAL_OCCUPANCY:
        PrintMap(robX, robY, real, orientation)
    else:
        PrintMap(robX, robY, sim, orientation)
def getLastID():
    tried_id=0
    foundId=0
    while True:
        filter1 = {"ActionSequnceId": tried_id}
        belief = BeliefStates.find_one(filter1)
        if belief is not None:
            foundId=tried_id
            tried_id=tried_id+1
        else:
            return foundId



def get_map_cell(x,y, map_data):
    return map_data[int(x+y*map_width)]

def PrintMap(robX, robY, map_data, orientation): 
    print('orientation:',orientation)
    w = int(map_width)
    GREEN = '\033[32m'
    WHITE = '\033[37m'
    ONE = '\033[1;32;40m'
    Blue = "\033[0;34m"
    TWO = ''
    a = ""
    orX = robX
    orY = robY
    if orientation < 135 and orientation > 45:#forward
        orY = orY+1
    if orientation < 45 and orientation > -45:#right        
        orX = orX+1
    if orientation < -45 and orientation > -135:#backwards        
        orY = orY-1
    if orientation < -135 or orientation > 135:#left        
        orX = orX-1

    print('robX:' + str(robX) + ',robY:' + str(robY))
    if True:
        for row in range(w, -1, -1):
            has = False
            for col in range(w):
                color = WHITE
                # print('abs(col-robX):'+str(abs(col-robX)) + ', abs(row-robY):'+str(abs(row-robY)))
                if abs(col - robX) < 50 and abs(row - robY) < 50:
                    has = True
                    color = GREEN
                    if abs(col - robX) < 2 and abs(row - robY) < 2:
                        color = WHITE
		    if abs(col - orX) < 1 and abs(row - orY) < 1:
                        color = Blue

                    # a=a + str(get_map_cell(robY+ col -int(w/2),row)) + ','
                    a = a + color + '' + str("{0:03}".format(get_map_cell(col, row, map_data))) + ','
            if has:
                a = a + '\n'
        print(a)
#print(real)
id_to_print=1
while True:
    curId= getLastID()
    if curId > id_to_print:
	time.sleep(0.5)
        print("Print action ID:",curId)
        id_to_print = curId
        printByActionId(id_to_print)

# printByActionId(4)
