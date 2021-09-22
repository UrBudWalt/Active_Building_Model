import serial
import time
import datetime

subsystem_ID = "HVAC"

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
            # Start A/C
            message = str("Temp" + " : " + temp + " : " + date + " : " + time)

        elif float(temp) <= 21:
            date, time = get_date()
            # Start Heating
            message = str("Temp" + " : " + temp + " : " + date + " : " + time)

    elif "Humidity" in msg:
        temp_hum_val = msg.split(" ")
        hum = temp_hum_val[2]

        if float(hum) > 22:
            date, time = get_date()
            # Start A/C
            message = str("Humidity" + " : " + hum + " : " + date + " : " + time)

        elif float(hum) < 18:
            date, time = get_date()
            # Start Heating
            message = str("Humidity" + " : " + hum + " : " + date + " : " + time)
        
    
    return message