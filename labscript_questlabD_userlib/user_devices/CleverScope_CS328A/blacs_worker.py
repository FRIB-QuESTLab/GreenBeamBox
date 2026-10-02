import numpy as np
from moku.instruments import MultiInstrument, WaveformGenerator, Oscilloscope
from labscript import Device, AnalogOut, AnalogIn, LabscriptError
from blacs.tab_base_classes import Worker
import labscript_utils.h5_lock, h5py
from datetime import datetime

# CleverScope packages
import sys
sys.path.append('I:\\QuESTlab\\daq and control software\\labscript_questlabD_userlib\\user_devices\\CleverScope_CS328A\\Cleverscope\\Cscope control driver\\Examples\\Visual Studio 2022 Python\\MultiScope')

import CleverscopeInterface
from T_AcquireSpec import T_AcquireSpec, T_AcquireAction, T_SigGenWaveform, T_LinkPort, T_TrigChannel
from T_ChannelSpec import T_ChannelSpec, T_Probe, T_GlobalFilter, T_PreFilter20MHz, T_MA_Filter, T_ExpFilter, T_FilterOption, T_Coupling
from T_InterfaceSpec import T_InterfaceSpec, T_Interface
from T_ReplaySpec import T_ReplaySpec
from T_T0dt import T_T0dt
from CleverscopeClasses import T_CAUStatus, T_Command, T_FunctionCommand, T_LinkMasterSlave, T_TriggeringUnit
from time import sleep, time
import ctypes
import numpy as np 
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt


