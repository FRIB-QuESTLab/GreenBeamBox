
'''
Changed to a flexible multi scope approach - Capable of 1 - 32 
Configuration in separate ScopeConfigx.py file
RHC 2025 12 06
'''

import CleverscopeInterface
from T_AcquireSpec import T_AcquireSpec, T_AcquireAction, T_SigGenWaveform, T_LinkPort, T_TrigChannel
from T_ChannelSpec import T_ChannelSpec, T_Probe, T_GlobalFilter, T_PreFilter20MHz, T_MA_Filter, T_ExpFilter, T_FilterOption, T_Coupling
from T_InterfaceSpec import T_InterfaceSpec, T_Interface
from T_ReplaySpec import T_ReplaySpec
from T_T0dt import T_T0dt
from CleverscopeClasses import T_CAUStatus, T_Command, T_FunctionCommand, T_LinkMasterSlave, T_TriggeringUnit
from time import sleep, time
import ctypes
# Install these additional Packages:
import platform               
import msvcrt
import numpy as np 
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler

########### SELECT CONFIGURATION FILE HERE
# Change this import to use different configurations
# Options: ScopeConfig1, ScopeConfig2, ScopeConfig3, etc.
import ScopeConfig1 as config

# Import configuration variables
Debug = config.Debug
StartTime = config.StartTime
StopTime = config.StopTime
FrameNum = config.FrameNum
NumSamples = config.NumSamples
MaximumSamples = config.MaximumSamples
TriggerSource = config.TriggerSource
TriggerLevel = config.TriggerLevel
ScopeConfigs = config.ScopeConfigs
InterfaceSource = config.InterfaceSource

########### Probe Gain Mapping
PROBE_GAIN_MAP = {
    'x1': T_Probe.T_Probe_x1,
    'x10': T_Probe.T_Probe_x10,
    'x100': T_Probe.T_Probe_x100,
    'x1K': T_Probe.T_Probe_x1K,
    'x2': T_Probe.T_Probe_x2,
    'x20': T_Probe.T_Probe_x20,
    'x50': T_Probe.T_Probe_x50,
    'x200': T_Probe.T_Probe_x200,
    'Vsat_0_15': T_Probe.T_Probe_Vsat_0_15,
    'Vsat_1_50': T_Probe.T_Probe_Vsat_1_50,
    'Vsat_15_0': T_Probe.T_Probe_Vsat_15_0,
    'Vsat_x2': T_Probe.T_Probe_Vsat_x2
}


########### Plotting Configuration and Functions
# Cleverscope color scheme
cscope_colors = [
    "#FF0000",  # Ch1 – red
    "#0000FF",  # Ch2 – blue
    "#00FF00",  # Ch3 – green
    "#FFA500",  # Ch4 – orange
    "#00FFFF",  # Ch5 – cyan
    "#FF00FF",  # Ch6 – magenta
    "#FFFF00",  # Ch7 – yellow
    "#8B0000",  # Ch8 – dark red
    "#00008B",  # Ch9 – dark blue
    "#006400",  # Ch10 – dark green
    "#B8860B",  # Ch11 – dark goldenrod
    "#008B8B",  # Ch12 – dark cyan
    "#8B008B",  # Ch13 – dark magenta
    "#BDB76B",  # Ch14 – dark khaki
    "#2E8B57",  # Ch15 – sea green
    "#FF4500",  # Ch16 – orange red
    "#4682B4",  # Ch17 – steel blue
    "#32CD32",  # Ch18 – lime green
    "#9400D3",  # Ch19 – dark violet
    "#A52A2A",  # Ch20 – brown
]

# Set chart parameters
params = {
    'text.color': 'white',
    'xtick.color': 'white',
    'ytick.color': 'white',
    'figure.facecolor': 'green',
    'axes.facecolor': '0.7'
}
mpl.rcParams.update(params)

