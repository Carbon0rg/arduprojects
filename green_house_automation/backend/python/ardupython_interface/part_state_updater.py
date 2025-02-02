from dbupdate import db
import time
from datetime import datetime as dt
import serial
import ttycheck


arduino = serial.Serial(port=ttycheck.usb_path(), baudrate=9600,timeout=1)

databaseobj = db()

def write_read(x):
    try:
        arduino.write(bytes(x, "utf-8"))
        time.sleep(1)
        result = arduino.readall().decode("utf-8").rstrip()
        int_value = int(result)
        return int_value
    except Exception as e:
        print("Error: ", e)


class parts:
    def pump(self, new_state:int):
        if new_state == 1:

            pump_state = write_read('8')
            if pump_state is not None:
                databaseobj.db_update_part_state(pump_state = pump_state)

        if new_state == 0:

            pump_state = write_read('9')
            if pump_state is not None:
                databaseobj.db_update_part_state(pump_state = pump_state)
    
    def cooler_fan(self, new_state:int):
        if new_state == 1:

            cooler_fan_state = write_read('10')
            if cooler_fan_state is not None:
                databaseobj.db_update_part_state(cooler_fan_state = cooler_fan_state)

        if new_state == 0:

            cooler_fan_state = write_read('11')
            if cooler_fan_state is not None:
                databaseobj.db_update_part_state(cooler_fan_state = cooler_fan_state)

    def temp_control(self, new_state:int):
        if new_state == 1:

            cooler_state = write_read('12')
            if cooler_state is not None:
                databaseobj.db_update_part_state(cooler_state = cooler_state)

        if new_state == 0:

            cooler_state = write_read('13')
            if cooler_state is not None:
                databaseobj.db_update_part_state(cooler_state = cooler_state)

    def heater_fan(self, new_state:int):
        if new_state == 1:

            heater_fan_state = write_read('14')
            if heater_fan_state is not None:
                databaseobj.db_update_part_state(heater_fan_state = heater_fan_state)

        if new_state == 0:

            heater_fan_state = write_read('15')
            if heater_fan_state is not None:
                databaseobj.db_update_part_state(heater_fan_state = heater_fan_state)
    
    def light_control(self, level):
        time_now = dt.now()
        hour = time_now.hour
        light_state = write_read("16")
        if light_state == 1:
            if hour > 20:
                    databaseobj.db_update_part_state(light_state = 0)
                    light_is_on = write_read("0")
                    print("light state: ",light_is_on)
            
            else:
                # databaseobj.db_update_part_state(light_state = str(light_state))
                light_is_on = write_read(str(level))
                if light_is_on == 0:
                    databaseobj.db_update_part_state(light_state = 0)
                    print("light state: ",light_is_on)
                else:
                    databaseobj.db_update_part_state(light_state = str(light_state))
                    print("light state: ",light_is_on)
                # databaseobj.db_update_part_state(light_state = 0)
        else:
            print("Arduino Responded with errors")

            
    
    def calibrate(self):
        """Calibrates the sensors by deleting the first reply and flushing the buffers"""
        #print("\033[31m\033[1mcalibrating")
        write_read('15')
        write_read('11')
        write_read('13')
        arduino.flushInput()
        arduino.flushOutput()
        #print("Finished Calibration")


