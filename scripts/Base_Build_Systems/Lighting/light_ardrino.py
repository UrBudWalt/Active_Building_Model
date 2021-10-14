import time
import pickle
import serial
import datetime

subsystem_ID = "Lights Controller"

relay_dict = {}

filename = 'relay_rooms'

#############################-- Arduino connection --#################################
## This section tries for arduino connection on a specified port                    ##
######################################################################################

try:
    arduino = serial.Serial("/dev/cu.usbmodem143101" ,timeout=1)

except:
    print("Please check port")

###############################-- date and time --####################################
## Time and dates are collected here for sending data to server.                    ##
######################################################################################

def get_date():
    # Gets the time of the event from the local device
    x = datetime.datetime.now()

    date = x.strftime("%c")
    hour = x.strftime("%H")
    mins = x.strftime("%M")
    seconds = x.strftime("%S")

    # combindes hour, mins and seconds
    time = str(hour + ':' + mins + ':' + seconds)
    
    return date, time

###############################-- write and read --###################################
## This fuction submits a specified value to the arduino and waits for a response   ##
##  followed by a response which is returned.                                       ##
######################################################################################

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.30)
    data = arduino.readline()
    return data

###############################-- HVAC Sensors --#####################################
## - Co2 Sensor                                                                     ##
## - Carbon dioxide levels and potential health problems are indicated below:       ##
## - 250-350 ppm: background (normal) outdoor air level.                            ##
## - 350-1,000 ppm: typical level found in occupied spaces with good air exchange.  ##
## – 1,000-2,000 ppm: level associated with complaints of drowsiness and poor air.  ##
##                                                                                  ##
## - Temp Sensor                                                                    ##
##                                                                                  ##
## - Air flow Sensor                                                                ##
##                                                                                  ##
## - Humidity Sensor                                                                ##
##                                                                                  ##
######################################################################################

def pickle_dict(dict):
    outfile = open(filename,'wb')
    pickle.dump(dict,outfile)
    outfile.close()

def get_dict():
    infile = open(filename,'rb')
    new_dict = pickle.load(infile)
    infile.close()

def update_pikle(dict):
    outfile = open(filename,'wb')
    pickle.dump(dict,outfile)
    outfile.close()

def first_light_setup():
    print("test")


def write_file():
    outfile = open(filename,'wb')

    op = 'y'
    check = 'y'
    relay_list = []
        
    while op == 'y':
  
        RoomID = int(input("Enter the room ID: "))
        RoomName = input("Enter room name being added: ")
        while check == 'y':
            Relays = input("Enter relay numbers seprated by a ,: ")
            val_relays = Relays.split(",")
            for i in val_relays:
                if int(i) >16 or int(i) <0:
                    print("Relay " + i +" value is not valid.")
                    correct = input("Enter relay numbers seprated by a ,: ")
                    i = correct
                    relay_list.append(i)
                
                else:
                    relay_list.append(i)
            
            check = 'n'
            print("Relays are ok")
  
        pickle.dump([RoomID, RoomName, relay_list], outfile)
  
        op = input("Do you wish to add additional rooms? (y or n): ")
  
    outfile.close()
  
  
print("Saving details of rooms to the pickle file")
write_file()

def read_file():
    f = open(filename, 'rb')
    while True:
        try:
            L = pickle.load(f)
  
            print("RoomName: ", L[1], "\t\t Relays: ",L[2])
  
        except EOFError:
            print("Completed reading details")
            break
    f.close()
  
  
