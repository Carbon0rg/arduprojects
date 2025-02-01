import serial
from time import sleep
import sqlite3
from dbupdate import db  # Assuming this module exists and handles database interactions
import ttycheck  # Assuming this module exists and provides the USB path

def map_value(x, in_min, in_max, out_min, out_max):
    """Maps a value from one range to another."""
    try:
        x = float(x)  # Attempt to convert x to a float for calculations
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    except ValueError:
        print(f"Invalid input for map_value: {x}")
        return None  # Or handle the error as needed


def write_read(x, board):
    """Writes to the serial port and reads the response."""
    try:
        board.write(bytes(x + '\n', 'utf-8'))
        sleep(0.2)  # Allow time for the Arduino to respond
        line = board.readline().decode('utf-8').rstrip()
        return line
    except serial.SerialException as e:
        print(f"Serial port error: {e}")
        return None
    except UnicodeDecodeError as e:
        print(f"Decoding error: {e}")
        return None
    except Exception as e: # Catch any other potential errors during read/write
        print(f"An unexpected error occurred during serial communication: {e}")
        return None

def read_and_update():
    """Reads sensor data and updates the database."""
    arduino = None  # Initialize arduino outside the try block for proper closing
    try:
        port = ttycheck.usb_path()
        if port is None:
            print("No USB device found. Check connection and ttycheck module.")
            return  # Exit early if no port is found

        arduino = serial.Serial(port=port, baudrate=9600, timeout=4)

        sensor_data = {} # Store sensor data in a dictionary for easier handling

        sensor_names = ["temperature", "humidity", "moisture", "light", "fire", "intrusion", "gas_sensor"]
        commands = ['1', '2', '3', '4', '5', '6', '7']

        for name, command in zip(sensor_names, commands):
            reading = write_read(command, arduino)
            print(f"{name.capitalize()}: {reading}")

            # Attempt to convert to float, handle errors gracefully
            try:
                sensor_data[name] = float(reading) if reading is not None else None
            except (ValueError, TypeError):
                print(f"Invalid reading for {name}: {reading}")
                sensor_data[name] = None  # Store None if conversion fails

        if arduino:  # Close only if the port was successfully opened
            arduino.close()

        # Check if all readings are valid before updating the database
        if all(value is not None for value in sensor_data.values()):
            try:
                db.connect()  # Ensure db.connect() is defined in your dbupdate module
                db.update(**sensor_data)  # Pass the dictionary as keyword arguments
                print("Database updated successfully.")
            except sqlite3.Error as e:
                print(f"Database error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred during database update: {e}")
        else:
            print("Some sensor readings are invalid. Database not updated.")

    except serial.SerialException as e:
        print(f"Serial port error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:  # Ensure arduino is closed even if an exception occurs
        if arduino and arduino.is_open:
            arduino.close()

while True:
    read_and_update()
    sleep(5)