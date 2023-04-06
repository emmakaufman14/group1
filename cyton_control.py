import socket

import numpy as np

import time
from statistics import mode


class CytonController:
    """
    Management class for performing specific actions with the cyton gamma robot. Also provides an interface for
    sending commands to the robot
    """

    def __init__(self, connect: bool = False):

        self.connect = connect

        self.sock: socket.socket = None
        self.udp_ip = None
        self.udp_port = None

        if self.connect:
            self.establish_connection()

        print(f"Setting starting pose to home")

        self.go_home()

        time.sleep(5)

        # print(f"Setting starting pose to one")
        #
        # self.go_one()
        #
        # time.sleep(5)

        # print(f"Setting starting pose to two")
        #
        # self.go_two()
        #
        # time.sleep(5)
        #
        # print(f"Setting starting pose to three")
        #
        # self.go_three()
        #
        # time.sleep(5)
        #
        # print(f"Setting starting pose to four")
        #
        # self.go_four()
        #
        # time.sleep(5)
        #
        # print(f"Setting starting pose to human")
        #
        # self.go_human()


        # self.set_pose(self.pose)

    # def __del__(self):
    #     self.sock.shutdown()

    def establish_connection(self, udp_ip: str = "127.0.0.1", udp_port: int = 8888) -> bool:
        """
        Establishes a connection to the robot
        :return: True/False whether the connection was successful
        """
        print(f"Establishing Connection at {udp_ip}:{udp_port}")

        self.udp_ip = udp_ip
        self.udp_port = udp_port

        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP

        self.sock.connect((self.udp_ip, self.udp_port))


        print("Connection established")

    def set_angles(self, q):
        """
        Sets the pose for the robot. If connected, then it sets the robot's end effector pose.
        :param q: Pose (SE3)
        :return:
        """
        # TODO

        data = np.array(q, dtype=np.double)
        data = data.view(np.uint8)
        print(data)

        if self.connect:
            try:
                self.sock.sendto(data, (self.udp_ip, self.udp_port))
                time.sleep(0.2)

            except Exception as e:
                # recreate the socket and reconnect
                print(f"Error connecting to {self.udp_ip}:{self.udp_port}. Reconnecting")
                self.establish_connection(self.udp_ip, self.udp_port)

                self.sock.send(data)
        # TODO: fake printouts

    # def set_pose(self, P: SE3):

    def go_home(self):
        # self.set_pose(self.robot.qz)
        self.set_angles([0, 0, 0, 0, 0, 0, 0, 0])

    def go_one(self):
        # self.set_pose(self.robot.qz)
        self.set_angles([1.058, 1.061, 0.0, 1.309, 0.0, 0.811476, 0.0, 0.01])
    def go_two(self):
        # self.set_pose(self.robot.qz)
        self.set_angles([0.557, 1.0612, 0.0, 1.309, 0.0, 0.725, 0.0, 0.01])

    def go_three(self):
        # self.set_pose(self.robot.qz)
        self.set_angles([0.0, 0.979, 0.0, 1.46989, 0.0, 0.811476, 0.0, 0.01])

    def go_four(self):
        # self.set_pose(self.robot.qz)
        self.set_angles([-0.5011, 1.0612, 0.0, 1.309, 0.0, 0.725, 0.0, 0.01])

    def go_human(self):
        # self.set_pose(self.robot.qz)
        self.set_angles([0.0, -0.7, 0.0, -0.7, 0.0, -0.7, 0.0, 0.01])


class leapController:
    """
    """

    def __init__(self, connect: bool = False):

        self.connect = connect

        self.sock: socket.socket = None
        self.udp_ip = None
        self.udp_port = None

        self.fingers = []
        self.finger_mode = 0

        if self.connect:
            self.establish_connection()

    def establish_connection(self, udp_ip: str = "127.0.0.1", udp_port: int = 5005) -> bool:
        """
        Establishes a connection to the robot
        :return: True/False whether the connection was successful
        """
        print(f"Establishing Connection at {udp_ip}:{udp_port}")

        self.udp_ip = udp_ip
        self.udp_port = udp_port


    def read_leap(self):
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP

        self.sock.bind((self.udp_ip, self.udp_port))
        self.fingers = []
        for ii in range(100):
            data, addr = self.sock.recvfrom(1)
            self.fingers.append(data[0])
        self.finger_mode = mode(self.fingers)
        self.sock.close()



if __name__ == "__main__":

    controller = CytonController(connect=True)

    leap = leapController(connect=True)
    while True:
        leap.read_leap()
        print(leap.finger_mode)
        if leap.finger_mode == 1:
            controller.go_one()
        elif leap.finger_mode == 2:
            controller.go_two()
        elif leap.finger_mode == 3:
            controller.go_three()
        elif leap.finger_mode == 4:
            controller.go_four()
        elif leap.finger_mode == 5:
            controller.go_human()
        time.sleep(5)



    # controller.set_angles([0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0])
    # q = [0, 0.7, 0, 0.7, 0, 0.7, 0, 0.1]
    #
    # controller.set_angles(q)