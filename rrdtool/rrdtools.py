#!/usr/bin/env python

import time
import rrdtool
from subprocess import *

class RRDTool:

    def create(self,rrd_name):
	option1 = "--step"
	option2 = "5"
	DS = "DS:cpu:GAUGE:30:0:100"
	RRA1 = "RRA:AVERAGE:0.5:1:6"
	RRA2 = "RRA:MIN:0.5:1:6"
	RRA3 = "RRA:MAX:0.5:1:6"
	rrdtool.create(rrd_name,option1,option2,DS,RRA1,RRA2,RRA3)

    def update(self,rrd_name,value):
	data = "N:%s" %value
	rrdtool.update(rrd_name,data)

    def graph(self,graph_name,rrd_name,start,end):
	op1 = "--start"
	op2 = "--end"
	op3 = "--step"
	op4 = "--lower-limit"
	op5 = "--upper-limit"
	op6 = "DEF:load=aaa.rrd:cpu:AVERAGE"
	op7 = "LINE2:load#FF0000"
	rrdtool.graph(graph_name,op1,start,op2,end,op3,"5",
	op4,"0",op5,"1",op6,op7)


if __name__ == '__main__':
    rrd = RRDTool()
    rrd_name = "test.rrd"
    s_time = int(time.time())
    rrd.create(rrd_name)
    command = "snmpwalk -v 1 -c itskewpie localhost .1.3.6.1.4.1.2021.10.1.3.1|awk '{print $4}'" 

    process = Popen(command,shell=True,stdout=PIPE,stderr=PIPE)
    print process.stdout.readlines()
    """
    i = 0
    while 1 < 6:
	process = Popen(command,shell=True,stdout=PIPE,stderr=PIPE)
	value = process.stdout.readlines()
	rrd.update(rrd_name,value)
	i += 1
	time.sleep(5)


    e_time = int(time.time())

    rrd.graph("test.png",rrd_name,s_time,e_time)

	
    """ 
    pass
