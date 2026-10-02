# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 15:00:02 2026

@author: mikisilv
"""

"""
Manual: https://www.agilent.com/cs/library/usermanuals/public/Copy%20of%20XGS-600%20Gauge%20Controller.pdf
Specifications: page 51

This file is meant
"""

import serial
import time
from datetime import datetime
import os

class Agilent_xgs_600:
    def __init__(self, com_str):
        # com_str should be a string as: 'COM1', 'COM10', etc
        self.ser = serial.Serial(
            port=com_str,
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1)
        
    def make_timestamp_string(self):
        return datetime.now().strftime("%H:%M:%S")
    
    def make_today_string(self):
        now_object = datetime.now()
        today_string = str(now_object.year) + '-' + str(now_object.month) + '-' + str(now_object.day)
    
        return today_string
    
    def get_gauge_data(self, ser):
        data = []
        fileday = datetime.now().day
    
        ser.reset_input_buffer()
        ser.write("#000F\r".encode("ascii"))
        time.sleep(0.2)
    
        resp = ser.read(ser.in_waiting or 1)
        decoded = resp.decode("ascii", errors="replace").strip()
    
        if decoded.startswith(">"):
            decoded = decoded[1:]
    
        fields = decoded.split(",")
    
        for f in fields:
            try:
                data.append(float(f.strip()))
            except ValueError:
                data.append(0.0) #NOTE: this means channels without readings will be "zero" not "nan" for graphing reasons
    
        return data
    
    def acquire(self, save_dir, dt=60):
        # try:
        #     base_dir = os.path.dirname(os.path.abspath(__file__))
        # except NameError:
        #     base_dir = os.getcwd()
        
        # directory = os.path.join(base_dir, 'data', 'agilent_xgs_600')
        # os.makedirs(directory, exist_ok=True)
        # print("Logging to:", directory)
        try:
            os.makedirs(save_dir, exist_ok=True)
            while True:
                file_path = os.path.join(save_dir, f"{self.make_today_string()}.txt")
                with open(file_path, 'a') as f:
                    data = self.get_gauge_data(self.ser)
                    data = [self.make_timestamp_string()] + data
                    line = ','.join(map(str, data))
                    f.write(line + '\n')
                    print(line)
                time.sleep(dt)
                
        except KeyboardInterrupt:
            print("Loop stopped by user.")
            self.stop()
            f.close()
            
            
    def stop(self):
        self.ser.close()
            
            
if __name__ == "__main__":
    ag_xgs600 = Agilent_xgs_600(com_str='COM8')
    ag_xgs600.acquire('I:\\QuESTlab\\Data\\GreenBeamBox\\slow_monitoring_acquisition\\agilent_xgs_600')