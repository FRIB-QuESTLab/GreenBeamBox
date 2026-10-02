# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 15:14:12 2026

@author: mikisilv
"""

import serial
import time
from datetime import datetime
import os


class Lakeshore_218:
    def __init__(self, com_str):
        self.ser = serial.Serial(
            port=com_str,
            baudrate=9600,
            bytesize=serial.SEVENBITS,
            parity=serial.PARITY_ODD,
            timeout=2)
        
    def get_single_8channel_temp(self, ser):
        data = []
        for i in range(1,9):
            write_str = 'KRDG?' + str(i) + '\r\n'
            ser.write(write_str.encode('utf-8'))
            data.append(float(ser.readline().decode("utf-8").lstrip("+")))
        return data

    def make_today_string(self):
        now_object = datetime.now()
        today_string = str(now_object.year) + '-' + str(now_object.month) + '-' + str(now_object.day)
        return today_string
    
    def make_timestamp_string(self):
        now_object = datetime.now()
        timestamp_string = str(now_object.hour) + ':' + str(now_object.minute) + ':' + str(now_object.second)
        return timestamp_string
    
    def acquire(self, save_dir, dt=60):
        try:
            os.makedirs(save_dir, exist_ok=True)
            while True:
                file_path = os.path.join(save_dir, f"{self.make_today_string()}.txt")
                with open(file_path, 'a') as f:
                    data = self.get_single_8channel_temp(self.ser)
                    data = [self.make_timestamp_string()] + data
                    f.write(','.join(map(str, data)))
                    f.write('\n')
                    f.close()
                    print(','.join(map(str, data)))
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
    lake_218 = Lakeshore_218(com_str='COM6')
    lake_218.acquire('I:\\QuESTlab\\Data\\GreenBeamBox\\slow_monitoring_acquisition\\lakeshore_218', dt=30)