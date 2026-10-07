# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 13:25:45 2026

@author: mikisilv
"""

from blacs.device_base_class import DeviceTab
from user_devices.MokuGo_AIO.blacs_worker import MokuGoAIOWorker

import labscript_utils.h5_lock
import h5py
from labscript_utils import dedent

class CleverScope_CS328ATab(DeviceTab):       
    def initialise_GUI(self):
        connection_table = self.settings['connection_table']
        properties = connection_table.find_by_name(self.device_name).properties           
        
        self.serialNumber = str(self.settings['connection_table'].find_by_name(self.settings["device_name"]).BLACS_connection)

        # Create and set the primary worker
        self.create_worker(
            "main_worker",
            'user_devices.CleverScope_CS328A.blacs_worker.CleverScope_CS328AWorker',
            {
                'name':self.device_name,
                'serialNumber': self.serialNumber,
                'num_AI': properties['num_AI'],
                'allowed_analog_chan': properties['allowed_analog_chan'],
                'startTime' : properties['startTime'],
                'stopTime' : properties['stopTime'],
                'minVoltage_a' : properties['minVoltage_a'],
                'maxVoltage_a' : properties['maxVoltage_a'],
                'minVoltage_b' : properties['minVoltage_b'],
                'maxVoltage_b' : properties['maxVoltage_b'],
                'numSamples' : properties['numSamples'],
                'maximumSamples' : properties['maximumSamples'],
                'frameNum' : properties['frameNum'],
                'triggerChannel' : properties['triggerChannel'],
                'triggerLevel': properties['triggerLevel'],
                'triggerMode': properties['triggerMode'],
                'coupling': properties['coupling']}
            )
        self.primary_worker = "main_worker"
        
        
        
        