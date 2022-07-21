#!/usr/bin/python
import datetime
import rospy
import pymongo
import operator
import traceback
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
    filter1 = {"ActionSequnceId": -1}
    simName = 'occupancyGrid2'
    if id % 2 == 0:
        simName = 'occupancyGrid1'
    belief = BeliefStates.find_one(filter1)
    map_width = belief["BeliefeState"][0]["map_width"]
    robX = belief["BeliefeState"][0]["robotGridLocX"]
    robY = belief["BeliefeState"][0]["robotGridLocY"]
    real = belief["BeliefeState"][0]["occupancyGrid"]
    sim = belief["BeliefeState"][0][simName]
    equal=True
    show_grid = real
    if not IS_REAL_OCCUPANCY:
        show_grid = sim
    for a in range(len(real)):
        equal = equal and real[a]==sim[a]
        print('index:',a, ', equal:', str(real[a]==sim[a]), ',total:',str(equal))

    return equal
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

def PrintMap(robX, robY, map_data):
    w = int(map_width)
    GREEN = '\033[32m'
    WHITE = '\033[37m'
    ONE = '\033[1;32;40m'
    TWO = ''
    a = ""
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

                    # a=a + str(get_map_cell(robY+ col -int(w/2),row)) + ','
                    a = a + color + '' + str(get_map_cell(col, row, map_data)) + ','
            if has:
                a = a + '\n'
        print(a)
#print(real)
id_to_print=1
while True:
    curId= getLastID()
    if curId > id_to_print:
        print("Print action ID:",curId)
        id_to_print = curId
        print(str(printByActionId(id_to_print)))

# printByActionId(4)