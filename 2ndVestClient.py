# -*- coding: utf-8 -*-
"""
2nd Vest Client
    Try
        Initiazlize host and port
        Bind to socket
        Load tact files

        Try
            Haptics loop
                Receive command
                Process string
                Play haptics

        Except ValueError (Disconnected)

    Except ConnectionRefusedError (Wrong IP address)

Created on Mon Feb 14 20:19:39 2022
@author: Ben Toaz
"""

import socket
from bhaptics import better_haptic_player as player
import utilitiesMethods as utility

# Switches index key to new index value
rvs_index_dict = {'d': "a", 'a': 'd', 's': "w", 'w': 's', 'sd': 'wa',
                  'sa': 'wd', 'wd': 'sa', 'wa': 'sd'}

# Matches reversed index to opposite direction haptic file name
rvs_haptic_dict = {'d': "MoveLeft", 'a': 'MoveRight', 's': "MoveForward",
                   'w': 'MoveBack', 'sd': 'ForwardLeft', 'sa': 'ForwardRight',
                   'wd': 'BackLeft', 'wa': 'BackRight'}

try:
    # Initialize host and port
    host = "35.12.209.58"
    port = 8080

    # Bind socket with port and host
    s = socket.socket()
    s.connect((host, port))
    print("Connected to Server.")

    # Picks Set of Haptic Feedback
    iteration = 4
    player.initialize()

    # Load Tact files from directory
    for value in rvs_haptic_dict.values():
        player.register(value+str(iteration), value+str(iteration)+".tact")

    try:

        # Haptics loop
        while(True):

            # Receive command from master program
            command = s.recv(1024)

            # Command is string of 1-2 letters and intensity float
            command = command.decode()

            # Recover index and intensity from command
            command = command.split('-')
            raw_intensity = float(command[0])
            index = command[1]
            teacher_intensity = float(command[2])

            # Play teacher haptics
            utility.play(haptic_index=rvs_index_dict[index],
                         intensity=raw_intensity*teacher_intensity)

    # Server ends program
    except ValueError:
        print('Disconnected')

except ConnectionRefusedError:
    print("Check IP address")
