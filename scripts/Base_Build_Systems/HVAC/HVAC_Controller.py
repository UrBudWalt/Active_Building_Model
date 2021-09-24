""" 
Hi Welcome to the HVAC controller of the....
______                 ______       _ _     _   _____           _                 
| ___ \                | ___ \     (_) |   | | /  ___|         | |                
| |_/ / __ _ ___  ___  | |_/ /_   _ _| | __| | \ `--. _   _ ___| |_ ___ _ __ ___  
| ___ \/ _` / __|/ _ \ | ___ \ | | | | |/ _` |  `--. \ | | / __| __/ _ \ '_ ` _ \ 
| |_/ / (_| \__ \  __/ | |_/ / |_| | | | (_| | /\__/ / |_| \__ \ ||  __/ | | | | |
\____/ \__,_|___/\___| \____/ \__,_|_|_|\__,_| \____/ \__, |___/\__\___|_| |_| |_|
                                                       __/ |                      
                                                      |___/                       
For the active building model.

####################################################################################
## This script is designed to control the following sub systems of the AB Model:  ##
## - HVAC                                                                         ##
####################################################################################

Developer Info:
Name: Walter Bassage 
Email: w.bassage@sheffield.ac.uk
Code Version: 0.1v
"""

###############################-- Import Libaries --##################################
## For this network I have used a simple soctet connection to setup a newtork that  ##
######################################################################################
import os
import sys
import time
import errno
import serial
import socket
import logging
import threading
import configparser
from time import sleep
from queue import Queue
from random import randrange
from co2_monitor import sensros

###############################-- Global Variables --#################################
## For this network I have used a simple soctet connection to setup a newtork that  ##
######################################################################################
HEADER_LENGTH = 10          # Variable used when sending messages to server
NUMBER_OF_THREADS = 3       # Number of threads in which I can use
JOB_NUMBER = [1,2,3]        # Number of active jobs at any point in run time
queue = Queue()


# Variables used in the creation and recalling settings file
system_file = "client_settings.ini"
config = configparser.ConfigParser()

subsystem_ID = "HVAC"

##################################-- Nework Setup --##################################
## Check conncetion status                                                          ##
## Request client restarts                                                          ##
## Records data from clients                                                        ##
######################################################################################
        
# This function creates the connection to the server
def connection():
    # call the settings files and uses the Stored IP and HOST 
    config.read(system_file)
    config.sections()

    # Mannal Update on IP and Username 
    subsystem_ID = "HVAC"
    host = '10.0.0.11'
    port = 1234
    
    # Use global to allow the veriable use outside the function
    global client_socket
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    # Prevents the recvie function not to be blocking
    client_socket.setblocking(False)
    
    username = subsystem_ID.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(username_header + username)
    
    print("Connection establised with server")
    
###############################-- Global Variables --#################################
## For this network I have used a simple soctet connection to setup a newtork that  ##
######################################################################################

def main_sensor():
    while True:
        for x in range(3):
            num = str(x+1)
            message = sensros(num)
            time.sleep(0.10)
            if not message:
                print("System booting...")
                time.sleep(0.30)
            else:
                send_data(message)

def self_manage():
    while True:
        try:
            sleep(15)
            continue
        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error', str(e))
            continue
                
        except Exception as e:
            print('General error', str(e))
            sys.exit()

def security_protocalls():
    print("Hey this is where security will running")

###############################-- Client Commands --##################################
## Check conncetion status                                                          ##
## Request client restarts                                                          ##
## Records data from clients                                                        ##
######################################################################################

def send_data(info):
    try:
        message = (info)
        # Ecryption add here
        
        message = message.encode('utf-8')
        message_header =  f"{len(message) :< {HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message)
        # sleep(0.5)
            
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            error_code = str(e)
            if error_code == "[Errno 32] Broken pipe":
                # Protocal that makes the HVAC system manage itself while disconnected from the controller 
                self_manage()
            sys.exit()
            
    except Exception as e:
        print('General error', str(e))
        sys.exit()

def recive_commands():
    while True:        
        try:
            # We recive things
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("connction closed by the server")
                sys.exit()
            
            username_length = int(username_header.decode("utf-8").strip())
            username = client_socket.recv(username_length).decode("utf-8")
            
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf-8").strip())
            message = client_socket.recv(message_length).decode("utf-8")
            
            # Decryption add here


            print(f"{username}> {message}")
                
        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error', str(e))
                error_code = str(e)
                if error_code == "[Errno 32] Broken pipe":
                    self_manage()
                sys.exit()
            continue
                
        except Exception as e:
            print('General error', str(e))
            sys.exit()

###########################-- Multithreading Setup --#################################
## Main Setup that will be run on start up of script                                ##
######################################################################################
# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

# Do next that is in the queue (First thread handles connections, Second Thread sends commands)                   
def work():
    while True:
        x = queue.get()
        if x == 1:
            main_sensor()
        if x == 2:
            security_protocalls()
            
        queue.task_done()

def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    
    queue.join()

################################-- Main Setup --######################################
## Main Setup that will be run on start up of script                                ##
######################################################################################

if __name__ == "__main__": 
    connection()
    create_workers()
    create_jobs()

    