def DrawPlot(units):
    """
    Draw plot for any number of connected Cleverscope units.
    Each unit can have different number of channels.
    
    Args:
        units: Dictionary of connected Cleverscope unit objects
    """
    if not units:
        raise ValueError("No units supplied.")
    
    # ------------------------------------------------------------
    # 1. Build time axis from first unit
    # ------------------------------------------------------------
    first_unit = list(units.values())[0]
    StartTime_plot = first_unit.T0dt.T0
    StopTime_plot = first_unit.T0dt.T0 + (first_unit.T0dt.n * first_unit.T0dt.dt)
    TimeIndex = np.arange(start=StartTime_plot, stop=StopTime_plot, step=first_unit.T0dt.dt)
    
    # ------------------------------------------------------------
    # 2. Build channel table dynamically based on each unit
    # ------------------------------------------------------------
    df = pd.DataFrame(index=TimeIndex)
    
    # Use actual unit names from connected_scopes
    color_index = 0
    
    for unit_name, unit in units.items():
        # Get number of channels for this unit
        num_ch = unit.GetNumberOfChannels()
        
        # Get channel data - try different attribute patterns
        for ch_index in range(num_ch):
            ch_letter = chr(ord('A') + ch_index)  # A, B, C, D...
            col_name = f"{unit_name}_Ch{ch_letter}"
            
            # Try to get channel data
            attr_name = f"Channel{ch_letter}Data"
            if hasattr(unit, attr_name):
                data = getattr(unit, attr_name)
                if data is not None and len(data) == len(TimeIndex):
                    df[col_name] = np.asarray(data)
                else:
                    df[col_name] = np.nan
            else:
                df[col_name] = np.nan
    
    # ------------------------------------------------------------
    # 3. Create plot with custom colors
    # ------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(12, 6))
    plotted_any = False
    color_idx = 0
    
    for col in df.columns:
        series = df[col].dropna()
        if len(series) > 0:
            color = cscope_colors[color_idx % len(cscope_colors)]
            ax.plot(series.index, series.values, label=col, color=color, linewidth=1.5)
            plotted_any = True
            color_idx += 1
    
    if plotted_any:
        ax.legend(loc='center left', bbox_to_anchor=(1, 1), fancybox=True, framealpha=0.8)
        ax.grid(True, alpha=0.3)
    else:
        ax.set_xlim(StartTime_plot, StopTime_plot)
        ax.set_ylim(-1, 1)
        ax.text(
            0.5, 0.5, "No data available",
            ha='center', va='center',
            transform=ax.transAxes, fontsize=12
        )
    
    # ------------------------------------------------------------
    # 4. Titles and labels
    # ------------------------------------------------------------
    n_units = len(units)
    n_channels = df.shape[1]
    ax.set_title(f"Cleverscope Plot — {n_units} Units, {n_channels} Channels", 
                 fontsize=14, fontweight='bold')
    ax.set_xlabel("Time (s)", fontsize=12)
    ax.set_ylabel("Voltage (V)", fontsize=12)
    
    plt.gcf().canvas.manager.set_window_title("Cleverscope Python Demonstration")
    plt.tight_layout()
    plt.show()

# Example usage after acquisition:
# DrawPlot(connected_scopes)



##########  Prints out imformation about the connected unit
def GetAndDisplayUnitInfo(CscopeUnit):
	FunctionsToCall = ['ID','FirmwareVer','DriverVer','Resolution','FrameLength','Temperature', ]
	for i,info in enumerate(FunctionsToCall):
		CscopeUnit.DoCscopeFunction(ctypes.c_uint16(i),0)
		if info=='DriverVer':
			print("%s: %.3f" %('DLL Version',CscopeUnit.FunctionResult.value))
		else:
			print("%s: %.0f" %(info,CscopeUnit.FunctionResult.value))


########### Initialise the Classes for each Scope
print("___________________")
print("# Initialising... #\n")


# Dictionary to store all scope instances
scopes = {}


UnitNumber = -1
for config in ScopeConfigs:
    unit_name = config['UnitName']
    UnitNumber = UnitNumber + 1
    print(f"Initializing {unit_name}...")
    if UnitNumber == 0:
        LinkPort = T_LinkPort.T_LinkPort_Master
    else:
        LinkPort = T_LinkPort.T_LinkPort_Slave


    # Create scope instance with parameters from config
    scopes[unit_name] = CleverscopeInterface.Cleverscope(
        UnitNumber,  
        InterfaceSource= InterfaceSource,
        IPAddr=config['IPAddr'],
        TCP_Port=config['TCP_Port'],
        SerialNumber=config['SerialNumber'],
        StartTime=StartTime,
        StopTime=StopTime,
        FrameNum=FrameNum,
        NumSamples=NumSamples,
        MaximumSamples=MaximumSamples,
        TriggerSource=TriggerSource, 
        TriggerLevel=TriggerLevel,
        LinkPort=LinkPort,
        ProbeMinVoltage=config['ProbeMinVoltage'],
        ProbeMaxVoltage=config['ProbeMaxVoltage'],
        ProbeAGain=PROBE_GAIN_MAP.get(config['ProbeAGain'], T_Probe.T_Probe_x1),
        ProbeBGain=PROBE_GAIN_MAP.get(config['ProbeBGain'], T_Probe.T_Probe_x1),
        ProbeCGain=PROBE_GAIN_MAP.get(config['ProbeCGain'], T_Probe.T_Probe_x1),
        ProbeDGain=PROBE_GAIN_MAP.get(config['ProbeDGain'], T_Probe.T_Probe_x1),
        ProbeCoupling=T_Coupling.T_Coupling_DC
    )

