#!/usr/bin/env python
#

import snmp
#import pysnmp as snmp


def Main(sess, oids):
    top = map(sess.mibnode, oids)
    next = top
    while 1:
	if not next: break
	next =  sess.getnext(next)
	indices = range( len(next) )
	indices.reverse()
	for i in indices:
	    T,V = top[i], next[i]
	    if snmp.issuboid(T, V):
		print V.oid[-45:], ":", V.value
	    else:
		del top[i], next[i]
    return
#
# The rest is just command line processing
#
if __name__ == "__main__":
    import sys
    Usage = "Usage: " + sys.argv[0] + " hostname [-c community] oid[...]"
    community = "public"

    # start by looking for the -community option
    for i in range(len(sys.argv)):
	A = sys.argv[i]
	if A[0:2] == "-c":
	    try:
		del sys.argv[i]
		community = sys.argv[i]
		del sys.argv[i]
	    except:
		print Usage
		sys.exit(1)
	    break

    if len(sys.argv) == 1:
	print Usage
	sys.exit(1)
    elif len(sys.argv) == 2:
	sys.argv.append(".iso")

    Main( snmp.open(sys.argv[1], community), sys.argv[2:])
    try:
	Main( snmp.open(sys.argv[1], community), sys.argv[2:])
    except snmp.SnmpError, msg:
	print "Sorry, SNMP error:",msg
    except ValueError, msg:
	print "Sorry!", msg
