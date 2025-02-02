import sqlite3
import sys
import conf
class db:
    def connect(self):
        try:
            conn = sqlite3.connect(conf.db)
            conn.row_factory = sqlite3.Row
            #print('Connected to database')
            return conn
        
        except sqlite3.Error as error:
            print("Error: ", error)
            sys.exit()

    def update(self, new_temperature :int, new_humidity :int, new_moisture :int,new_light :int, new_fire :int, new_intrusion :int, new_gas_leak :int):
        conn = self.connect()

        # Temperature

        conn.execute('UPDATE data SET current =? WHERE key =?', (new_temperature, 'temperature'))

        # Humidity

        conn.execute('UPDATE data SET current =? WHERE key =?', (new_humidity, 'humidity'))

        # Light

        conn.execute('UPDATE data SET current =? WHERE key =?', (new_light, 'light'))

        # Soil Moisture  

        conn.execute('UPDATE data SET current =? WHERE key =?', (new_moisture, 'soil_moisture'))

        # Fire

        conn.execute('UPDATE data SET current =? WHERE key =?', (new_fire, 'fire'))

        # Intrusion

        conn.execute('UPDATE data SET current =? WHERE key =?', (new_intrusion, 'intrusion'))   
        
        # Gas Alert# Database update (handle potential None values)
        
        conn.execute('UPDATE data SET current =? WHERE key =?', (new_gas_leak, 'gas_leak'))
        

        conn.commit()
        conn.close()

    def db_update_part_state(self, heater_fan_state: int = None, pump_state: int = None, cooler_state: int = None, light_state: int = None, cooler_fan_state :int = None):
        conn = self.connect()

        # Fan State
        if heater_fan_state is not None:
            conn.execute('UPDATE data SET current = ? WHERE key = ?', (str(heater_fan_state), 'heater_fan_state'))

        if cooler_fan_state is not None:
            conn.execute('UPDATE data SET current = ? WHERE key = ?', (str(cooler_fan_state), 'cooler_fan_state'))

        # Pump State
        if pump_state is not None:
            conn.execute('UPDATE data SET current = ? WHERE key = ?', (str(pump_state), 'pump_state'))

        # Cooler State
        if cooler_state is not None:
            conn.execute('UPDATE data SET current = ? WHERE key = ?', (str(cooler_state), 'cooler_state'))

        # Light State
        if light_state is not None:
            conn.execute('UPDATE data SET current = ? WHERE key = ?', (str(light_state), 'light_state'))

        conn.commit()
        conn.close()

        return 0