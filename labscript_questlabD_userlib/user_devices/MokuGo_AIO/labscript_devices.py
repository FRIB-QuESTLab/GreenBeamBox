import numpy as np
import re

from labscript import config, Device, IntermediateDevice, AnalogIn, AnalogOut, StaticAnalogOut, LabscriptError, set_passed_properties
from labscript_utils import dedent

class MokuGoAIO(IntermediateDevice):
    description = 'MokuGo Analog Output'    
    allowed_children = [StaticAnalogOut, AnalogIn]
    trigger_duration = 1e-3


    def __init__(self, name, parent_device, ip6, clock_terminal='Input2'):
        '''VISA_name can be full VISA connection string or NI-MAX alias.
        Trigger Device should be fast clocked device. '''
        self.BLACS_connection = ip6
        IntermediateDevice.__init__(self, name, parent_device)
        

    # The code below is borrowed and modified from the labscript source code for 
    # labscript-devices/labscript_devices/NI_DAQmx/labscript_devices.py

    def generate_code(self, hdf5_file):

        """Generates the hardware code from the script and saves it to the
        shot h5 frunmanile. 

        This is called by runmanager when a shot is compiled. The instructions 
        can then be parsed by the transfered_to_buffer method in blacs_worker.py

        Args:
            hdf5_file (str): Path to shot's hdf5 file to save the instructions to.
        """
        IntermediateDevice.generate_code(self, hdf5_file)
        analogs = {}
        inputs = {}
        for device in self.child_devices:
            if isinstance(device, StaticAnalogOut):
                analogs[device.connection] = device
            elif isinstance(device, AnalogIn):
                inputs[device.connection] = device
            else:
                raise TypeError(device)

        clockline = self.parent_device
        times = clockline.parent_device.times[clockline]
        AO_table = self._make_analog_out_table(analogs, times)

        grp = self.init_device_group(hdf5_file)
        if AO_table is not None:
            print(AO_table)
            grp.create_dataset('AO', data=AO_table, compression=config.compression)

    
            
    def _make_analog_out_table(self, analogs, times):
        """
        Collect analog output data and create the output array.
        For each channel, there is a 1D array containing output voltage values 
        as a timeseries.
        
        The timing information is stored on the parent clock device.
        """
        if not analogs:
            return None
        n_timepoints = len(times)
        connections = sorted(analogs, key=self.split_conn_AO)
        dtypes = [(c, np.float32) for c in connections]
        analog_out_table = np.empty(n_timepoints, dtype=dtypes) 
        for connection, output in analogs.items():
            analog_out_table[connection] = output.raw_output
        return analog_out_table
    
    
    def split_conn_AO(self, connection):
        """Return analog output number of a connection string such as 'ao1' as an
        integer, or raise ValueError if format is invalid"""
        try:
            split_str = []
            for i in re.split(r'(\d+)', connection):
                split_str.append(i) if i else None
                
            return int(split_str[-1])

        except (ValueError, IndexError):
            msg = """Analog output connection string %s does not match format 'ao<N>' for
                integer N"""
            raise ValueError(dedent(msg) % str(connection))