import os
import sys

def usb_path():
    if os.path.exists('/dev/ttyUSB0') == True:
        return "/dev/ttyUSB0"

    elif os.path.exists('/dev/ttyUSB1') == True:
        return "/dev/ttyUSB1"
    
    elif os.path.exists('/dev/ttyUSB2') == True:
        return "/dev/ttyUSB2"
    
    else:
        sys.exit(f"Error: Arduino Not Connected to any port")
        