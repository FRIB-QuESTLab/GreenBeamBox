# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 15:56:03 2026

@author: QUESTLAB
"""

import serial
import time
from datetime import datetime
import os


class Mks_902b:
    def __init__(self, com_str, address):
        self.ser = serial.Serial(
            port=com_str,
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=2)
        
        self.address = address


    def get_pressure(self, ser, address):  # check on pressure gauge settings to find the address (number between 001 to 253). Use address 254 if address is not known
        write_str = '@' + address + 'PR4?' + ';FF'  # query pressure with 4 digit precision
        ser.write(write_str.encode('utf-8'))
        response = ser.readline().decode("utf-8")
        out = response[-11:-3]  # remove #xxxACK____;FF from message
            
        return out
    
    
    def make_today_string(self):
        now_object = datetime.now()
        today_string = str(now_object.year) + '-' + str(now_object.month) + '-' + str(now_object.day)
    
        return today_string
    
    
    def make_timestamp_string(self):  # returns timestamp in hour:minute:second format. Uses military 24hr format. Example: '1:14:46', '13:20:56', etc. 
        now_object = datetime.now()
        timestamp_string = str(now_object.hour) + ':' + str(now_object.minute) + ':' + str(now_object.second)
        return timestamp_string
    
    
    def acquire(self, save_dir, dt):        
        try:
            os.makedirs(save_dir, exist_ok=True)
            while True:
                file_path = os.path.join(save_dir, f"{self.make_today_string()}.txt")
                with open(file_path, 'a') as f:
                    data = self.get_pressure(self.ser, self.address)
                    data = self.make_timestamp_string() + ',' + data
                    f.write(data + '\n')
                    f.close()
                    print(data)
                    time.sleep(dt)  # seconds
        
        except KeyboardInterrupt:
            print("Loop stopped by user.")
            self.stop()
            f.close()
        
        except ValueError:
            print("Value Error, check if Lakeshore device is disconnected from computer")
            self.stop()
            f.close()
            
    def stop(self):
        self.ser.close()
        
        
if __name__ == "__main__":
    mks_902b = Mks_902b(com_str='COM9', address='253')
    mks_902b.acquire('I:\\QuESTlab\\Data\\GreenBeamBox\\slow_monitoring_acquisition\\mks_902b', dt=60)