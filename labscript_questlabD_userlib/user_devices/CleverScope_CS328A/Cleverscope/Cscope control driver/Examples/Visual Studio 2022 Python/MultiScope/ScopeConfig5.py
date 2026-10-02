'''
Cleverscope Configuration File
Configuration: 1-unit setup
RHC 2025 12 06
'''
from T_InterfaceSpec import T_Interface
from T_AcquireSpec import  T_TrigChannel


########### Configuration Variables
Debug = False  # Set to True for debug mode

# Common acquisition parameters for all units
StartTime = -0.005      # -5ms
StopTime = 0.005        # +5ms
FrameNum = 0
NumSamples = 10000
MaximumSamples = 10000
TriggerSource = T_TrigChannel.T_TrigChan_ChanA
TriggerLevel = 0.3


########### Global Connection Settings
# Set the interface source for all scopes

# InterfaceSource = T_Interface.T_Interface_USBFirstFound
InterfaceSource = T_Interface.T_Interface_EthernetFirstFound
# InterfaceSource = T_Interface.T_Interface_EthernetIPAddress
# InterfaceSource = T_Interface.T_Interface_EthernetOrUSBUseSerialNumber
# InterfaceSource = T_Interface.T_Interface_EthernetOrUSBFirstFound


########### Scope Configuration Table
# Define all scopes here - add or remove entries as needed
ScopeConfigs = [
    {
        'UnitName': 'Unit_A',
        'UnitNo' : 0,
        'IPAddr': '203.109.232.203',
        'TCP_Port': 54270,
        'SerialNumber': 'IW10210',
        'ProbeMinVoltage': -2.5,
        'ProbeMaxVoltage': 2.5,
        'ProbeAGain': 'x1',
        'ProbeBGain': 'x1',
        'ProbeCGain': 'x1',
        'ProbeDGain': 'x1',
    },
    {
        'UnitName': 'AcquisitionUnitB',
        'IPAddr': '203.109.232.203',
        'TCP_Port': 55270,
        'SerialNumber': 'JX10339',
        'TriggerSource': 'UnitATriggerChannel',
        'TriggerLevel': 0.5,
        'ProbeMinVoltage': -2.5,
        'ProbeMaxVoltage': 2.5,
        'ProbeAGain': 'x1',
        'ProbeBGain': 'x1',
        'ProbeCGain': 'x1',
        'ProbeDGain': 'x1',
    },
    {
        'UnitName': 'AcquisitionUnitC',
        'IPAddr': '203.109.232.203',
        'TCP_Port': 56270,
        'SerialNumber': 'JX10340',
        'TriggerSource': 'UnitATriggerChannel',
        'TriggerLevel': 0.5,
        'ProbeMinVoltage': -2.5,
        'ProbeMaxVoltage': 2.5,
        'ProbeAGain': 'x1',
        'ProbeBGain': 'x1',
        'ProbeCGain': 'x1',
        'ProbeDGain': 'x1',
    },
    {
        'UnitName': 'AcquisitionUnitD',
        'IPAddr': '203.109.232.203',
        'TCP_Port': 57270,
        'SerialNumber': 'JX10338',
        'TriggerSource': 'UnitATriggerChannel',
        'TriggerLevel': 0.5,
        'ProbeMinVoltage': -2.5,
        'ProbeMaxVoltage': 2.5,
        'ProbeAGain': 'x1',
        'ProbeBGain': 'x1',
        'ProbeCGain': 'x1',
        'ProbeDGain': 'x1',
    },
    {
        'UnitName': 'AcquisitionUnitE',
        'IPAddr': '203.109.232.203',
        'TCP_Port': 58270,
        'SerialNumber': 'JX10333',
        'TriggerSource': 'UnitATriggerChannel',
        'TriggerLevel': 0.5,
        'ProbeMinVoltage': -2.5,
        'ProbeMaxVoltage': 2.5,
        'ProbeAGain': 'x1',
        'ProbeBGain': 'x1',
        'ProbeCGain': 'x1',
        'ProbeDGain': 'x1',
    },
]