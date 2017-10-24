#!/usr/bin/env python
from threading import Thread
import subprocess
from Queue import Queue
import multiprocessing

num_threads = multiprocessing.cpu_count()
print("Number of available threads: ",num_threads)
queue = Queue(-1)
ips = []
for i in range(1,255):
	ips=ips+["192.168.1."+str(i)]
#wraps system ping command
def pinger(i, q):
    """Pings subnet"""
    while True:
	print("--i am thread ",i," --")
        ip = q.get()
        #print "Thread %s: Pinging %s" % (i, ip)
        ret = subprocess.call("ping -c 1 %s" % ip,
            shell=True,
            stdout=open('/dev/null', 'w'),
            stderr=subprocess.STDOUT)
        if ret == 0:
            print "%s: is alive" % ip
        else:
            print "%s: did not respond" % ip
        q.task_done()
#Spawn thread pool
for i in range(num_threads):

    worker = Thread(target=pinger, args=(i, queue))
    worker.setDaemon(True)
    worker.start()
#Place work in queue
for ip in ips:
    queue.put(ip)
#Wait until worker threads are done to exit    
queue.join()
