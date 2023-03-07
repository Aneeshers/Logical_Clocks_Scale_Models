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


# Listens for incoming messages on the connection
def consumer(conn):

    # Retrives global counter value
    global counter

    print("consumer accepted connection" + str(conn)+"\n")
    
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
    print("PORTVAL:",portVal)

    # Creates a socket connecting 
    host= "127.0.0.1"
    port1 = int(portVal[0])
    port2 = int(portVal[1])
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    t = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # Sets the "system speed"
    ticks = random.randint(1, 6)
    sleepVal = 1/ticks
    filename = str(port1) + ".txt"

    # abstract
    # Start time
    start = time.time()

    # Try to connect to socket
    try:
        # Connects to sockets
        s.connect((host,port1))
        t.connect((host,port2))

        # Connection message
        print("Client-side connection success to port val:" + str(port1) + "\n")
        print("Client-side connection success to port val:" + str(port2) + "\n")

        # While program is running send and dequeue messages
        while (True):

            # Prints to console the elapsed time
            print("time elapsed ", time.time() - start)
            time.sleep(sleepVal)
            
            # If there are queued messages first dequeue
            if len(msg_queue) > 0:

                # Get the most recent message
                m = msg_queue.pop()

                # Creates a timestamp from the dateTime value in message
                counter = calc_recv_timestamp(int(m), counter)
                
                # TODO Do we want to make the writen information in CSF am 
                # Open the file associated with the current process and writes to it before saving
                f = open(filename, "a")
                f.write("msg received " + local_time(counter) + " msg_queue len: " + str(len(msg_queue))+"\n")
                
                # Closes file to save newly written data
                f.close()

            # If there are no messages in queque send a message
            else:
                
                # Random number to decide what the action is
                r = random.randint(1, 10)

                # TODO implement actions for values 1,2,3
                # Values not equal to 1, 2, or 3 result in no action
                if r > 3 :
                    counter += 1

                # Sends to process 1
                elif r == 1:
                    counter += 1
                    s.send(str(counter).encode('ascii'))
                
                # Sends to process 2
                elif r == 2: 
                    counter += 1
                    t.send(str(counter).encode('ascii'))

                # Sends to both other processes
                else:
                    counter += 1
                    t.send(str(counter).encode('ascii'))
                    s.send(str(counter).encode('ascii'))

    
    # Catches any errors when connecting to the socket
    except socket.error as e:
        print ("Error connecting producer: %s" % e)
 

# Used to accept connections
def init_machine(config):

    # Gets HOST and PORT from congfig
    HOST = str(config[0])
    PORT = int(config[1])

    print("starting server| port val:", PORT)

    # Connects to HOST and PORT
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()

    # Starts a new thread to recieve messages on
    while True:
        conn, addr = s.accept()
        start_new_thread(consumer, (conn,))
 
# Initalization of the different threads
def machine(config):

    # TODO Idk what this does
    config.append(os.getpid())
    global code
    global msg_queue
    global counter

    # Initalizes the counter an message queue
    counter = 0
    msg_queue = []

    #print(config)
    # Starts thread to listen for new connections request
    init_thread = Thread(target=init_machine, args=(config,))
    init_thread.start()

    # Add delay to initialize the server-side logic on all processes
    time.sleep(2)
    print("CONFIG:",config)

    # Extensible to multiple producers
    # Starts thread to send connection requests
    prod_thread = Thread(target=producer, args=(config[1:3],))
    prod_thread.start()
 

    # TODO: Idk what this does tbh. Commented it out and it still works
    # while True:
    #     code = random.randint(1,3)


    ##### Starts Tests #####

# Hard Code LocalHost
localHost= "127.0.0.1"
 

if __name__ == '__main__':

    # Hard coded ports for the 3 proccesses
    port1 = 2056
    port2 = 3056
    port3 = 4056
 
    # Initalizes Process1
    config1=[localHost, port1, port2,]
    p1 = Process(target=machine, args=(config1,))

    # Initalizes Process2
    config2=[localHost, port2, port3]
    p2 = Process(target=machine, args=(config2,))

    # Initalizes Process3
    config3=[localHost, port3, port1]
    p3 = Process(target=machine, args=(config3,))
    
    # Start the processes
    p1.start()
    p2.start()
    p3.start()
    
    # Once child processes starts the main Process
    p1.join()
    p2.join()
    p3.join()