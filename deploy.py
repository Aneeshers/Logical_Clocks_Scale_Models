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
import select


# Function takes the max of two values timestamp values
def calc_recv_timestamp(recv_time_stamp, counter):
    try:
        # Check if the inputs are the correct time
        assert isinstance(recv_time_stamp,int), "recv_time_stamp is not an int val type "
        assert isinstance(counter,int), "counter is not an int val type"
     
        # Returns the larger timestamp
        return max(recv_time_stamp, counter)

    except AssertionError as error:
        print(f"[PORT: INTERNAL FUNCTION] | UNIT TEST: calc_recv_timestamp() - ❌ - {error}")


# Helper function to log logical clock time and global system time 
def logical_and_global_time(counter):
    try:
        assert isinstance(counter,int), "counter is not an int val type"
        
        return ' (LAMPORT_TIME={}, SYSTEM_TIME={})'.format(counter,
                                                     datetime.datetime.now())
    except AssertionError as error:
        print(f"[PORT: INTERNAL FUNCTION] | UNIT TEST: local_time() - ❌ - {error}")


# Listens for incoming messages on the connection
def consumer(conn,PORT):
    try:

        # Check if the parameters 
        assert conn, "empty socket passed into consumer()"
        assert isinstance(PORT,int), "given PORT an int value"


        # Retrives global counter (logical clock) value
        global counter
        
        # Decodes message and adds it to the queued message list (note this instanteously)
        while True:
            data = conn.recv(1024)
            dataVal = data.decode('ascii')

            # Check if the recieved message is the correct type before appending to message
            assert isinstance(dataVal,str), f"received data payload is not a str type"

            msg_queue.append(dataVal)

    except AssertionError as error:
        print(f"[PORT:{PORT}] | UNIT TEST: consumer() - ❌ - {error}")

 
# Sends connection request and once connected sends messages to other processes
def producer(portVal):
    try:

        # Checks if there are only 4 system args getting past in
        assert len(portVal) == 4, "config param didn't pass 4 arguments into producer()"

        # Global variables counter (logical clock) and message queue list
        global counter
        global msg_queue

        # Creates a socket connecting 
        host= "127.0.0.1"

        # Initalizes ports
        port0 = int(portVal[1])
        port1 = int(portVal[2])
        port2 = int(portVal[3])

        # Check if Ports an integers (able to be converted)
        assert isinstance(port0, int), "PORT was not was unable to be converted to an int"
        assert isinstance(port1, int), "PORT was not was unable to be converted to an int"
        assert isinstance(port2, int), "PORT was not was unable to be converted to an int"

        # starts sockets to communicate to port1 and port2
        s1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        # Checks if sockets were successfully created
        assert s1, "socket was unable to be created in producer()"
        assert s2, "socket was unable to be created in producer()"

        # Sets the "system speed"
        ticks = random.randint(1, 24)
        sleepVal = 1/ticks

        # Initialize log and plotting logs
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

            # Checks if sockets were able to connect to the other ports
            assert s1.getsockname() , f"socket was unable to connect to: [PORT: {port1}, HOST: {host}]"
            assert s2.getsockname() , f"socket was unable to connect to: [PORT: {port2}, HOST: {host}]"

            print(str(port0) + " is attempting to connect to " + str(port1) +  " AND " + str(port2))

            # Create/Clear log files and other files used to graph
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

                # Simulate clock cycle speed
                time.sleep(sleepVal)

                # log plotting data every 5 seconds
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
                    
                    assert isinstance(m, str), "Message that is popped is not a string value"

                    m = m.split(":")

                    assert len(m) == 2, "Invalid message has been sent. Contains extra information."


                    # update logical clock from the dateTime value in message and current logical clock
                    counter = calc_recv_timestamp(int(m[1]), counter)

                    assert calc_recv_timestamp(1,10) == 10, "Incorrect timestamp returned type 1"
                    assert calc_recv_timestamp(0, 0) == 0, "Incorrect timestamp returned type 2"
                    assert calc_recv_timestamp(-10,10) == 10, "Incorrect timestamp returned type 3"
                    assert calc_recv_timestamp(-10,-10) == -10, "Incorrect timestamp returned type 4"
                    assert calc_recv_timestamp(10,-10) == 10, "Incorrect timestamp returned type 5"

                    # Log message was recieved, the logical clock time, and global time.
                    f = open(log, "a")
                    f.write("msg received" + logical_and_global_time(counter) + " msg_queue len: " + str(len(msg_queue))+"\n")
                    

                    # Closes file to save newly written data
                    f.close()

                # If there are no messages in queque send a message
                else:
                    
                    # Random number to decide what the action is
                    r = random.randint(1, 10)

                    # Values not equal to 1, 2, or 3 result in no action
                    message = str(port0) + ":"

                    # here the probability that an internal event will occur is 70%
                    if r > 3 :
                        counter += 1
                        f = open(log, "a")
                        f.write("INTERNAL EVENT." + logical_and_global_time(counter)+"\n")
                    
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

    except AssertionError as error:
        print(f"[PORT:{port0}] | UNIT TEST: producer() - ❌ - {error}")