########### Connect to the Hardware
print("___________________")
print("# Connecting...   #\n")

for unit_name, scope in scopes.items():
    print(f"Connecting {unit_name}...")
    scope.ConnectToHardware()

########### Wait for each unit to complete their connection and verify
print("\n___________________")
print("# Verifying...    #\n")

connected_scopes = {}
failed_scopes = []

for unit_name, scope in scopes.items():
    scope.WaitForConnectionToComplete(5)
    
    if scope.IsConnected():
        if Debug:
            scope.DoCscopeFunction(9999, 0)
        
        print("______________________________")
        print(f"Hardware ({unit_name}) connected OK")
        
        SerialNumber = scope.GetSerialNumber()
        SigGenType = scope.GetSigGenType()
        CAUType = scope.GetCAUType()
        print("Model:", CAUType, "Serial#:", SerialNumber, "Sig Gen:", SigGenType)
        
        NumberOfChannels = scope.GetNumberOfChannels()
        print("Channels:", NumberOfChannels)
        
        GetAndDisplayUnitInfo(scope)
        
        connected_scopes[unit_name] = scope
        print()
    else:
        print(f"{unit_name} Failed to connect")
        failed_scopes.append(unit_name)
        print()

# Summary
print("==============================")
print(f"Connected: {len(connected_scopes)}/{len(scopes)} units")
if failed_scopes:
    print(f"Failed units: {', '.join(failed_scopes)}")
else:
    print("All units connected successfully!")

print("\nAll units ready for acquisition!")

########### Acquisition Loop
# Set acquisition parameters
DoAnAcquisition = True  # Set to False to skip acquisition
AcquisitionTypeToDo = T_AcquireAction.T_AcquireAction_Triggered  # Default acquisition type

while DoAnAcquisition:
    ########### Begin Acquisition
    print("_______________________")
    print("# Sampling Started... #")
    
    # Dictionary to track which units are waiting for samples
    waiting_for_samples = {}
    
    # Start acquisition for all connected units
    for unit_name, scope in connected_scopes.items():
        if scope.IsConnected():
            waiting_for_samples[unit_name] = True
            scope.BeginSampleCapture(AcquisitionTypeToDo)
            print(f"{unit_name} acquisition started")
        else:
            waiting_for_samples[unit_name] = False
    
    ########### Wait For Acquisition to Finish
    # Note: if the trigger mode is set to "Triggered" then the trigger may never occur if the parameters 
    # for capture are out of bounds of the signal. If the Capture Mode is "Auto" then the time to acquire 
    # should be roughly twice the sample period as well as allow some time for communications with hardware.
    print("\nWaiting for sampling to complete.\n")
    
    TimeLimit = 20  # 20 Second timeout
    StartTime_acq = time()
    TimedOut = False
    
    # Wait for all units to complete sampling
    while not TimedOut and any(waiting_for_samples.values()):
        for unit_name, is_waiting in list(waiting_for_samples.items()):
            if is_waiting:
                scope = connected_scopes[unit_name]
                if scope.CheckForSampleCaptureComplete():
                    waiting_for_samples[unit_name] = False
                    print(f"{unit_name} Sample Capture Complete")
        
        # Check for timeout
        if (time() - StartTime_acq) > TimeLimit:
            TimedOut = True
            print("\nTimeout waiting for sample capture!")
            print("Units still waiting:", [name for name, waiting in waiting_for_samples.items() if waiting])
        
        sleep(0.01)  # Small delay to prevent CPU spinning
    
    if not TimedOut:
        print("\nAll units completed sampling successfully!")
    DrawPlot(connected_scopes)
    # Exit loop after one acquisition (change logic as needed)
    DoAnAcquisition = False


########### Access individual scopes via: 
# scopes['AcquisitionUnitA'], scopes['AcquisitionUnitB'], etc.
# Or use connected_scopes dictionary for only successfully connected units