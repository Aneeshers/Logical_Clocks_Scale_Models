import unittest
import socket
import time
from multiprocessing import Process
from deploy import *

class TestDistributedSystem(unittest.TestCase):

    def test_valid_payload(self):
        # Ensure that the message payload is valid
        msg = "Test message"
        encoded_msg = msg.encode('ascii')
        decoded_msg = encoded_msg.decode('ascii')
        self.assertEqual(msg, decoded_msg)

    def test_port_number(self):
        # Ensure that the port number is within the valid range
        port = 2056
        with self.assertRaises(Exception) as context:
            # Attempt to bind to an invalid port number
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("127.0.0.1", port))
        self.assertTrue("OSError" in str(context.exception))

    def test_message_queue(self):
        # Ensure that the message queue is being properly updated
        msg_queue = []
        p = Process(target=producer, args=(["127.0.0.1", 2056, 3056, 4056],))
        p.start()
        time.sleep(2) # Wait for the producer to initialize
        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s1.connect(("127.0.0.1", 2056))
        s1.send("1".encode('ascii'))
        time.sleep(2) # Wait for the message to be processed
        p.terminate()
        self.assertEqual(msg_queue, ["1"])

if __name__ == '__main__':
    unittest.main()
