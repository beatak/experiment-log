#!/usr/bin/env python

import sys, os
def daemonize (stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    # Perform first fork.
    try:
        pid = os.fork( )
        if pid > 0:
            sys.exit(0) # Exit first parent.
    except OSError, e:
        sys.stderr.write("fork #1 failed: (%d) %sn" % (e.errno, e.strerror))
        sys.exit(1)
    # Decouple from parent environment.
    os.chdir("/")
    os.umask(0)
    os.setsid( )
    # Perform second fork.
    try:
        pid = os.fork( )
        if pid > 0:
            sys.exit(0) # Exit second parent.
    except OSError, e:
        sys.stderr.write("fork #2 failed: (%d) %sn" % (e.errno, e.strerror))
        sys.exit(1)
    # The process is now daemonized, redirect standard file descriptors.
    for f in sys.stdout, sys.stderr: f.flush( )
    si = file(stdin, 'r')
    so = file(stdout, 'a+')
    se = file(stderr, 'a+', 0)
    os.dup2(si.fileno( ), sys.stdin.fileno( ))
    os.dup2(so.fileno( ), sys.stdout.fileno( ))
    os.dup2(se.fileno( ), sys.stderr.fileno( ))

# =======================================

from fsevents import Observer, Stream
import subprocess, logging, string

project_name = 'directory_monitor'
logger = logging.getLogger(project_name)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
callback_script = False

def file_event_callback(event):
    logger.info('Mask: %s, Cookie: %s, Name: %s' % (event.mask, event.cookie, event.name))
    proc = subprocess.Popen([callback_script, str(event.mask), str(event.name)])
    proc.wait()

def normalize_path(str):
    if string.find(str, '~') == 0:
        result = os.path.expanduser(str)
    elif string.find(str, '/') == 0:
        result = str
    else :
        result = os.path.abspath( os.getcwd() + '/' + str )
    return result

def main():
    if len(sys.argv) != 3:
        sys.stderr.write('Usage: self PATH_TO_WATCH CALLBACK_SCRIPT')
        sys.exit(1)
    #path
    path = normalize_path(sys.argv[1].encode())
    #callback_script
    global callback_script
    callback_script = normalize_path(sys.argv[2].encode())

    if os.path.isdir(path) == False:
        sys.stderr.write ('%s does not exists.' % (path) )
        sys.exit(1)
    if os.path.isfile(callback_script) == False:
        sys.stderr.write('%s does not exists.' % (callback_script) )
        sys.exit(1)

    pid = os.getpid()
    logpath = os.path.expanduser('~/Library/Logs/%s-%d.log' % (project_name, pid))
    if os.path.isfile(logpath) == False:
        open(logpath, 'w').close()
    mylog = logging.FileHandler(logpath)
    mylog.setFormatter(formatter)
    logger.addHandler(mylog)
    logger.setLevel(logging.INFO)

    print('Log path is %s' % (logpath) )
    logger.info('%s started' % (project_name))
    logger.info('watching %s and will excute %s' % (path, callback_script) )

    observer = Observer()
    observer.start()
    stream = Stream(file_event_callback, path, file_events=True)
    observer.schedule(stream)

    daemonize()

main()
