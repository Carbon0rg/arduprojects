import dbupdate
import part_state_updater as psu
import time

"""
SNIPPETS

def track_temperature(self):
        self.cursor.execute("SELECT * FROM data WHERE key = 'temperature'")
        temperature_row = self.cursor.fetchall()
        temperature_remote = int(temperature_row[0][1])
        temperature_current = int(temperature_row[0][2])
        if temperature_current > (temperature_remote + 5):
            self.pu.cooler(1)
            self.pu.fan(1)

        elif temperature_current < (temperature_remote - 5):
            self.pu.cooler(0)
            self.pu.fan(0)
"""


class awcs:
    def __init__(self):
        self.pu = psu.parts()
        try:
            self.conn = dbupdate.db.connect()
            self.cursor = self.conn.cursor()
        except Exception as e:
            pass
        #self.pu.calibrate()

    

    
    def track_temperature(self):
        print("Tracking and Maintaning Remote Temperature")
        self.cursor.execute("SELECT * FROM data WHERE key = 'temperature'")
        temperature_row = self.cursor.fetchall()
        temperature_remote = int(temperature_row[0][1])
        temperature_current = int(temperature_row[0][2])
        if temperature_current > (temperature_remote + 10):
            print("Temperature too HIGH")
            self.pu.temp_control(1)
            self.pu.cooler_fan(1)
            self.pu.heater_fan(0)

        elif temperature_current > (temperature_remote + 5):
            print("Temperature HIGH")
            self.pu.temp_control(0)
            self.pu.cooler_fan(1)
            self.pu.heater_fan(0)

        elif temperature_current < (temperature_remote - 10):
            print("Temperature too LOW")
            self.pu.temp_control(1)
            self.pu.heater_fan(1)
            self.pu.cooler_fan(0)
        elif temperature_current < (temperature_remote - 5):
            print("Temperature LOW")
            self.pu.temp_control(0)
            self.pu.heater_fan(1)
            self.pu.cooler_fan(0)

        else:
            print("Temperature is PERFECT for PLANT GROWTH")
            self.pu.temp_control(0)
            self.pu.heater_fan(0)
            self.pu.cooler_fan(0)

    def track_humidity(self):
        print("Tracking and Maintaining Remote Humidity")
        self.cursor.execute("SELECT * FROM data WHERE key = 'humidity'")
        humidity_row = self.cursor.fetchall()
        humidity_remote = int(humidity_row[0][1])
        humidity_current = int(humidity_row[0][2])
        if humidity_current < (humidity_remote - 7):
            print("HUMIDITY LOW")
            self.pu.pump(1)
            #self.pu.humidifier(1)

        elif humidity_current > (humidity_remote + 7):
            print("HUMIDITY HIGH")
            self.pu.pump(0)
            #self.pu.humidifier(0)
        else:
            print("HUMIDITY PERFECT")
            self.pu.pump(0)
            #self.pu.humidifier(0)
            
    
    def track_soil_moisture(self):
        print("Tracking and Maintaining Remote Soil_Moisture")
        self.cursor.execute("SELECT * FROM data WHERE key = 'soil_moisture'")
        soil_moisture_row = self.cursor.fetchall()

        soil_moisture_threshold = int(soil_moisture_row[0][1])  # Threshold from DB
        soil_moisture_current = int(soil_moisture_row[0][2])

        if soil_moisture_current < (soil_moisture_threshold - 5):
            self.pu.pump(1)  # Turn on water pump
            print("Watering plants...")
        else:
            self.pu.pump(0)  # Turn off water pump
            print("Plants have enough water.")

    def track_light_level(self):
        print("Tracking and Maintaining Remote Light Levels")
        self.cursor.execute("SELECT * FROM data WHERE key = 'light'")
        light_row = self.cursor.fetchall()

        light_remote = int(light_row[0][1])  # Threshold from DB
        light_current = int(light_row[0][2])

        if light_current < (light_remote - 15):
            self.pu.light_control(light_remote) # Turn on light
            print("LIGHT level LOW")
        else:
            self.pu.light_control(0)  # Turn off light
            print("LIGHT level OK")
    
    def calibrate_devices(self):
        self.pu.calibrate()
    
    def start_tracking(self):
        print("Starting")
        time.sleep(1.5)
        awcs.track_humidity(self)
        awcs.track_temperature(self)
        awcs.track_soil_moisture(self)
        awcs.track_light_level(self)
