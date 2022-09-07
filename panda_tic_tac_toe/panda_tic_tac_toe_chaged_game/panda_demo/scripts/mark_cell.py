#!/usr/bin/env python
import socket
import sys

import sys
from sys import exit
from panda_demo.srv import mark_cell, mark_cellResponse
import time
from datetime import datetime
import signal
import string

import os, time, signal, threading
import subprocess
from subprocess import Popen, PIPE, call


import roslib
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from subprocess import Popen, PIPE


def tcp_client_send_message(host, port,msg):
    was_sent=False
    sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('client connected')
    try:
        # Send data
        #print >> sys.stderr, 'sending "%s"' % msg
        sock.sendall(msg)

        data = sock.recv(1024)
    except Exception as e:
        print('Exception:',e)
    finally:
        print('closing socket')
        sock.close()
    return was_sent


def mark_cb(req):
    HOST = "132.72.96.57"#socket.gethostbyname("localhost")
    PORT = 1770
    message = 'write_o' + ' ' + req.cell
    print('Sending message to robot (HOST:',HOST,'PORT:',PORT,'), message:\'',message,'\'')

    tcp_client_send_message(HOST, PORT,message.encode())
 
 
if __name__ == "__main__":
    rospy.init_node('mark_tic_tac_toe_cell')
    s = rospy.Service('mark_tic_tac_toe_cell_service', mark_cell, mark_cb)
    print("Ready to mark tic-tac-toe cell!")
    rospy.spin()
 
    #rospy.init_node('mark_tic_tac_toe_cell', anonymous=True)
    try:
      rospy.spin()
    except:
      print("Shutting down")
 
