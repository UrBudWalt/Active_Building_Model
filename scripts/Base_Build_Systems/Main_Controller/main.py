""" 
Hi Welcome to the main controller of the....
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
## - Lift Control                                                                 ##
## - Lighting                                                                     ##
## - Security                                                                     ##
## - Smart Energy (Solar Panels)                                                  ##
## - Misellaneous Functions (Scripts that are needed for simulation)              ##
####################################################################################

Developer Info:
Name: Walter Bassage 
Email: w.bassage@sheffield.ac.uk
Code Version: 0.1v
"""

###############################-- Import Libaries --##################################
## For this network I have used a simple soctet connection to setup a newtork that  ##
######################################################################################
import socket
import select
import pymongo
import threading
import configparser
from queue import Queue
from file_and_logs import write_to_log
from file_and_logs import ip_continuity
from file_and_logs import check_log_folder
from file_and_logs import check_setting_file

###############################--  Variables --#######################################
## For this network I have used a simple soctet connection to setup a newtork that  ##
######################################################################################
HEADER_LENGHT = 10
NUMBER_OF_THREADS = 2
JOB_NUMBER = [1,2]
queue = Queue()

simple_list = [] ## Needs a better name stores clients and reemoves them from this list
clients = {} # List that stores the address of the connected clients
text = [] # Store the recived message from client

# File variables 
filename = "settings.ini"
config = configparser.ConfigParser()

# Mongo Client Address
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["BBSdatabase"]

#############################-- Nework Setup --#######################################
## For this network I have used a simple soctet connection to setup a newtork that  ##
## will allow for other clients to connect to and relay infromation back and forth. ##
## The network will also be able to approve and deny client access based on if the  ##
## IP is known or not. This network is also independent and has no connection to    ##
## the Fit Out System network (This may change just need to check some details)     ##
######################################################################################

def conection():
    global server_socket
    global sockets_list
    global port
    
    # Server IP and Port used for the connections with the clients (hard coded for now)
    config.read(filename)
    server_info = config['SERVER_INFO']
    host = server_info['server_ip']
    port = int(server_info['server_port'])
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allows for reconnection
    
    server_socket.bind((host,port))
    
    server_socket.listen()
    print(f"Server is active on: {host}:{port}")
    
    # List of client (e.g Sockets)
    sockets_list = [server_socket]

###############################-- Client Commands --##################################
## Records client connections anc check to see if client is approved for the        ##
## connection. Functions also listen for incoming messages from clients.            ##
## Server can submit messages back to clients (comands or queries)                  ##
######################################################################################

# Message recived function
def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGHT)
        
        if not len(message_header):
            return False
        
        message_lenght = int(message_header.decode("utf-8").strip())
        return{"header": message_header, "data": client_socket.recv(message_lenght)}
        
    except:
        return False

# This funcion works in tangent with both connection of new clienta as well as monitoring the client messages recived
def recive_data():
    global connections
    global text
    connections = 0
    
    while True:
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
        
        for notified_socket in read_sockets:
            if notified_socket == server_socket:
                client_socket, client_address = server_socket.accept()
                
                user = receive_message(client_socket)
                if user is False:
                    continue
                
                sockets_list.append(client_socket)
                clients[client_socket] = user
                user_ID = user['data'].decode('utf-8')
                client_info = user_ID + ": " + client_address[0] + ": " + str(client_address[1])
                simple_list.append(client_info)
                connections = len(simple_list)
                print(simple_list)

                print(f"Accepted new connection from: {client_address[0]}:{client_address[1]} Username: {user['data'].decode('utf-8')}")
                   
            else:
                message = receive_message(notified_socket)

                if message is False:
                    del_user_ID = clients[notified_socket]['data'].decode('utf-8')
                    matching = [s for s in simple_list if del_user_ID in s]
                    matching = matching[0]
                    print(f"Closed connection from :{clients[notified_socket]['data'].decode('utf-8')}")
                    sockets_list.remove(notified_socket)
                    simple_list.remove(matching)
                    del clients[notified_socket]
                    continue
                
                user = clients[notified_socket]
                
                text.append(f"Recived message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")
                print(text)
                text = []
                
        for notified_socket in exception_sockets: 
            sockets_list.remove(notified_socket)
            del clients[notified_socket]

