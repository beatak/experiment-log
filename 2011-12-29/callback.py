#!/usr/bin/env python

import sys, os, logging

logger = logging.getLogger('python-callback')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logpath = os.path.expanduser('~/Library/Logs/python-callback.log')
if os.path.isfile(logpath) == False:
    open(logpath, 'w').close()
mylog = logging.FileHandler(logpath)
mylog.setFormatter(formatter)
logger.addHandler(mylog)
logger.setLevel(logging.INFO)

logger.info('callback! ')
logger.info(sys.argv)
