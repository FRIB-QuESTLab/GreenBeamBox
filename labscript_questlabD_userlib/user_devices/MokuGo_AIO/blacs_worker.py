import numpy as np
from moku.instruments import MultiInstrument, WaveformGenerator, Oscilloscope

from labscript import Device, AnalogOut, AnalogIn, LabscriptError
from blacs.tab_base_classes import Worker
import labscript_utils.h5_lock, h5py
from datetime import datetime


class MokuGoAIOWorker(Worker):
    def init(self):
        self.connection = MultiInstrument(self.ip6_address, force_connect=True, platform_id=3)
        self.osc = self.connection.set_instrument(1, Oscilloscope)
        self.wg1 = self.connection.set_instrument(2, WaveformGenerator)
        self.wg2 = self.connection.set_instrument(3, WaveformGenerator)
        self.wg = ('channel 0 does not exist', self.wg1, self.wg2)
        connections = [
            dict(source="Input1", destination="Slot1InA"),
            dict(source="Input2", destination="Slot1InB"),
            dict(source="Slot2OutA", destination="Output1"),
            dict(source="Slot3OutA", destination="Output2"),
        ]
    
        print(self.connection.set_connections(connections=connections))
        
    
    
    def shutdown(self):
        for ch in range(1,self.num_AO+1):
            response = self.wg[ch].generate_waveform(
                channel=ch, 
                type='DC', 
                dc_level=0)
            
            print(response)
        self.connection.relinquish_ownership()
        
        
        
    def program_manual(self,front_panel_values):
        print(datetime.now().strftime("%Y/%m/%d %H:%M:%S"), ': Output controlled by front panel')
        
        for aoi, value in front_panel_values.items():
            ch = int(aoi[-1])    
            response = self.wg[ch].generate_waveform(
                channel=ch, 
                type='DC', 
                dc_level=value)
            print(response)

        return {}
    
    
            
    def transition_to_manual(self):
        print(len(self.oscilloscopedata))
        return True
    
    
    
    def transition_to_buffered(self,device_name,h5file,initial_values,fresh):
        # Store the initial values in case we have to abort and restore them:
        self.initial_values = initial_values

        # Get the data to be programmed into the output tasks:
        AO_table = self.get_output_tables(h5file, device_name)
        
        ch1_static_value = AO_table[0][0]
        ch2_static_value = AO_table[0][1]
        
        self.wg[1].generate_waveform(
            channel=1, 
            type='DC', 
            dc_level=ch1_static_value.item())  # convert from numpy float32 to float
        
        self.wg[2].generate_waveform(
            channel=2, 
            type='DC', 
            dc_level=ch2_static_value.item())  # convert from numpy float32 to float
        
        final_values = {}
        i = 0
        for aoi, value in initial_values.items():
            final_values[aoi] = AO_table[0][i]
            i += 1
            
        self.osc.set_trigger(type='Edge', source='ChannelB', level=2.5, mode='Normal')
        self.osc.set_timebase(-20e-3, 260e-3)
        self.oscilloscopedata = self.osc.get_data()
        
        return final_values
    
    
    
    def abort_transition_to_buffered(self):
        for aoi, value in self.initial_values.items():
            ch = int(aoi[-1])    
            response = self.wg[ch].generate_waveform(
                channel=ch, 
                type='DC', 
                dc_level=value)
            print(response)
        return True
    
    
    
    def abort_buffered(self):
        for aoi, value in self.initial_values.items():
            ch = int(aoi[-1])    
            response = self.wg[ch].generate_waveform(
                channel=ch, 
                type='DC', 
                dc_level=value)
            print(response)
        return True
    
    
    
    def check_status(self):
        '''
        returns a string summarizing the oscillscope settings 
        '''
        return ''
    
    
    
    # Code below is borrowed and modified from the labscript source code for 
    # labscript-devices/labscript_devices/NI_DAQmx/labscript_devices.py
    def get_output_tables(self, h5file, device_name):
        """Return the AO tables rom the file, or None if they do not exist."""
        with h5py.File(h5file, 'r') as hdf5_file:
            group = hdf5_file['devices'][device_name]
            try:
                AO_table = group['AO'][:]
            except KeyError:
                AO_table = None

        return AO_table
    
