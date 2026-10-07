import numpy as np
import re

from labscript import config, Device, IntermediateDevice, LabscriptError, set_passed_properties, AnalogIn
from labscript_utils import dedent
from user_devices import ScopeChannel

"""
This device is based on NAQSlab's implementation of the TektronixTDS and 
KeysightXSeries oscilloscopes. 

https://github.com/naqslab/naqslab_devices/blob/master/TektronixTDS/labscript_device.py
"""

class CleverScope_CS328A(IntermediateDevice):
    description = 'Cleverscope CS328A'    
    allowed_children = [ScopeChannel, AnalogIn]
    
    @set_passed_properties(
        property_names={
            'connection_table_properties': [
                'serialNumber', 
                'num_AI',
                'allowed_analog_chan',
                'maximumSamples',
                'frameNum',
                'startTime',
                'stopTime',
                'minVoltage_a',
                'maxVoltage_a',
                'minVoltage_b',
                'maxVoltage_b',
                'numSamples',
                'triggerChannel',
                'triggerLevel',
                'triggerMode',
                'coupling'
            ],
            'device_properties': [
            ]
        }
    )

    def __init__(
            self, 
            name, 
            serialNumber, 
            parent_device, 
            num_AI=2, 
            allowed_analog_chan = ['chA', 'a', 'chB', 'b'],
            trigger_duration=1e-3,
            startTime = -0.02,
            stopTime = 0.02,
            minVoltage_a = -5,
            maxVoltage_a = 5,
            minVoltage_b = -5,
            maxVoltage_b = 5,
            numSamples = int(4e6),
            maximumSamples = int(4e6),
            frameNum = 0,
            triggerChannel = 'ext',
            triggerLevel=0.5,
            triggerMode = 'Normal',
            coupling='DC'):
        '''
        name : str
            Conventional name of device. May be in the context of an experiment.
        serialNumber : str
            Typically found in the back of the device. 
        trigger_device : labscript object
            Trigger device. Used by labscript
        trigger_connection : labscript object
            Trigger channel on trigger object. Used by labscript
        num_AI : int
            Number of input channels.
        trigger_duration : float
            ??
        startTime : float
            Acquistion time before trigger. Can be thought of as the left x-lim
            of an oscilloscope screen.
        stopTime : float
            Acquistion time after trigger. Can be thought of as the right x-lim
            of an oscilloscope screen.
        minVoltage : float or int, 
            ??
        maxVoltage : float or int, 
            ??
        numsamples : int, 
            How many data points to collect. This affects time step between 
            data points, for a given time span
        maximumSamples : int, 
            Device model dependent. Typically 4e6 
        frameNum : int, 
            ??
        triggerChannel : str, 
            'Ch A', 'Ch B', or 'ext' for external trigger channel (EXT TR)
        triggerLevel : float, 
            -
        triggerMode : str,
            'Auto', 'Automatic', 'Single', 'Normal', or 'Triggered'. Normal and
            Triggered refer to the same mode of triggering. Auto and Automatic 
            refer to the same mode.
        coupling : str, 
            'AC' or 'DC'.

        Returns
        -------
        None.

        '''
        IntermediateDevice.__init__(self,name,parent_device)
        self.BLACS_connection = serialNumber

        self.serialNumber = serialNumber  # Usually on the back of device.
        self.num_AI = num_AI
        self.allowed_analog_chan = allowed_analog_chan
        self.trigger_duration = trigger_duration
        self.startTime = startTime
        self.stopTime = stopTime
        self.minVoltage_a = minVoltage_a
        self.maxVoltage_a = maxVoltage_a
        self.minVoltage_b = minVoltage_b
        self.maxVoltage_b = maxVoltage_b
        self.numSamples = numSamples
        self.maximumSamples = maximumSamples  # model dependent. Typically 4 million.
        self.frameNum = frameNum
        self.triggerChannel = triggerChannel
        self.triggerLevel = triggerLevel
        self.triggerMode = triggerMode
        self.coupling = coupling
        
        # initialize start_time variable
        self.trigger_time = None


    def generate_code(self, hdf5_file):
        """Generates the hardware code from the script and saves it to the
        shot h5 frunmanile. 

        This is called by runmanager when a shot is compiled. The instructions 
        can then be parsed by the transfered_to_buffer method in blacs_worker.py

        Args:
            hdf5_file (str): Path to shot's hdf5 file to save the instructions to.
        """
        IntermediateDevice.generate_code(self, hdf5_file)
        acqs = []
        for channel in self.child_devices:
            ch = channel.connection
            for acq in channel.acquisitions:
                acqs.append(
                        (ch,
                        acq['label'],
                        acq['start_time'],
                        acq['end_time'],
                        acq['wait_label'],
                        acq['scale_factor'] if acq['scale_factor'] is not None else 1.0,
                        acq['units'] if acq['units'] is not None else ''
                    ))
                
        acq_dtype = np.dtype([
            ('connection', 'a32'),     # Hardware channel ID
            ('label', 'a64'),          # Trace name for HDF5 storage
            ('start_time', 'f8'),      # Acquisition start time (s)
            ('end_time', 'f8'),        # Acquisition end time (s)
            ('wait_label', 'a64'),     # Optional wait label
            ('scale_factor', 'f4'),    # Unit conversion scaling factor
            ('units', 'a32')           # Units
        ])
        
        # Convert list to structured array
        acquisition_table = np.array(acqs, dtype=acq_dtype)
        
        # 4. Save the acquisition metadata table into the device's HDF5 group
        group = self.init_device_group(hdf5_file)
        group.create_dataset('Acquisitions', data=acquisition_table)
                                
    def acquire(self,start_time):
        '''Call to define time when trigger will happen for scope.'''
        if not self.child_devices:
            raise LabscriptError('No channels acquiring for trigger {0:s}'.format(self.name))
        else:
            self.parent_device.trigger(start_time,self.trigger_duration)
            self.trigger_time = start_time
    