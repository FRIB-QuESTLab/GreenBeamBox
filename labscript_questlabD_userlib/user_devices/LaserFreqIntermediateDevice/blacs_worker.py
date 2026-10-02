# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 13:14:41 2026

@author: mikisilv
"""

import numpy as np
from labscript import Device, AnalogOut, AnalogIn, LabscriptError
from blacs.tab_base_classes import Worker
import labscript_utils.h5_lock, h5py
from datetime import datetime
import socket
import re
import time

class LaserFreqIntermediateDeviceWorker(Worker):                      
    def init(self):
        try:  
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.ip, self.port))
            print('connected to: ', self.ip, self.port)
        except socket.error as e:
            print("Failed to connect! Ensure that the laser computer is listening")
            raise e
        s.close()
            

    def _send_msg_laser_frequencies(self, set_freqs, channels):
        '''
        Receives the set_freq array built from HDF5 file and builds a string 
        message to send to the the Labview laser control software running on 
        the laser computer.
        
        set_freqs: 2D numpy array. Columns correspond to different laser 
        channels. Rows correspond to the set frequency instructions.
        channels: 1D list. Contains the laser channels as strings. Ex: '1', 
        '15', etc.
        '''
        if set_freqs is None:
            return None
    
        for j in range(len(channels)):
            ch = channels[j]
            f = set_freqs[ch][0]
            # if f = 0.0, it likely means that a channel was defined in the 
            # connection table but was not used in experimental sequence. Then,
            # do not send msg for this channel.
            if f:  
                try:  
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((self.ip, self.port))
                    print('connected to: ', self.ip, self.port)
                except socket.error as e:
                    print("Failed to connect! Ensure that the laser computer is listening")
                    raise e
                msg = 'CMD:FREQ' + str(ch) + '=' + '{:.6f}'.format(f) + '\r\n'
                s.sendall(msg.encode('utf-8'))
                print('sent: ', msg)
                s.close()
                time.sleep(0.01)
            else:
                continue
            
        return None
                

    def shutdown(self):
        pass

    def program_manual(self,front_panel_values):
        return {}
    
            
    def transition_to_manual(self):
        return True
    
    
    def transition_to_buffered(self,device_name,h5file,initial_values,fresh):
        '''
        Get frequencies for all channels from hdf5 file. They are stored under 
        devices\device_name\SetFrequencies.
        Then, send a string message to laser computer per channel.
        '''
        with h5py.File(h5file, 'r') as hdf5_file:
            group = hdf5_file['devices'][device_name]
            try:
                set_freqs = group['SetFrequencies'][()]  # frequencies are stored as float in THz
                channels = group['SetFrequencies'].dtype.names  # channels are stored as strings. Ex: '1', '15'

            except KeyError:
                set_freqs = None
                channels = None
        
        self._send_msg_laser_frequencies(set_freqs, channels)
       
        return {}
        
    
    def abort_transition_to_buffered(self):
        return True
    
    
    def abort_buffered(self):
        return True
    
    