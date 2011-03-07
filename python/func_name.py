#!/usr/bin/env python

import sys

def test():
    print __name__
    print sys._getframe().f_code.co_name

test()
