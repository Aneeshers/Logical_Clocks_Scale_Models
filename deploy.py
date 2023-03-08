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
import sys


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


# Listens for incoming messages on the connection
def consumer(conn):

    # Retrives global counter value
    global counter
    
    # Decodes message and adds it to the queued message list
    while True:
        data = conn.recv(1024)
        dataVal = data.decode('ascii')
        msg_queue.append(dataVal)
 
# Sends connection request and once connected sends messages to other processes
def producer(portVal):

    # Global variables counter and message queue list
    global counter
    global msg_queue

    # Creates a socket connecting 
    host= "127.0.0.1"
    port0 = int(portVal[1])
    port1 = int(portVal[2])
    port2 = int(portVal[3])
    s1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # Sets the "system speed"
    ticks = random.randint(1, 24)
    sleepVal = 1/ticks
    log = "logs/" + str(port0) + ".txt"
    times = "logs/" + str(port0) + "time.txt"
    msgqueulen = "logs/" + str(port0) + "msgqueulen.txt"
    timestamps = "logs/" + str(port0) + "timestamps.txt"
    
    # Start time
    start = time.time()
    recurr = time.time()

    # Try to connect to socket
    try:
        # Connects to sockets
        s1.connect((host,port1))
        s2.connect((host,port2))
        print(str(port0) + " is attempting to connect to " + str(port1) +  " AND " + str(port2))
        f = open(log, "w")
        f.close()
        xf = open(times, "w")
        xf.close()
        yf = open(msgqueulen, "w")
        yf.close()
        tf = open(timestamps, "w")
        tf.close()
        # While program is running send and dequeue messages
        while (True):

            # Prints to console the elapsed time
            time.sleep(sleepVal)

            if (time.time() - recurr) > 5:

                recurr  = time.time()
            
                # log seconds elapsed every 5 seconds (system time)
                xf = open(times, "a")
                xf.write(str(time.time() - start) + "," )
                xf.close()

                # log msg queue lengths at those system times
                yf = open(msgqueulen, "a")
                yf.write(str(len(msg_queue)) + ",")
                yf.close()
                
                # log logical clock time stamps at those system times
                tf = open(timestamps, "a")
                tf.write(str(counter) + ",")
                tf.close()
                
                
            # If there are queued messages first dequeue
            if len(msg_queue) > 0:
                

                # Get the most recent message
                m = msg_queue.pop()
                m = m.split(":")
                # Creates a timestamp from the dateTime value in message
                counter = calc_recv_timestamp(int(m[1]), counter)
               
                


                # TODO Do we want to make the writen information in CSF am 
                # Open the file associated with the current process and writes to it before saving
                f = open(log, "a")
                f.write("msg received" + local_time(counter) + " msg_queue len: " + str(len(msg_queue))+"\n")
                
                # Closes file to save newly written data
                f.close()

            # If there are no messages in queque send a message
            else:
                
                # Random number to decide what the action is
                r = random.randint(1, 10)

                # Values not equal to 1, 2, or 3 result in no action
                message = str(port0) + ":"
                if r > 3 :
                    counter += 1
                    f = open(log, "a")
                    f.write("INTERNAL EVENT." + local_time(counter)+"\n")
                
                    # Closes file to save newly written data
                    f.close()

                # Sends to process 1
                elif r == 1:
                    counter += 1
                    s1.send((message + str(counter)).encode('ascii'))
                
                # Sends to process 2
                elif r == 2: 
                    counter += 1
                    s2.send((message + str(counter)).encode('ascii'))

                # Sends to both other processes
                else:
                    counter += 1
                    s1.send((message + str(counter)).encode('ascii'))
                    s2.send((message + str(counter)).encode('ascii'))

    
    # Catches any errors when connecting to the socket
    except socket.error as e:
        print ("Error connecting producer: %s" % e)
 

# Used to accept connections
def init_machine(config):
    try:

        # Gets HOST and PORT from congfig
        HOST = str(config[0])
        PORT = int(config[1])

        assert len(config) == 4, "config param didn't pass 4 arguments into init_machine()"

        print("starting server| port val:", PORT)

        # Connects to HOST and PORT
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # assert not hasattr(s, 'fileno'), "socket was unable to be created in init_machine()"

        s.bind((HOST, PORT))

        # assert s.getsockname()[1] == 0, f"socket was unable to connect to: [PORT: {PORT}]"

        s.listen()

        # assert s.getsockopt(socket.SOL_SOCKET, socket.SO_ACCEPTCONN) != 1, f"socket was unable to listen on: [PORT: {PORT}]"

        print(f"PORT {PORT}: machine() - ✅")
        # Starts a new thread to recieve messages on
        while True:
            conn, addr = s.accept()
            start_new_thread(consumer, (conn,))

    except AssertionError as error:
        print(f"[PORT:{PORT}]| UNIT TEST: init_machine() - ❌ - {error}")


# Initalization of the different threads
def machine(config):
    try:

        # Checks if there are only 4 system args getting past in
        assert len(config) == 4, "config param didn't pass 4 arguments into machine()"

        # # TODO Idk what this does
        # config.append(os.getpid())
        global msg_queue
        global counter
        # Initalizes the counter an message queue
        counter = 0
        msg_queue = []

        # Checks if counters and messages are set to zero on connection
        assert counter == 0, "counter is not initialized to 0 in machine()"
        assert msg_queue == [], "msg_queue is not initialized to [] in machine()"
        
        print(f"[PORT:{config[1]}]| UNIT TEST: machine() - ✅")

        
        #print(config)
        # Starts thread to listen for new connections request
        init_thread = Thread(target=init_machine, args=(config,))
        init_thread.start()

        # Add delay to initialize the server-side logic on all processes
        time.sleep(2)

        # Extensible to multiple producers
        # Starts thread to send connection requests
        prod_thread = Thread(target=producer, args=(config,))
        prod_thread.start()

    except AssertionError as error:
        print("UNIT TEST: machine() - ❌ -",error)


    ##### Starts Tests #####

# Hard Code LocalHost
localHost= "127.0.0.1"
 
def defaultPort(default, CL_arg):
    print(default)
    if not (str(default)).isnumeric():
        return ValueError("Default port needs to be a number")
    try:
        port = int(CL_arg)
        return port
    except:
        return default



if __name__ == '__main__':
    try:
        # Hard coded ports for the 3 proccesses
        if len(sys.argv) == 5:
            port1 = defaultPort(2056,sys.argv[2])
            port2 = defaultPort(3056,sys.argv[3])
            port3 = defaultPort(4056,sys.argv[4])
        else:
            port1 = 2056
            port2 = 3056
            port3 = 4056


        # Assertions for checking if the port is correct
        assert defaultPort(2056,"ASDF") == 2056
        assert defaultPort(3056, 2056) == 2056
        assert isinstance(defaultPort("ASDF", 2056),ValueError)
        assert isinstance(defaultPort("ASDF", "2056"),ValueError)
    
        
        # Initalizes Process1
        config1=[localHost, port1, port2,port3]
        p1 = Process(target=machine, args=(config1,))

        # Initalizes Process2
        config2=[localHost, port2, port3, port1]
        p2 = Process(target=machine, args=(config2,))

        # Initalizes Process3
        config3=[localHost, port3, port1, port2]
        p3 = Process(target=machine, args=(config3,))
        
        # Start the processes
        p1.start()
        p2.start()
        p3.start()
        
        # Once child processes starts the main Process
        p1.join()
        p2.join()
        p3.join()
    except Exception:
        exit()