class CleverScope_CS328AWorker(Worker):
    def GetAndDisplayUnitInfo(self, CscopeUnit):
        FunctionsToCall = ['ID','FirmwareVer','DriverVer','Resolution','FrameLength','Temperature', ]
        for i,info in enumerate(FunctionsToCall):
            CscopeUnit.DoCscopeFunction(ctypes.c_uint16(i),0)
            if info=='DriverVer':
                print("%s: %.3f" %('DLL Version',CscopeUnit.FunctionResult.value))
            else:
                print("%s: %.0f" %(info,CscopeUnit.FunctionResult.value))
                
                
                
    def PrintT0dt(self, Label, CscopeUnit):
        print(Label)
        print("  T0dt.dt: ",CscopeUnit.T0dt.dt)
        print("  T0dt.n: ",CscopeUnit.T0dt.n)
        print("  T0dt.T0: ",CscopeUnit.T0dt.T0)
        print("  T0dt.TTrig: ",CscopeUnit.T0dt.TTrig)
        print("  T0dt.Frame: ",CscopeUnit.T0dt.Frame)
        
        
        
    def init(self):
        if self.triggerChannel[-1].lower() == 'a':
            trigger_chan_object = T_TrigChannel.T_TrigChan_ChanA
        elif self.triggerChannel[-1].lower() == 'b':
            trigger_chan_object = T_TrigChannel.T_TrigChan_ChanB
        elif self.triggerChannel[0:3].lower() == 'ext':
            trigger_chan_object = T_TrigChannel.T_TrigChan_ExtTrigger
        else:
            raise LabscriptError('triggerChannel string cannot be parsed')
                    
        if self.triggerMode.lower() == 'auto' or self.triggerMode.lower() == 'automatic':
            self.trigger_mode_object = T_AcquireAction.T_AcquireAction_Automatic #Choose Single, Automatic, or Triggered
        elif self.triggerMode.lower() == 'single':
            self.trigger_mode_object = T_AcquireAction.T_AcquireAction_Single #Choose Single, Automatic, or Triggered
        elif self.triggerMode.lower() == 'normal' or self.triggerMode.lower() == 'triggered':
            self.trigger_mode_object = T_AcquireAction.T_AcquireAction_Triggered #Choose Single, Automatic, or Triggered
        else:
            raise LabscriptError('triggerMode string cannot be parsed')
        
        if self.coupling.lower() == 'dc':
            coupling_object = T_Coupling.T_Coupling_DC
        elif self.coupling.lower() == 'ac':
            coupling_object = T_Coupling.T_Coupling_AC
        else:
            raise LabscriptError('coupling string cannot be parsed')
        

        self.connection = CleverscopeInterface.Cleverscope(
            UnitNumber=0,
            InterfaceSource = T_Interface.T_Interface_EthernetOrUSBUseSerialNumber,
            IPAddr = '0.0.0.0',  # not using TCP
            TCP_Port = 53270, 
            SerialNumber=self.serialNumber,
            StartTime = self.startTime,
            StopTime =self.stopTime,  
            FrameNum = self.frameNum, 
            NumSamples = self.numSamples,
            MaximumSamples = self.maximumSamples,
            TriggerSource = trigger_chan_object, 
            TriggerLevel = self.triggerLevel, 
            LinkPort = T_LinkPort.T_LinkPort_Debug,
            ProbeMinVoltage = self.minVoltage,
            ProbeMaxVoltage = self.maxVoltage, 
            ProbeAGain = T_Probe.T_Probe_x1,
            ProbeBGain = T_Probe.T_Probe_x1,
            ProbeCGain = T_Probe.T_Probe_x1,
            ProbeDGain = T_Probe.T_Probe_x1,
            ProbeCoupling = coupling_object
        )
        
        self.connection.ConnectToHardware()
        self.connection.WaitForConnectionToComplete(5)
        if self.connection.IsConnected():
            print("______________________________")  # Provide some details of Unit A
            print("Hardware (Unit A) connected OK")
            SerialNumber = self.connection.GetSerialNumber()
            SigGenType = self.connection.GetSigGenType()
            CAUType = self.connection.GetCAUType()
            if (CAUType[:3] == "CS3"):
                CSType = CAUType[:6]
            else:
                CSType = CAUType[:5]
            print("Model:", CAUType,"Serial#:",SerialNumber,"Sig Gen:", SigGenType)
            NumberOfChannels = self.connection.GetNumberOfChannels()
            print("Channels:",NumberOfChannels)
            IPAddressA = self.connection.GetIPAddress()
            if IPAddressA.find('.')<1:
                print ("USB Connected")
            else:
                print("ethernet Connected")
                print("IP Address is ",IPAddressA)
            self.GetAndDisplayUnitInfo(self.connection)

        else:
            raise LabscriptError("Unit A Failed to connect")
            

            
    
    def shutdown(self):
        self.connection.SendCleverscopeCommand(T_Command.T_Command_Close)
        self.connection.SendCleverscopeCommand(T_Command.T_Command_Finish)
        
        
        
    def program_manual(self,front_panel_values):
        return {}
    
    
            
    def transition_to_manual(self):
        # wait for oscilloscope to complete capture:
        LastTime = time()
        UnitA_WaitingForSamples = True
        while UnitA_WaitingForSamples:
            if UnitA_WaitingForSamples:
                if self.connection.CheckForSampleCaptureComplete():
                    UnitA_WaitingForSamples = False
                    print("Sample Capture Complete")

            if time()-LastTime > 1:
                print(".")
                LastTime = time()

            sleep(0.01)
        print('acquisition details:')
        self.PrintT0dt("Unit A:", self.connection)
        
        # get channels that were called to acquire in sequence
        with h5py.File(self.h5file, 'r') as hdf5_file:
            group = hdf5_file['devices'][self.device_name]
            ch_from_h5 = group['Acquisitions']['connection']
        if len(ch_from_h5) == 0:
            print('No acquisitions!')
            return True
        
        # retrieve time data from scope        
        StartTime = self.connection.T0dt.T0
        StopTime  = self.connection.T0dt.T0 + (self.connection.T0dt.n * self.connection.T0dt.dt)
        t = np.arange(start=StartTime, stop=StopTime, step=self.connection.T0dt.dt)

        # from channels found above, retrieve data points
        data_points = {}
        data_types = [('time', 'float')]
        for ch in ch_from_h5:
            ch_str = ch.decode('utf-8')[-1].lower()
            if ch_str == 'a':
                data_types.append((ch.decode('utf-8'),'float'))
                data_points[ch.decode('utf-8')] = np.asarray(self.connection.ChannelAData)[:len(t)]
            elif ch_str == 'b':
                data_types.append((ch.decode('utf-8'),'float'))
                data_points[ch.decode('utf-8')] = np.asarray(self.connection.ChannelBData)[:len(t)]
            else:
                raise LabscriptError('triggerChannel string cannot be parsed')
        data = np.empty(len(t), dtype=data_types)
        data['time'] = t
        for ch in data_points:
            data[ch] = data_points[ch]
            
        # save data in HD5 file under /data/traces/device_name/
        with h5py.File(self.h5file, 'r+') as hdf_file:
            grp = hdf_file.require_group('/data/traces')
            print('Saving traces...')
            grp.create_dataset(self.device_name, data=data)
        
        print('Done!')
        return True
    
    
    
    def transition_to_buffered(self,device_name,h5file,initial_values,fresh):
        self.h5file = h5file  # store this for saving traces
        
        if self.connection.IsConnected():
            print('transitioning to buffered:')
            self.connection.BeginSampleCapture(self.trigger_mode_object);
            print('oscilloscope armed')
            return {}
        else:
            raise LabscriptError('Scope is not connected')
        
        
    
    def abort_transition_to_buffered(self):
        return True
    
    
    
    def abort_buffered(self):
        return True
    
    
    
    # Code below is borrowed and modified from the labscript source code for 
    # labscript-devices/labscript_devices/NI_DAQmx/labscript_devices.py
    # def get_output_tables(self, h5file, device_name):
    #     """Return the AO tables rom the file, or None if they do not exist."""
    #     with h5py.File(h5file, 'r') as hdf5_file:
    #         group = hdf5_file['devices'][device_name]
    #         try:
    #             AO_table = group['AO'][:]
    #         except KeyError:
    #             AO_table = None

    #     return AO_table
    
