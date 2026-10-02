# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 13:14:41 2026

@author: mikisilv
"""

import numpy as np
import re

from labscript import config, Device, IntermediateDevice, LabscriptError, set_passed_properties, AnalogIn, StaticDigitalOut, StaticAnalogOut
from labscript_utils import dedent
from user_devices import FrequencyOut

"""
This device is based on NAQSlab's implementation of the TektronixTDS and 
KeysightXSeries oscilloscopes. 

https://github.com/naqslab/naqslab_devices/blob/master/TektronixTDS/labscript_device.py
"""

class LaserFreqIntermediateDevice(Device):
    description = 'IntermediateDevice to couple labscript with current laser frequency control scheme running in Labview VI'    
    allowed_children = [FrequencyOut]
    @set_passed_properties(
        property_names={
            'connection_table_properties': [
                'ip',
                'port',
            ],
        }
    )
    def __init__(self, name, ip, port):
        '''
        name: str, name of device
        ip: str
        port: int, safer to be larger than 5000
        '''
        Device.__init__(self,name,parent_device=None, connection=None)
        self.BLACS_connection = (ip, port)

    def generate_code(self, hdf5_file):
        """Generates the hardware code from the script and saves it to the
        shot h5 file.
    
        This is called automatically when a shot is compiled.
    
        Args:
            hdf5_file (str): Path to shot's hdf5 file to save the instructions to.
        
        Adapted from https://github.com/labscript-suite/labscript-devices/blob/master/labscript_devices/NI_DAQmx/labscript_devices.py#L573
        """
        IntermediateDevice.generate_code(self, hdf5_file)
        

        laser_channels = {}
        for device in self.child_devices:
            if isinstance(device, (FrequencyOut)):
                laser_channels[device.connection] = device
            else:
                raise TypeError(device)           
            
            
        """Collect analog output data and create the output array"""
        dtypes = [(c, np.float64) for c in laser_channels]
        set_freq = np.empty(1, dtype=dtypes) 
        for connection, output in laser_channels.items():
            set_freq[connection] = output.static_value
        grp = self.init_device_group(hdf5_file)
        if set_freq is not None:
            grp.create_dataset('SetFrequencies', data=set_freq, compression=config.compression)