# (TEST FILE DO NOT RELEASE ONCE DONE)



# Importing Libraries
import serial
import time
arduino = serial.Serial("/dev/cu.usbmodem143101" ,timeout=1)

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.10)
    data = arduino.readline()
    return data

while True:
    num = input("Enter a number: ") # Taking input from user
    value = write_read(num)
    if value != "":
        print(value) # printing the value
    else:
        time.sleep(0.05)
        value = write_read(num)
        print(value) # printing the value


# # Calls value
# # while True:
#     # data_request = input("Enter a number: ") # Taking input from user
#     value = recive_Readings(data_request)
#     # print(value) # printing the value

#     # raw_msg = arduino.readline()
#     # msg = raw_msg.decode('utf-8')


#     if 1 == data_request:
#         raw_data = value.split(" ")
#         striped_val = raw_data[4].split("\r\n")
#         fin_data = striped_val[0]
        
    
#     elif 2 == data_request:
#         raw_data = value.split(" ")
#         fin_data = raw_data[2]


#     elif 3 == data_request:
#         raw_data = value.split(" ")
#         fin_data = raw_data[5]

#     return fin_data