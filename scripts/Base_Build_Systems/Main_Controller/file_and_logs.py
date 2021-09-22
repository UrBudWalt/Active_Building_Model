""" 
Hi Welcome to the file_and_logs functions of the....
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
import os
import socket
import logging
import datetime
import configparser

# File variables 
filename = "settings.ini"
config = configparser.ConfigParser()

##########################--  Client File System --###################################
## function check settings file is designed to check if file is present and if not  ##
## it will create the file with the hardcoded data, this is not a good way of doing ##
## it but can be changed to allow user input later on.                              ##
######################################################################################
def check_setting_file():
    fileStatus = os.path.isfile(filename)
    if fileStatus:
        message = "Server Info file found"
        write_to_log('info',message)
    else:
        print("No setting file found in directry..")
        print("Starting setup..")
        create_settings()

def create_settings():
    server_IP = input("Please input IP address of Server: ")
    server_Port = input("Please input Port of Server: ")
    x = datetime.datetime.now()
    date = get_date("date")
    config['SERVER_INFO'] = {'server_ip': server_IP,
                        'server_port': server_Port,
                        'last_changed': date}

    with open(filename, 'w') as configfile:
        config.write(configfile)

def ip_continuity():
    local_IP = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] 
                if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), 
                s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
    
    config.read(filename)
    server_info = config['SERVER_INFO']
    fileIP = server_info['server_ip']
    
    if str(fileIP) != str(local_IP):
        message = "IP error Local IP: " + local_IP + " doesnt match stored IP: " + fileIP
        print(message)
        print("This has been noted")
        write_to_log('error',message)

        responce = input("Do you wish to update stored IP? Note on response of N server will shut down. (Y/N): ")
        if responce == "Y":
            config.read(filename)
            config.set('SERVER_INFO', 'server_ip', local_IP)
            with open(filename, 'w') as configfile:
                config.write(configfile)
        else:
            print("Shutting Down, please check IP or update to new one")
            message = "User requested server shutdown due to IP validation error. Local IP: " + local_IP + " stored IP: " + fileIP
            print(message)
            write_to_log('info',message)
            exit()
    else:
        message = "IP Local IP: " + local_IP + " matchs stored IP: " + fileIP
        write_to_log('info',message)

#############################-- Log File management --################################
## Designateds path for file creation for logs                                      ##
## Each day has its own folder                                                      ##
## Log files are create by date and all infromation is logged by time               ##
## Files should be zipped every Monday for the past week                            ##
######################################################################################

def get_date(reqType):
    # Gets the time of the event from the local device
    x = datetime.datetime.now()

    if reqType == "log_file":

        # Gets day, month and year for file creation of the daily file for the log
        day = x.strftime("%d")
        month = x.strftime("%m")
        year = x.strftime("%Y")

        # combindes day, month and year for directory name
        dirNameDate = day + '_' + month + '_' + year
        return dirNameDate
    
    # Any date is requested is conducted here
    elif reqType == "date":
        date = x.strftime("%c")
        return date
    
    # Time of log message is genrated here
    elif reqType == "time":
        hour = x.strftime("%H")
        mins = x.strftime("%M")
        seconds = x.strftime("%S")

        # combindes hour, mins and seconds
        time = str(hour + ':' + mins + ':' + seconds)
        return time

def get_path():
    str1=os.getcwd()
    str2=str1.split('\\')
    n=len(str2)
    system_dir = str2[n-1]

    dirNameDate = get_date("log_file")

    # path for log folder creation
    path = system_dir + '/Logs/' + dirNameDate

    return path

def check_log_folder():
    path = get_path()
    dirNameDate = get_date("log_file")
    logFileName = "log_" + str(dirNameDate) + ".log"

    filename = path +'/'+ logFileName
    fileStatus = os.path.isfile(filename)

    if fileStatus:
        message = "Log file check and found"
        write_to_log('info',message)
    else:
        print("No log file found in directry..")
        print("running create function now")
        create_log_folder()

def create_log_folder():
    # Log file directories are created daily and are zipped in groups of weeks Mon-Sun
    # Log Files are created each day
    path = get_path()

    try:
        os.makedirs(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
        write_to_log("error", "Failed created log file directory %s" % path)
    else:
        write_to_log("info", "Successfully created the directory %s" % path)

# Write to log file function  
def write_to_log(alert,message):

    # Get file path location from get_path function
    path = get_path()

    # requests date combinations
    dirNameDate = get_date("log_file")

    # Names log File
    logFileName = "log_" + str(dirNameDate) + ".log"
    time = get_date("time")

    logging.basicConfig(filename= path +'/'+ logFileName, filemode='a', level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')
    
    message = time + " - " + message

    # Checks the type of log message recived 
    if alert == "debug":
        logging.debug(message)
    elif alert == "info":
        logging.info(message)
    elif alert == "warning":
        logging.warning(message)
    elif alert == "error":
        logging.error(message)