# Used to accept connections
def init_machine(config):
    try:

        # Checks if there are only 4 system args getting past in
        assert len(config) == 4, "config param didn't pass 4 arguments into init_machine()"

        # Gets HOST and PORT from congfig
        HOST = str(config[0])
        PORT = int(config[1])

        # Checks if the PORT and HOST are acceptable types
        assert isinstance(HOST, str), "HOST was not was unable to be converted a string"
        assert isinstance(PORT, int), "PORT was not was unable to be converted to an int"

        print("starting server| port val:", PORT)

        # Connects to HOST and PORT
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Check if the socket was succesfully created
        assert s, f"socket was unable to be created in init_machine()"

        s.bind((HOST, PORT))

        # Checks if socket binded correctly
        assert s.getsockname() , f"socket was unable to connect to: [PORT: {PORT}, HOST: {HOST}]"

        s.listen()
        
        # Checks if s is in the read list (aka listening)
        read_list, write_list, error_list = select.select([s], [], [], 5)
        assert s in read_list, f"socket was unable to listen on: [PORT: {PORT}, HOST:{HOST}]"

        print(f"[PORT:{PORT}] | UNIT TEST: init_machine() - ✅")

        # Starts a new thread to recieve messages on
        while True:
            conn, addr = s.accept()
            start_new_thread(consumer, (conn,PORT))

    except AssertionError as error:
        print(f"[PORT:{PORT}] | UNIT TEST: init_machine() - ❌ - {error}")


# Initalization of the different threads per machine process
def machine(config):
    try:

        # Checks if there are only 4 system args getting past in
        assert len(config) == 4, "config param didn't pass 4 arguments into machine()"

        global msg_queue
        global counter

        # Initalizes the counter (logical clock) and message queue
        counter = 0
        msg_queue = []

        # Checks if counter (logical clock) and messages are set to zero on connection
        assert counter == 0, "counter is not initialized to 0 in machine()"
        assert msg_queue == [], "msg_queue is not initialized to [] in machine()"
        
        print(f"[PORT:{config[1]}] | UNIT TEST: machine() - ✅")

        
        # Starts thread to listen for new connections request
        init_thread = Thread(target=init_machine, args=(config,))
        init_thread.start()

        # Add delay to initialize the server-side logic on all processes
        time.sleep(2)

        # Starts thread to send connection requests and simulate clock speed + execute actions
        prod_thread = Thread(target=producer, args=(config,))
        prod_thread.start()

    except AssertionError as error:
        print(f"[PORT:{config[1]}] | UNIT TEST: machine() - ❌ - {error}")


##### Start Tests #####

# Hard Code LocalHost
localHost= "127.0.0.1"

if __name__ == '__main__':

    # Hard coded ports for the 3 proccesses
    port1 = 2056
    port2 = 3056
    port3 = 4056
    
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