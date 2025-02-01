import serial
from time import sleep
import sqlite3
from dbupdate import db
import ttycheck
import automated_weather_control_system as awcs

try:
    autowcs = awcs.awcs()
except Exception as e:
    print("Error: ", e)

try:
    arduino = serial.Serial(port=ttycheck.usb_path(), baudrate=9600,timeout=1)

except Exception as e:
    print("Error: ", e)

data_list = list()

        


def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def write_read(x):
    try:
        arduino.write(bytes(x, "utf-8"))
        sleep(1)
        result = arduino.readall().decode("utf-8").rstrip()
        int_value = int(result)
        return int_value
    except Exception as e:
        print("Error: ", e)


def calibrate():
    print("\033[31m\033[1mcalibrating")

    write_read('2')

    write_read('2')

    write_read('3')

    write_read('4')

    write_read('5')

    write_read('6')

    write_read('7')

    autowcs.calibrate_devices()

    
    print("\033[32m\033[1mfinished Calibrating\033[33m\033[1m")


def get_data():
    data_list.clear()
    temperature = write_read("1")
    data_list.append(temperature)
    print("temperature: ", temperature)

    humidity = write_read("2")
    data_list.append(humidity)
    print("humidity: ", humidity )

    soil_moisture = write_read("3")
    print("soil moisture sensor OUT: ", soil_moisture)
    soil_moisture_perc = round(map_value(1005 - soil_moisture, 0, 1005, 0, 100))
    data_list.append(soil_moisture_perc)
    print("soil_moisture: ", soil_moisture_perc)

    light = write_read("4")
    print("light sensor OUT: ", light)
    light_perc = round(map_value(1015-light, 0, 1015, 0, 255))
    data_list.append(light_perc)
    print("light: ", light_perc)

    fire = write_read("5")
    data_list.append(fire)
    print("fire: ", bool(1-fire))

    intrusion = write_read("6")
    data_list.append(intrusion)
    print("intrusion: ", bool(1-intrusion) )

    gas_leak = write_read("7")
    data_list.append(gas_leak)
    print("gas_leak: ", bool(1-gas_leak))
    
    try:
        db.update(*data_list)
        print('DataBase Updated Successfully')
    except sqlite3.Error as e:
        print("SQlite Database connection/updation Error: ", e)

    


    sleep(5)

def start():
    calibrate()
    while True:
        try:
            get_data()
            autowcs.start_tracking()
        except KeyboardInterrupt as e:
            print("exited running process")
            exit(0)
        except serial.SerialException as e:
            print('Serial Connection Error: ', e)




start()
    