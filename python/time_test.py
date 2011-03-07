#!/usr/bin/env python

import time
import datetime


t1 = int(time.time())
time.sleep(10)
t2 = int(time.time())

diff = datetime.timedelta(seconds=t2-t1)
print diff

