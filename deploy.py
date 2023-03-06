from multiprocessing import Process
import os
import socket
from _thread import *
import threading
import time
from threading import Thread
import random
import datetime
import time

# Some notes
# The more ticks, the less drift
# plots msq_queu over time
# plots lamport time stamps for each process 

# once they have been initalized -- THEN you can make choices on design


# Unit tests
# Whether your packet has a valid payload?
# write about the checks you make on the packets?
# error checking -- host and port, randomness, use assertions (host and port should be terminal)


# sleep for 1/ticks 
def calc_recv_timestamp(recv_time_stamp, counter):
    return max(recv_time_stamp, counter)

def local_time(counter):
    return ' (LAMPORT_TIME={}, SYSTEM_TIME={})'.format(counter,
                                                     datetime.datetime.now())


def consumer(conn):
    global counter
    print("consumer accepted connection" + str(conn)+"\n")
    while True:
        data = conn.recv(1024)
        dataVal = data.decode('ascii')
        msg_queue.append(dataVal)
 

def producer(portVal):
    global counter
    global msg_queue
    host= "127.0.0.1"
    port = int(portVal)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ticks = random.randint(1, 6)
    sleepVal = 1/ticks
    filename = str(portVal) + ".txt"
    # abstract
    start = time.time()
    try:
        s.connect((host,port))
        print("Client-side connection success to port val:" + str(portVal) + "\n")
        while (True):
            print("time elapsed ", time.time() - start)
            time.sleep(sleepVal)
            if len(msg_queue) > 0:
                m = msg_queue.pop()
                counter = calc_recv_timestamp(int(m), counter)
                print("msg received " + local_time(counter) + " msg_queue len: " + str(len(msg_queue)))
            else:
                r = random.randint(0, 9)
                if r < 4:
                    counter += 1
                    s.send(str(counter).encode('ascii'))
                else:
                    counter +=1
    except socket.error as e:
        print ("Error connecting producer: %s" % e)
 

def init_machine(config):
    HOST = str(config[0])
    PORT = int(config[1])
    print("starting server| port val:", PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        start_new_thread(consumer, (conn,))
 

def machine(config):
    config.append(os.getpid())
    global code
    global msg_queue
    global counter
    counter = 0
    msg_queue = []
    #print(config)
    init_thread = Thread(target=init_machine, args=(config,))
    init_thread.start()
    #add delay to initialize the server-side logic on all processes
    time.sleep(2)
    # extensible to multiple producers
    prod_thread = Thread(target=producer, args=(config[2],))
    prod_thread.start()
 

    while True:
        code = random.randint(1,3)

localHost= "127.0.0.1"
 

if __name__ == '__main__':
    port1 = 2056
    port2 = 3056
    port3 = 4056
 

    config1=[localHost, port1, port2,]
    p1 = Process(target=machine, args=(config1,))
    config2=[localHost, port2, port3]
    p2 = Process(target=machine, args=(config2,))
    config3=[localHost, port3, port1]
    p3 = Process(target=machine, args=(config3,))
    

    p1.start()
    p2.start()
    p3.start()
    

    p1.join()
    p2.join()
    p3.join()