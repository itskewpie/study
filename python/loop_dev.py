#!/usr/bin/env python

import commands

command = "/sbin/losetup -a"
(ret,output) = commands.getstatusoutput(command)

print ret
print output

if output == "":
    dev = "loop0"
else:
    pass
    


print dev
