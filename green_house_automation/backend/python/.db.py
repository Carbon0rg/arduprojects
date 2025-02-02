import sqlite3

def get_db_connection():
    conn = sqlite3.connect('green_house_automation/backend/db/testdb.db')
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS data
        (key TEXT, remote TEXT, current TEXT)
    ''')
    #temperature
    conn.execute('INSERT INTO data (key, remote, current) VALUES (?,?,?)', 
                 ('temperature', "35", "35"))
    #humidity
    conn.execute('INSERT INTO data (key, remote, current) VALUES (?,?,?)', 
                    ('humidity', "25", "15"))
    #light
    conn.execute('INSERT INTO data (key, remote, current) VALUES (?,?,?)', 
                    ('light', "100", "100"))
    #soil_moisture
    conn.execute('INSERT INTO data (key, remote, current) VALUES (?,?,?)', 
                    ('soil_moisture', "100", "100"))
    #fire
    conn.execute('INSERT INTO data (key, remote, current) VALUES (?,?,?)', 
                    ('fire', "0", "0"))
    #intrusion
    conn.execute('INSERT INTO data (key, remote, current) VALUES (?,?,?)', 
                    ('intrusion', "0", "0"))
    #gas_leak
    conn.execute('INSERT INTO data (key, remote, current) VALUES (?,?,?)', 
                    ('gas_leak', "0", "0"))
    #gas_leak
    conn.execute('INSERT INTO data (key, remote, current) VALUES (?,?,?)', 
                    ('pump_state', "0", "0"))
    #gas_leak
    conn.execute('INSERT INTO data (key, remote, current) VALUES (?,?,?)', 
                    ('cooler_state', "0", "0"))
    #gas_leak
    conn.execute('INSERT INTO data (key, remote, current) VALUES (?,?,?)', 
                    ('cooler_fan_state', "0", "0"))
    #gas_leak
    conn.execute('INSERT INTO data (key, remote, current) VALUES (?,?,?)', 
                    ('light_state', "0", "0"))
    #gas_leak
    conn.execute('INSERT INTO data (key, remote, current) VALUES (?,?,?)', 
                    ('heater_fan_state', "0", "0"))
    conn.commit()
    conn.close()


create_table()
print("FINISHED")