def update_details():
    f = open(filename, "rb+")
    roomList = []
    read_file()
    op = 'y'
    check = 'y'
    relay_list = []
    
    query_type = input("Would you like to update room name or relays(n or r): ")
    
    if query_type == 'n':
        t_code = int(input("Enter the room ID for the update: "))      
        while True:
            try:
                L = pickle.load(f)
                print(L)
                if L[0] == t_code:
                    RoomName = input("Enter the new desired name for this room: ")
                    L[1] = RoomName
                roomList.append(L)
                
            except EOFError:
                print("Completed Updating details")
                break

        f.seek(0)
        f.truncate()
      
        for i in range(len(roomList)):
            pickle.dump(roomList[i], f)
        else:
            f.close()
        
    
    elif query_type == 'r':
        t_code = int(input("Enter the room ID for the update: "))      
        while True:
            try:
                L = pickle.load(f)
                print(L)
                if L[0] == t_code:
                    while check == 'y':
                        Relays = input("Enter relay numbers seprated by a ,: ")
                        val_relays = Relays.split(",")
                        for i in val_relays:
                            if int(i) >16 or int(i) <0:
                                print("Relay " + i +" value is not valid.")
                                correct = input("Enter relay numbers seprated by a ,: ")
                                i = correct
                                relay_list.append(i)
                            else:
                                relay_list.append(i)

                        check = 'n'
                        print("Relays are ok")
                    
                    L[2] = relay_list
                roomList.append(L)
                
            except EOFError:
                print("Completed Updating details")
                break

        f.seek(0)
        f.truncate()

        for i in range(len(roomList)):
            pickle.dump(roomList[i], f)
        else:
            f.close()
  

def update_room():
    f = open("travel.txt", "wb")
    op = 'y'

    while op == 'y': 
        action_query = input("What action would you like to do? (Update/Remove/Add): ")

        if action_query == "Update":
            print("room list")

            room_query = input("What room would you like to update? "+ "/n" +"Please use the corrisponding number for identification: ")

            print("list Relays assigned to room")

            blink_query = input("What action would you like to do? (Update/Remove/Add): ")

            if blink_query == "N":
                relay_query = input("Please list all relays you wish to assign to" + room_query + ": ")
                print("check relays assigned")
                confirm_relay_query = input("Please list all relays you wish to assign to" + room_query + ": ")
                print("update save file")
                print("changes confirmed and updated to file.")

            elif blink_query == "Y":
                print("send request to blink related relays")
                relay_query = input("Please list all relays you wish to assign to" + room_query + ": ")
                print("check relays assigned")
                confirm_relay_query = input("Please list all relays you wish to assign to" + room_query + ": ")
                print("update save file")
                print("changes confirmed and updated to file.")

        elif action_query == "Remove":
            room_query = input("What action would you like to do? (Update/Remove/Add): ")

        elif action_query == "Add":
            room_query = input("What action would you like to do? (Update/Remove/Add): ")

        else:
            print("Request not understood. Please try again.")

def rec_light_requests():
    print("test")



def sensros(num):
    data = write_read(num)
    msg = data.decode('utf-8')
    message = ""

    if "CO2" in msg:
        co2_val = msg.split(" ")
        co2_val = co2_val[4].split("\r\n")
        co2 = co2_val[0]

        # Carbon dioxide detection
        if float(co2) >= 800:
            date, time = get_date()
            print("Level of Co2 is over productive threshold starting air circulation now.")
            # Send Message layout (subsystem_ID:cal_MQ135:o2:date:time)
            message = str("Co2" + " : " + co2 + " : " + date + " : " + time)
         
        else:
            date, time = get_date()
            message = str("Co2" + " : " + co2 + " : " + date + " : " + time)
        
    elif "Temperature" in msg:
        temp_hum_val = msg.split(" ")
        temp = temp_hum_val[2]
        
        if float(temp) >= 24:
            date, time = get_date()
            print("Temperature is over recomended level for effective productivity starting cooling protocall now.")
            # Start A/C
            message = str("Temp" + " : " + temp + " : " + date + " : " + time)

        elif float(temp) <= 21:
            date, time = get_date()
            print("Temperature is lower than recomended level for effective productivity starting heating protocall now.")
            # Start Heating
            message = str("Temp" + " : " + temp + " : " + date + " : " + time)

    elif "Humidity" in msg:
        temp_hum_val = msg.split(" ")
        hum = temp_hum_val[2]

        if float(hum) > 22:
            date, time = get_date()
            print("Humidity is higher than recomended level for effective productivity starting air circulation protocall now.")
            # Start A/C
            message = str("Humidity" + " : " + hum + " : " + date + " : " + time)

        elif float(hum) < 18:
            date, time = get_date()
            print("Humidity is lower than recomended level for effective productivity starting air circulation protocall now.")
            # Start Heating
            message = str("Humidity" + " : " + hum + " : " + date + " : " + time)
        
    
    return message