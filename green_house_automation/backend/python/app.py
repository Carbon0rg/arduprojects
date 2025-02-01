from flask import Flask, render_template, send_from_directory, request
import sqlite3
#import pandas as pd
import json

app = Flask(__name__, template_folder='../../frontend/web/html/', static_folder='../../frontend/web')

# Database things

def get_db_connection():
    conn = sqlite3.connect('/home/jkschool/Niranjan/projects/arduprojects/green_house_automation/backend/db/data.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS data
        (key TEXT, remote TEXT, current TEXT)
    ''')
    conn.close()

# Serve static files from the frontend/web directory

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('../../frontend/web', path)

# Serve CSS, JavaScript, and images from the frontend/web directory
@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('../../frontend/web/css', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('../../frontend/web/js', path)

@app.route('/res/<path:path>')
def send_res(path):
    return send_from_directory('../../frontend/res', path)

@app.route('/favicon.svg')
def send_favicon():
    return send_from_directory('../../frontend/res/images/favicon', 'green-house_17013259.svg')

@app.route('/control')
def control():
    return render_template('control.html')

@app.route('/home')
def home():
    return render_template('index.html')



# API for getting or posting data


@app.route("/change_data", methods=["POST"])
def post_request_handler():
    conn = get_db_connection()
    data = request.get_json()
    # Temperature
    conn.execute('UPDATE data SET remote =? WHERE key =?', (data["temperature"], 'temperature'))
    print(data["temperature"])
    # Humidity
    conn.execute('UPDATE data SET remote =? WHERE key =?', (data["humidity"], 'humidity'))
    # light
    conn.execute('UPDATE data SET remote =? WHERE key =?', (data["light"], 'light'))
    #soil_moisture
    conn.execute('UPDATE data SET remote =? WHERE key =?', (data["soil_moisture"], 'soil_moisture'))
    conn.commit()
    conn.close()
    response_data = {
        "temperature": data["temperature"],
        "humidity": data["humidity"],
        "light": data["humidity"],
        "soil_moisture": data["soil_moisture"]
    }
    return response_data

@app.route("/get_data", methods=["GET"])
def get_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Execute the query
    #temperature
    cursor.execute("SELECT * FROM data WHERE key = 'temperature'")
    temperature = cursor.fetchall()
    #humidity
    cursor.execute("SELECT * FROM data WHERE key = 'humidity'")
    humidity = cursor.fetchall()
    #light
    cursor.execute("SELECT * FROM data WHERE key = 'light'")
    light = cursor.fetchall()
    #soil_moisture
    cursor.execute("SELECT * FROM data WHERE key = 'soil_moisture'")
    soil_moisture = cursor.fetchall()
    #fire alert
    cursor.execute("SELECT current FROM data WHERE key = 'fire'")
    fire = cursor.fetchall()
    #instrusion alert
    cursor.execute("SELECT current FROM data WHERE key = 'intrusion'")
    intrusion = cursor.fetchall()
    #gas_leak
    cursor.execute("SELECT current FROM data WHERE key = 'gas_leak'")
    gas_leak = cursor.fetchall()


    # Fetch the query result
    unparsed_data = {'temperature': int(temperature[0][2]), 'humidity': int(humidity[0][2]), 'light': int(light[0][2]), 'soil_moisture': int(soil_moisture[0][2]),'temperature_set': int(temperature[0][1]), 'humidity_set': int(humidity[0][1]), 'light_set': int(light[0][1]), 'soil_moisture_set': int(soil_moisture[0][1]), 'fire': int(fire[0][0]), 'intrusion': int(intrusion[0][0]), 'gas_leak': int(gas_leak[0][0])}
    json_result = json.dumps(unparsed_data)
    print(json_result)
    return json_result

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5500)