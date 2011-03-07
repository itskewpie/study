#!/usr/bin/env python

import time
import rrdtool
from subprocess import *

class RRDTool:

    def create(self,rrd_name):
	rrd_name = "test.rrd"
	option1 = "--step"
	option2 = "5"
	DS = "DS:cpu:GAUGE:30:0:100"
	RRA1 = "RRA:AVERAGE:0.5:1:6"
	RRA2 = "RRA:MIN:0.5:1:6"
	RRA3 = "RRA:MAX:0.5:1:6"
	argv = list()
	argv.append(rrd_name)
	argv.append(option1)
	argv.append(option2)
	argv.append(DS)
	argv.append(RRA1)
	argv.append(RRA2)
	argv.append(RRA3)
	rrdtool.create(argv)

    def update(self,rrd_name,value):
	rrd_name = "test.rrd"
	data = "N:21"
	argv = list()
	argv.append(rrd_name)
	argv.append(data)
	rrdtool.update(argv)

    def graph(self,graph_name,rrd_name,start,end):
	argv = list()
	argv.append(graph_name)
	argv.append("--start")
	argv.append(start)
	argv.append("--end")
	argv.append(end)
	argv.append("--step")
	argv.append("--lower-limit")
	argv.append("0")
	argv.append("--upper-limit")
	argv.append("1")
	argv.append("DEF:load=aaa.rrd:cpu:AVERAGE")
	argv.append("LINE2:load#FF0000")
	rrdtool.graph(argv)



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
