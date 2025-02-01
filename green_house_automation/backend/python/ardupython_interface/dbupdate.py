import sqlite3
import sys
class db:
    def connect():
        try:
            conn = sqlite3.connect('green_house_automation/backend/db/data.db')
            conn.row_factory = sqlite3.Row
            #print('Connected to database')
            return conn
        
        except sqlite3.Error as error:
            print("Error: ", error)
            sys.exit()

    def update(new_temperature :int, new_humidity :int, new_light :int, new_moisture :int, new_fire :int, new_intrusion :int, new_gas_leak :int):
        conn = db.connect()

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

    def db_update_part_state(fan_state :int = None, pump_state :int = None, cooler_state :int = None, light_state :int = None):
        
        conn = db.connect()
        # Fan_State
        
        if fan_state is not None:
            conn.execute('UPDATE data SET current =? WHERE key =?', (fan_state, 'fan_state'))

        #pump_state
        if pump_state is not None:
            conn.execute('UPDATE data SET current =? WHERE key =?', (pump_state, 'pump_state'))

        #cooler_state
        if cooler_state is not None:
            conn.execute('UPDATE data SET current =? WHERE key =?', (cooler_state, 'cooler_state'))
        
        if cooler_state is not None:
            conn.execute('UPDATE data SET current =? WHERE key =?', (light_state, 'light_state'))

        conn.commit()
        conn.close()

        return 0

