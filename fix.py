import socket
import time
from ctypes import *

'''
A simple example for controlling a single joint move once by python

Ref: https://github.com/MrAsana/AMBER_B1_ROS2/wiki/SDK-&-API---UDP-Ethernet-Protocol--for-controlling-&-programing#2-single-joint-move-once
C++ version:  https://github.com/MrAsana/C_Plus_API/tree/master/amber_gui_4_node
     
'''
# IP_ADDR = "45.125.46.201"  # ROS master's IP address
IP_ADDR = "127.0.0.1"  # ROS master's IP address
PORT = 25001


class robot_joint_position(Structure):  # ctypes struct for send
    _pack_ = 1  # Override Structure align
    _fields_ = [("Cmd_no", c_int16),
                ("Length", c_int16),
                ("ID", c_int32),
                ("Can_id", c_byte),
                ("Can_len", c_byte),
                ("Joint_no", c_int16),
                ("Data0", c_byte),
                ("Data1", c_byte),
                ("Data2", c_byte),
                ("Data3", c_byte),
                ("Data4", c_byte),
                ("Data5", c_byte),
                ("Data6", c_byte),
                ("Data7", c_byte),
                ]


class robot_mode_data(Structure):  # ctypes struct for receive
    _pack_ = 1
    _fields_ = [("Cmd_no", c_int16),
                ("Length", c_int16),
                ("ID", c_int32),
                ("Can_id", c_byte),
                ("Can_len", c_byte),
                ("Empty", c_byte),
                ("Proxy_Status", c_byte),
                ("Data0", c_byte),
                ("Data1", c_byte),
                ("Data2", c_byte),
                ("Data3", c_byte),
                ("Data4", c_byte),
                ("Data5", c_byte),
                ("Data6", c_byte),
                ("Data7", c_byte),
                ]


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Standard socket processes
s.bind(("0.0.0.0", 12321))

payloadS = robot_joint_position(1,  # CMD_NO
                                20,  # Length
                                12,  # ID
                                0x11,  # Can_id
                                2,  # Can_len
                                1,  # Joint_no
                                0x5E, 0x0A, 0, 0, 0, 0, 0, 0  # DATA
                                )
s.sendto(payloadS, (IP_ADDR, PORT))  # Default port is PORT
s.settimeout(3)
try:
    data, addr = s.recvfrom(1024)  # Need receive return
    print("Receiving: ", data.hex())
    payloadR = robot_mode_data.from_buffer_copy(data)
    print("Received: Cmd_no={:d}, Length={:d}, "
          "ID={:d}, CAN_id={:x}, CAN_len={:d}, Proxy_Status={:d}, "
          "".format(payloadR.Cmd_no,
                    payloadR.Length,
                    payloadR.ID,
                    payloadR.Can_id,
                    payloadR.Can_len,
                    payloadR.Proxy_Status,
                    ))
    print("Received:Data={:x}  {:x}  {:x}  {:x}  {:x}  {:x}  {:x}"
          .format(payloadR.Data0,
                  payloadR.Data1,
                  payloadR.Data2,
                  payloadR.Data3,
                  payloadR.Data4,
                  payloadR.Data5,
                  payloadR.Data6,
                  payloadR.Data7,
                  ))
except socket.timeout:
    print("timeout!")
s.close()
time.sleep(0.5)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Standard socket processes
s.bind(("0.0.0.0", 12321))

payloadS = robot_joint_position(1,  # CMD_NO
                                20,  # Length
                                12,  # ID
                                0x11,  # Can_id
                                2,  # Can_len
                                1,  # Joint_no
                                0x71, 0x00, 0x73, 0, 0, 0, 0, 0  # DATA
                                )
s.sendto(payloadS, (IP_ADDR, PORT))  # Default port is PORT
s.settimeout(3)
try:
    data, addr = s.recvfrom(1024)  # Need receive return
    print("Receiving: ", data.hex())
    payloadR = robot_mode_data.from_buffer_copy(data)
    print("Received: Cmd_no={:d}, Length={:d}, "
          "ID={:d}, CAN_id={:x}, CAN_len={:d}, Proxy_Status={:d}, "
          "".format(payloadR.Cmd_no,
                    payloadR.Length,
                    payloadR.ID,
                    payloadR.Can_id,
                    payloadR.Can_len,
                    payloadR.Proxy_Status,
                    ))
    print("Received:Data={:x}  {:x}  {:x}  {:x}  {:x}  {:x}  {:x}"
          .format(payloadR.Data0,
                  payloadR.Data1,
                  payloadR.Data2,
                  payloadR.Data3,
                  payloadR.Data4,
                  payloadR.Data5,
                  payloadR.Data6,
                  payloadR.Data7,
                  ))
except socket.timeout:
    print("timeout!")
s.close()
