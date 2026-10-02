# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 13:14:15 2026

@author: mikisilv
"""

from blacs.device_base_class import DeviceTab
from user_devices.LaserFreqIntermediateDevice.blacs_worker import LaserFreqIntermediateDeviceWorker

import labscript_utils.h5_lock
import h5py
from labscript_utils import dedent

class LaserFreqIntermediateDeviceTab(DeviceTab):       
    def initialise_GUI(self):
        self.connection_table_properties = self.settings['connection_table'].find_by_name(self.device_name).properties
        self.ip = self.connection_table_properties.get('ip')
        self.port = self.connection_table_properties.get('port')

        # Create and set the primary worker
        self.create_worker(
            "main_worker",
            'user_devices.LaserFreqIntermediateDevice.blacs_worker.LaserFreqIntermediateDeviceWorker',
            {
                'name':self.device_name,
                'ip': self.ip,
                'port': self.port
            }
        )
        self.primary_worker = "main_worker"