# Send comands or queries
def send_data(recipients, message):
    if recipients != "all":
        num = 0
        for i in simple_list:
            x = i.split()
            name = x[0].replace(':', '')
            if name != recipients:
                num = num + 1
            else:
                recipient = list(clients.items())[num]
                recipient = {recipient[i]: recipient[i + 1] for i in range(0, len(recipient), 2)}

            for client_socket in recipient:
                message = message.encode('utf-8')
                message_header = f"{len(message):<{HEADER_LENGHT}}".encode('utf-8')
                client_socket.send(message_header + message)
    else:
        # Iterate over connected clients and broadcast message
        for client_socket in clients:
            message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGHT}}".encode('utf-8')
            client_socket.send(message_header + message)

# Check with the server controller if they want to send anything 
def do_something(job):
    if job == "send":
        recipients = input("Which system do you want to contact?: ")
        message = input("What do you want to say?: ")
        send_data(recipients, message)
    elif job == "quit":
        print("Shutting Down, please wait....")
        message = "User requested server shutdown"
        print(message)
        write_to_log('info',message)
        exit()


def check_status():
    print("Hey")

def req_restart():
    print("Hey")

###############################-- Data management --##################################
## Request spicific data from connected Clients or DBs                              ##
## Submit data for storage in related DB                                            ##
## Create file for settings and other required documents                            ##
## Create DB this will be for mutiple tables for known clients and their data       ##
######################################################################################

# This function should run once since the DB should not be created each time the server starts up
def create_DB():
    dblist = myclient.list_database_names()
    if "mydatabase" in dblist:
        print("The database exists.")
    else:
        print("Database Failed to be created") 

# Function submit data to MongaDB based on sender
def submit_data(data):
    # All data will be assigned a id when cataloged and the time of the event recordeded
    if data == "lights":
        Lightcol = mydb["lights"]
        # Room which the lights are active
        # Trigger this could be a sensor, switch, and timer
        # Status was the lights switch on or off
        mydict = { "_id": 1, "time": "time/date", "room": "hallway", "trigger": "switch", "status": "off" }
        Lightcol.insert_one(mydict)

    elif data == "HVAC":
        HVACcol = mydb["HVAC"]
        # 
        mydict = { "_id": 1, "time": "time/date", "function": "surcilate", "temp": "Sideway", "pollution": "Sideway" }
        HVACcol.insert_one(mydict)

    elif data == "EMS":
        EMScol = mydb["EMS"]
        # 
        mydict = { "_id": 1, "name": "Viola", "address": "Sideway 1633" }
        EMScol.insert_one(mydict)    

    elif data == "lift":
        Liftcol = mydb["lift"]
        #
        mydict = { "_id": 1, "name": "Viola", "address": "Sideway 1633" }
        Liftcol.insert_one(mydict)  

    elif data == "security":
        Securitycol = mydb["security"]
        #
        mydict = { "_id": 1, "name": "Viola", "address": "Sideway 1633" }
        Securitycol.insert_one(mydict) 

def search_DB():
    print("Hey")

################################-- Security --########################################
## Encryption Script for sent data comunication                                     ##
## Decryption Script for recived data comunication                                  ##
## Encryption Script for documents stored and DB                                    ##
## Decryption Script for documents stored and DB                                    ##
## Key generation                                                                   ##
######################################################################################

def encrypt():
    print("Hey")

def dencrypt():
    print("Hey")

def key_gen():
    print("Hey")

################################-- Main Setup --######################################
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
            recive_data()
        if x == 2:
            job = input("What do you want to do?: ")
            do_something(job)
            
        queue.task_done()

def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    
    queue.join()

if __name__ == "__main__":
    check_log_folder()
    check_setting_file()
    ip_continuity()
    conection()
    create_workers()
    create_jobs()
    write_to_log("info", "Server Started without errors")
