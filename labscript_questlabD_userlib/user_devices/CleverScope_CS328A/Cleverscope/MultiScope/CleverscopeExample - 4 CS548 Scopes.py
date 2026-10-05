'''
Shifted generic graph parameters into mpl.rcParams
Added DLL Version
Updated Sept 2021 RHC 
Updated Nov 2025 RHC for CS548 
'''


import CleverscopeInterface
from T_AcquireSpec import T_AcquireSpec, T_AcquireAction, T_SigGenWaveform, T_LinkPort, T_TrigChannel
from T_ChannelSpec import T_ChannelSpec, T_Probe, T_GlobalFilter, T_PreFilter20MHz, T_MA_Filter, T_ExpFilter, T_FilterOption, T_Coupling
from T_ReplaySpec import T_ReplaySpec
from T_T0dt import T_T0dt
from CleverscopeClasses import T_CAUStatus, T_Command, T_FunctionCommand, T_LinkMasterSlave, T_TriggeringUnit
from time import sleep, time
import ctypes
#Install these addional Packages:
import platform               
import msvcrt
import numpy as np 
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler

''' ignore this option
scope_colors = [
    "#FFFF00",  # 1  Yellow
    "#00FFFF",  # 2  Cyan
    "#FF00FF",  # 3  Magenta
    "#00FF00",  # 4  Green
    "#FFA500",  # 5  Orange
    "#1E90FF",  # 6  DodgerBlue
    "#FF4500",  # 7  OrangeRed
    "#ADFF2F",  # 8  GreenYellow
    "#FF1493",  # 9  DeepPink
    "#7B68EE",  # 10 MediumSlateBlue
    "#00BFFF",  # 11 DeepSkyBlue
    "#32CD32",  # 12 LimeGreen
    "#FFD700",  # 13 Gold
    "#BA55D3",  # 14 MediumOrchid
    "#00FA9A",  # 15 MediumSpringGreen
    "#8B0000",  # 16 DarkRed
    "#2E8B57",  # 17 SeaGreen
    "#DC143C",  # 18 Crimson
    "#708090",  # 19 SlateGray
    "#A0522D",  # 20 Sienna
]
'''
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
plt.rc('axes', prop_cycle=cycler(color=cscope_colors))


# Set the default color cycle to Labview colour convention
# mpl.rcParams['axes.prop_cycle'] = cycler('color',['#FF0000', '#0000FF', '#037100', '#FF8000','#B34B00','#5200A4','#723636','#800000'])

#set colors for chart parameters
params = {'text.color':'white', 'xtick.color':'white', 'ytick.color':'white', 'figure.facecolor':'green', 'axes.facecolor':'0.7'} 
mpl.rcParams.update(params)    

############# Definition of sub-routines
	#For this plot, we assume the T0dt values are the same for all connected cleverscopes
def DrawPlot(units):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    if not units:
        raise ValueError("No units supplied.")
    if len(units) > 5:
        raise ValueError("Maximum of 5 units supported.")

    # ------------------------------------------------------------
    # 1. Build time axis from Unit A
    # ------------------------------------------------------------
    UnitA = units[0]
    StartTime = UnitA.T0dt.T0
    StopTime  = UnitA.T0dt.T0 + (UnitA.T0dt.n * UnitA.T0dt.dt)
    TimeIndex = np.arange(start=StartTime, stop=StopTime, step=UnitA.T0dt.dt)

    # ------------------------------------------------------------
    # 2. Build channel table dynamically based on each model
    # ------------------------------------------------------------
    df = pd.DataFrame(index=TimeIndex)

    unit_names = ["A", "B", "C", "D", "E"]

    for i, unit in enumerate(units):
        prefix = unit_names[i]  # A, B, C...

        # Your system already knows num_channels from the model
        num_ch = unit.num_channels

        # If using explicit fields, detect channels automatically
        if hasattr(unit, "channel_data"):
            channel_arrays = unit.channel_data
        else:
            # Auto-detect from attributes: ChannelAData, ChannelBData, ...
            channel_arrays = []
            for ch in range(num_ch):
                attr = f"Channel{chr(ord('A') + ch)}Data"
                channel_arrays.append(getattr(unit, attr, None))

        for ch_index in range(num_ch):
            col_name = f"{prefix}{ch_index+1}"
            data = channel_arrays[ch_index]

            if data is not None and len(data) == len(TimeIndex):
                df[col_name] = np.asarray(data)
            else:
                # Fill the column but mark as empty
                df[col_name] = np.nan

    # ------------------------------------------------------------
    # 3. Plot safely
    # ------------------------------------------------------------
    fig, ax = plt.subplots()
    plotted_any = False

    for col in df.columns:
        series = df[col].dropna()
        if len(series) > 0:
            ax.plot(series.index, series.values, label=col)
            plotted_any = True

    if plotted_any:
        ax.legend()
    else:
        ax.set_xlim(StartTime, StopTime)
        ax.set_ylim(-1, 1)
        ax.text(
            0.5, 0.5, "No data available",
            ha='center', va='center',
            transform=ax.transAxes, fontsize=12
        )

    # ------------------------------------------------------------
    # 4. Titles + labels
    # ------------------------------------------------------------
    n_units = len(units)
    n_channels = df.shape[1]

    ax.set_title(f"Cleverscope Plot — {n_units} Units, {n_channels} Channels")
    ax.set_xlabel("Time")
    ax.set_ylabel("Voltage")
    plt.gcf().canvas.manager.set_window_title("Cleverscope Python Demonstration")

    plt.show()

def GetAndDisplayUnitInfo(CscopeUnit):
	FunctionsToCall = ['ID','FirmwareVer','DriverVer','Resolution','FrameLength','Temperature', ]
	for i,info in enumerate(FunctionsToCall):
		CscopeUnit.DoCscopeFunction(ctypes.c_uint16(i),0)
		if info=='DriverVer':
			print("%s: %.3f" %('DLL Version',CscopeUnit.FunctionResult.value))
		else:
			print("%s: %.0f" %(info,CscopeUnit.FunctionResult.value))


#### Used to poll keyboard to cancel sampling
def GetKeyPressed(): 
   x = msvcrt.kbhit()
   if x: 
      ret = ord(msvcrt.getch()) 
   else: 
      ret = 0 
   return ret

### Wait for Key Input with timeout option
def WaitForKey(Timeout):
	StartTime = time()
	KeyPressed = 0
	while KeyPressed == 0:
		sleep(0.010) #sleep 10ms
		KeyPressed = GetKeyPressed()
		#if KeyPressed != 0:
		#	print(KeyPressed)
		if (Timeout>0) and (time()-StartTime >Timeout):
			break
	return KeyPressed

### Print the T0dt to the display
def	PrintT0dt(Label, CscopeUnit):
	print("_______")
	print(Label)
	print("  T0dt.dt: ",CscopeUnit.T0dt.dt) 
	print("  T0dt.n: ",CscopeUnit.T0dt.n)
	print("  T0dt.T0: ",truncate(CscopeUnit.T0dt.T0))
	print("  T0dt.TTrig: ",CscopeUnit.T0dt.TTrig)
	print("  T0dt.Frame: ",CscopeUnit.T0dt.Frame)

### Get DC Average of samples
def CalculateSampleAverage(Samples):
	Average=sum(Samples)/len(Samples)
	return Average

### Get PEak to Peak Amplitide of waveform
def CalculateAmplitude(Samples):
	Amplitude=max(Samples)-min(Samples)
	return Amplitude

def truncate(n):
	return int(n * 10000) / 10000


################# End of Sub-routines


###########  Set triggering Parameters
TriggeringUnit = T_TriggeringUnit.T_TriggeringUnit_UnitA		# Trigger on Unit A (used when LinkedDualScope is True)
UnitATriggerChannel = T_TrigChannel.T_TrigChan_ChanB			# Unit A will Trigger on Channel A (if LinkedDualScope then the Triggering Unit will impact on this setting)
AcquisitionTypeToDo = T_AcquireAction.T_AcquireAction_Automatic	#Single, Automatic, or Triggered



#################  Main Code ########################
print("###### CLEVERSCOPE 20 CHANNEL SCOPE EXAMPLE ######\n")
AcquisitionUnitA = 0
AcquisitionUnitB = 1
AcquisitionUnitC = 2
AcquisitionUnitD = 3
AcquisitionUnitE = 4

LinkedDualScope = True
print("FIVE LINKED SCOPES")

########### Initialise the Classes for each of the Scopes to be connected
print("___________________")
print("# Initialising... #\n")
# SCOPE UNIT A
CscopeUnitA = CleverscopeInterface.Cleverscope(AcquisitionUnitA,
											   InterfaceSource = T_Interface.T_Interface_EthernetOrUSBUseSerialNumber,
											   IPAddr = '203.109.232.203', #'10.1.5.40',   #
											   TCP_Port = 54270, 
											   SerialNumber='IW10210',
											   StartTime = -0.005, # -5ms
											   StopTime = 0.005,   # +5ms
											   FrameNum = 0, 
											   NumSamples = 10000,
											   MaximumSamples = 10000,
											   TriggerSource = UnitATriggerChannel, 
											   TriggerLevel = 0.3, # 0.5V
											   LinkPort = T_LinkPort.T_LinkPort_Debug,
											   ProbeMinVoltage = -2.5, # -2V
											   ProbeMaxVoltage = 2.5, # +2V
											   ProbeAGain = T_Probe.T_Probe_x1,
											   ProbeBGain = T_Probe.T_Probe_x1,
											   ProbeCGain = T_Probe.T_Probe_x1,
											   ProbeDGain = T_Probe.T_Probe_x1,
											   ProbeCoupling = T_Coupling.T_Coupling_DC)

CscopeUnitB = CleverscopeInterface.Cleverscope(AcquisitionUnitB,
											   InterfaceSource = T_Interface.T_Interface_EthernetOrUSBUseSerialNumber,
											   IPAddr = '203.109.232.203', #'10.1.5.40',   #
											   TCP_Port = 55270, 
											   SerialNumber='JX10339',
											   StartTime = -0.005, # -5ms
											   StopTime = 0.005,   # +5ms
											   FrameNum = 0, 
											   NumSamples = 10000,
											   MaximumSamples = 10000,
											   TriggerSource = UnitATriggerChannel, 
											   TriggerLevel = 0.5, # 0.5V
											   LinkPort = T_LinkPort.T_LinkPort_Debug,
											   ProbeMinVoltage = -2.5, # -2V
											   ProbeMaxVoltage = 2.5, # +2V
											   ProbeAGain = T_Probe.T_Probe_x1,
											   ProbeBGain = T_Probe.T_Probe_x1,
											   ProbeCGain = T_Probe.T_Probe_x1,
											   ProbeDGain = T_Probe.T_Probe_x1,
											   ProbeCoupling = T_Coupling.T_Coupling_DC)

CscopeUnitC = CleverscopeInterface.Cleverscope(AcquisitionUnitC,
											   InterfaceSource = T_Interface.T_Interface_EthernetOrUSBUseSerialNumber,
											   IPAddr = '203.109.232.203', #'10.1.5.40',   #
											   TCP_Port = 56270, 
											   SerialNumber='JX10340',
											   StartTime = -0.005, # -5ms
											   StopTime = 0.005,   # +5ms
											   FrameNum = 0, 
											   NumSamples = 10000,
											   MaximumSamples = 10000,
											   TriggerSource = UnitATriggerChannel, 
											   TriggerLevel = 0.5, # 0.5V
											   LinkPort = T_LinkPort.T_LinkPort_Debug,
											   ProbeMinVoltage = -2.5, # -2V
											   ProbeMaxVoltage = 2.5, # +2V
											   ProbeAGain = T_Probe.T_Probe_x1,
											   ProbeBGain = T_Probe.T_Probe_x1,
											   ProbeCGain = T_Probe.T_Probe_x1,
											   ProbeDGain = T_Probe.T_Probe_x1,
											   ProbeCoupling = T_Coupling.T_Coupling_DC)

CscopeUnitD = CleverscopeInterface.Cleverscope(AcquisitionUnitD,
											   InterfaceSource = T_Interface.T_Interface_EthernetOrUSBUseSerialNumber,
											   IPAddr = '203.109.232.203', #'10.1.5.40',   #
											   TCP_Port = 57270, 
											   SerialNumber='JX10338',
											   StartTime = -0.005, # -5ms
											   StopTime = 0.005,   # +5ms
											   FrameNum = 0, 
											   NumSamples = 10000,
											   MaximumSamples = 10000,
											   TriggerSource = UnitATriggerChannel, 
											   TriggerLevel = 0.5, # 0.5V
											   LinkPort = T_LinkPort.T_LinkPort_Debug,
											   ProbeMinVoltage = -2.5, # -2V
											   ProbeMaxVoltage = 2.5, # +2V
											   ProbeAGain = T_Probe.T_Probe_x1,
											   ProbeBGain = T_Probe.T_Probe_x1,
											   ProbeCGain = T_Probe.T_Probe_x1,
											   ProbeDGain = T_Probe.T_Probe_x1,
											   ProbeCoupling = T_Coupling.T_Coupling_DC)

CscopeUnitE = CleverscopeInterface.Cleverscope(AcquisitionUnitE,
											   InterfaceSource = T_Interface.T_Interface_EthernetOrUSBUseSerialNumber,
											   IPAddr = '203.109.232.203', #'10.1.5.40',   #
											   TCP_Port = 57270, 
											   SerialNumber='JX10333',
											   StartTime = -0.005, # -5ms
											   StopTime = 0.005,   # +5ms
											   FrameNum = 0, 
											   NumSamples = 10000,
											   MaximumSamples = 10000,
											   TriggerSource = UnitATriggerChannel, 
											   TriggerLevel = 0.5, # 0.5V
											   LinkPort = T_LinkPort.T_LinkPort_Debug,
											   ProbeMinVoltage = -2.5, # -2V
											   ProbeMaxVoltage = 2.5, # +2V
											   ProbeAGain = T_Probe.T_Probe_x1,
											   ProbeBGain = T_Probe.T_Probe_x1,
											   ProbeCGain = T_Probe.T_Probe_x1,
											   ProbeDGain = T_Probe.T_Probe_x1,
											   ProbeCoupling = T_Coupling.T_Coupling_DC)




########### Connect to the Hardware
CscopeUnitA.ConnectToHardware()
CscopeUnitB.ConnectToHardware()
CscopeUnitC.ConnectToHardware()
CscopeUnitD.ConnectToHardware()
CscopeUnitE.ConnectToHardware()
########### Wait for each unit to complete their connection

Debug = 'False'

# SCOPE UNIT A
CscopeUnitA.WaitForConnectionToComplete(5)
if CscopeUnitA.IsConnected():
	if Debug:
		CscopeUnitA.DoCscopeFunction(9999,0)
	print("______________________________")
	print("Hardware (Unit A) connected OK")
	SerialNumber = CscopeUnitA.GetSerialNumber()
	SigGenType = CscopeUnitA.GetSigGenType()
	CAUType = CscopeUnitA.GetCAUType()
	print("Model:", CAUType,"Serial#:",SerialNumber,"Sig Gen:", SigGenType)
	NumberOfChannels = CscopeUnitA.GetNumberOfChannels()
	print("Channels:",NumberOfChannels)
	GetAndDisplayUnitInfo(CscopeUnitA)
else:
	print("Unit A Failed to connect")

# SCOPE UNIT B
CscopeUnitB.WaitForConnectionToComplete(5)
if CscopeUnitB.IsConnected():
	if Debug:
		CscopeUnitB.DoCscopeFunction(9999,0)
	print("______________________________")
	print("Hardware (Unit B) connected OK")
	SerialNumber = CscopeUnitB.GetSerialNumber()
	SigGenType = CscopeUnitB.GetSigGenType()
	CAUType = CscopeUnitB.GetCAUType()
	print("Model:", CAUType,"Serial#:",SerialNumber,"Sig Gen:", SigGenType)
	NumberOfChannels = CscopeUnitB.GetNumberOfChannels()
	print("Channels:",NumberOfChannels)
	GetAndDisplayUnitInfo(CscopeUnitB)
else:
	print("Unit B Failed to connect")
	
# SCOPE UNIT C
CscopeUnitC.WaitForConnectionToComplete(5)
if CscopeUnitC.IsConnected():
	if Debug:
		CscopeUnitC.DoCscopeFunction(9999,0)
	print("______________________________")
	print("Hardware (Unit C) connected OK")
	SerialNumber = CscopeUnitC.GetSerialNumber()
	SigGenType = CscopeUnitC.GetSigGenType()
	CAUType = CscopeUnitC.GetCAUType()
	print("Model:", CAUType,"Serial#:",SerialNumber,"Sig Gen:", SigGenType)
	NumberOfChannels = CscopeUnitC.GetNumberOfChannels()
	print("Channels:",NumberOfChannels)
	GetAndDisplayUnitInfo(CscopeUnitC)
else:
	print("Unit C Failed to connect")
	
# SCOPE UNIT D
CscopeUnitD.WaitForConnectionToComplete(5)
if CscopeUnitD.IsConnected():
	if Debug:
		CscopeUnitD.DoCscopeFunction(9999,0)
	print("______________________________")
	print("Hardware (Unit D) connected OK")
	SerialNumber = CscopeUnitD.GetSerialNumber()
	SigGenType = CscopeUnitD.GetSigGenType()
	CAUType = CscopeUnitD.GetCAUType()
	print("Model:", CAUType,"Serial#:",SerialNumber,"Sig Gen:", SigGenType)
	NumberOfChannels = CscopeUnitD.GetNumberOfChannels()
	print("Channels:",NumberOfChannels)
	GetAndDisplayUnitInfo(CscopeUnitD)
else:
	print("Unit D Failed to connect")

	
# SCOPE UNIT E
CscopeUnitE.WaitForConnectionToComplete(5)
if CscopeUnitE.IsConnected():
	if Debug:
		CscopeUnitE.DoCscopeFunction(9999,0)
	print("______________________________")
	print("Hardware (Unit E) connected OK")
	SerialNumber = CscopeUnitE.GetSerialNumber()
	SigGenType = CscopeUnitE.GetSigGenType()
	CAUType = CscopeUnitE.GetCAUType()
	print("Model:", CAUType,"Serial#:",SerialNumber,"Sig Gen:", SigGenType)
	NumberOfChannels = CscopeUnitE.GetNumberOfChannels()
	print("Channels:",NumberOfChannels)
	GetAndDisplayUnitInfo(CscopeUnitD)
else:
	print("Unit E Failed to connect")###################### Configure parameters as required for Acquisition
# Signal Generator
UnitAFreq = 1000
UnitBFreq = 1200
UnitCFreq = 800
UnitDFreq = 1500
CscopeUnitA.SetupSignalGenerator(UnitAFreq,3,50,T_SigGenWaveform.T_SigGenWaveform_sine)
CscopeUnitB.SetupSignalGenerator(UnitBFreq,1.5,50,T_SigGenWaveform.T_SigGenWaveform_sine)
CscopeUnitB.AcquireSpec.SigGenOffset = -1
CscopeUnitC.SetupSignalGenerator(UnitCFreq,2,50,T_SigGenWaveform.T_SigGenWaveform_sine)
CscopeUnitD.SetupSignalGenerator(UnitDFreq,2,50,T_SigGenWaveform.T_SigGenWaveform_sine)
CscopeUnitD.AcquireSpec.SigGenOffset = 1

########### Check the triggering is setup corectly for Quad Scope (with and without linking):
########### Figure Out how the units will trigger based on if the units are linked or not, and which unit is triggering:

CscopeUnitA.SetDualScopelink(T_LinkMasterSlave.T_LinkMasterSlave_Master, UnitATriggerChannel )
CscopeUnitB.SetDualScopelink(T_LinkMasterSlave.T_LinkMasterSlave_Slave, UnitATriggerChannel )
CscopeUnitC.SetDualScopelink(T_LinkMasterSlave.T_LinkMasterSlave_Slave, UnitATriggerChannel )
CscopeUnitD.SetDualScopelink(T_LinkMasterSlave.T_LinkMasterSlave_Slave, UnitATriggerChannel )

DoAnAcquisition = CscopeUnitA.IsConnected() or CscopeUnitB.IsConnected() or CscopeUnitC.IsConnected() or CscopeUnitD.IsConnected()

#Keep Looping doing acquisitions
while DoAnAcquisition: 
	########### Begin Acquisition
	print("_______________________")
	print("# Sampling Started... #")

	if CscopeUnitA.IsConnected():
		UnitA_WaitingForSamples = True;
		CscopeUnitA.BeginSampleCapture(T_AcquireAction.T_AcquireAction_Triggered)
	else:
		UnitA_WaitingForSamples = False;

	if CscopeUnitB.IsConnected():
		UnitB_WaitingForSamples = True;
		CscopeUnitB.BeginSampleCapture(T_AcquireAction.T_AcquireAction_Triggered)
	else:
		UnitB_WaitingForSamples = False;

	if CscopeUnitC.IsConnected():
		UnitC_WaitingForSamples = True;
		CscopeUnitC.BeginSampleCapture(T_AcquireAction.T_AcquireAction_Triggered)
	else:
		UnitC_WaitingForSamples = False;
		
	if CscopeUnitD.IsConnected():
		UnitD_WaitingForSamples = True;
		CscopeUnitD.BeginSampleCapture(AcquisitionTypeToDo)
	else:
		UnitD_WaitingForSamples = False;

	if CscopeUnitE.IsConnected():
		UnitD_WaitingForSamples = True;
		CscopeUnitE.BeginSampleCapture(AcquisitionTypeToDo)
	else:
		UnitE_WaitingForSamples = False;
	########### Wait For Acquisition to Finish
	# Note: if the trigger mode is set to "Triggered" then the trigger may never occur if the parameters for capture are out
	# of bounds of the signal. If the Capture Mode is "Auto" then the time to acquire should be roughly twice the sample period
	# as well as allow some time for communications with hardware.
	print ("Waiting for sampling to complete.\n")

	FinishedSampling=False
	CancelledByKeypress = False
	TimeLimit = 20 # 20 Second timeout
	StartTime = time()
	LastTime = StartTime
	TimedOut = False

	while (not TimedOut) and (UnitA_WaitingForSamples or UnitB_WaitingForSamples or UnitC_WaitingForSamples or UnitD_WaitingForSamples):
		if UnitA_WaitingForSamples:
			if  CscopeUnitA.CheckForSampleCaptureComplete():
				UnitA_WaitingForSamples = False
				print("UnitA Sample Capture Complete")
		if UnitB_WaitingForSamples:
			if CscopeUnitB.CheckForSampleCaptureComplete():
				UnitB_WaitingForSamples = False
				print("UnitB Sample Capture Complete")
		if UnitC_WaitingForSamples:
			if CscopeUnitC.CheckForSampleCaptureComplete():
				UnitC_WaitingForSamples = False
				print("UnitC Sample Capture Complete")
		if UnitD_WaitingForSamples:
			if CscopeUnitD.CheckForSampleCaptureComplete():
				UnitD_WaitingForSamples = False
				print("UnitD Sample Capture Complete")
		if UnitE_WaitingForSamples:
			if CscopeUnitE.CheckForSampleCaptureComplete():
				UnitD_WaitingForSamples = False
				print("UnitE Sample Capture Complete")

		KeyPressed = GetKeyPressed()
		if time()-LastTime > 1:
			print(".")
			LastTime = time()
		if KeyPressed != 0:
			print("\r\nAcquision cancelled by keypress")
			CancelledByKeypress = True
			break
		if time()-StartTime > TimeLimit:
			print("\r\nAcquision timeout")
			TimedOut = True
			break
		sleep(0.01)

	# If samples received and not timed out
	if (not TimedOut) and (not CancelledByKeypress):
		# Show the T0dt of the captured samples:
		PrintT0dt("Unit A:", CscopeUnitA)
		PrintT0dt("Unit B:", CscopeUnitB)
		PrintT0dt("Unit C:", CscopeUnitC)
		PrintT0dt("Unit D:", CscopeUnitD)
		PrintT0dt("Unit E:", CscopeUnitD)
	
		
		# Display Average and DC each channel:
		print("___________________________________________")
		print("ChannelA: Average:%.4fV Amplitude:%.4fV" % ( CalculateSampleAverage(CscopeUnitA.ChannelAData) , CalculateAmplitude(CscopeUnitA.ChannelAData) ) )
		print("ChannelB: Average:%.4fV Amplitude:%.4fV" % ( CalculateSampleAverage(CscopeUnitA.ChannelBData) , CalculateAmplitude(CscopeUnitA.ChannelBData) ) )
		print("ChannelC: Average:%.4fV Amplitude:%.4fV" % ( CalculateSampleAverage(CscopeUnitB.ChannelAData) , CalculateAmplitude(CscopeUnitB.ChannelAData) ) )
		print("ChannelD: Average:%.4fV Amplitude:%.4fV" % ( CalculateSampleAverage(CscopeUnitB.ChannelBData) , CalculateAmplitude(CscopeUnitB.ChannelBData) ) )
		print("ChannelE: Average:%.4fV Amplitude:%.4fV" % ( CalculateSampleAverage(CscopeUnitC.ChannelAData) , CalculateAmplitude(CscopeUnitC.ChannelAData) ) )
		print("ChannelF: Average:%.4fV Amplitude:%.4fV" % ( CalculateSampleAverage(CscopeUnitC.ChannelBData) , CalculateAmplitude(CscopeUnitC.ChannelBData) ) )
		print("ChannelG: Average:%.4fV Amplitude:%.4fV" % ( CalculateSampleAverage(CscopeUnitD.ChannelAData) , CalculateAmplitude(CscopeUnitD.ChannelAData) ) )
		print("ChannelH: Average:%.4fV Amplitude:%.4fV" % ( CalculateSampleAverage(CscopeUnitD.ChannelBData) , CalculateAmplitude(CscopeUnitD.ChannelBData) ) )
		print("ChannelG: Average:%.4fV Amplitude:%.4fV" % ( CalculateSampleAverage(CscopeUnitD.ChannelAData) , CalculateAmplitude(CscopeUnitD.ChannelAData) ) )
		print("ChannelH: Average:%.4fV Amplitude:%.4fV" % ( CalculateSampleAverage(CscopeUnitD.ChannelBData) , CalculateAmplitude(CscopeUnitD.ChannelBData) ) )

		print("_______________________________________________________")
		#print("Acquire:",abs(truncate(CscopeUnitA.AcquireSpec.StartTime))," Replay:",abs(truncate(CscopeUnitA.ReplaySpec.StartTime))," Tdt.T0:",abs(truncate(CscopeUnitA.T0dt.T0)),"Error:",truncate(CscopeUnitA.ReplaySpec.StartTime-CscopeUnitA.T0dt.T0))	
		#if 	abs(CscopeUnitA.ReplaySpec.StartTime-CscopeUnitA.T0dt.T0) > .000005:
		#d	print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!ERROR!!!!!!!!!!!!!!!!!!!!!!!!!")	 

####### Reconfigure for next capture. You must set both the Acquire and Replay start and stop times. Replay is initialised with the Acquire values
### Note: Replay Start and Stop Times must be within those set by the Aquire values. You are able to request a Replay without Acquire
		#CscopeUnitA.AcquireSpec.StartTime = CscopeUnitA.AcquireSpec.StartTime - 0.0001
		#CscopeUnitA.AcquireSpec.StopTime = CscopeUnitA.AcquireSpec.StopTime + 0.0001
		#CscopeUnitA.ReplaySpec.StartTime = CscopeUnitA.AcquireSpec.StartTime
		#CscopeUnitA.ReplaySpec.StopTime = CscopeUnitA.AcquireSpec.StopTime



# Signal Generator
		#UnitAFreq = UnitAFreq + 50
		#CscopeUnitA.AcquireSpec.SigGenOffset = -1
		#CscopeUnitA.SetupSignalGenerator(UnitAFreq,3,50,T_SigGenWaveform.T_SigGenWaveform_sine)

######################### End of Reconfiguration
	
####### Display Menu and wait for response
	FinishedWaitingForKeyPress = False
	while not FinishedWaitingForKeyPress:
		print("\n[d]=Display Plot, [enter] or [space] to Capture samples again or [esc] or [q] to quit")
		KeyPressed = WaitForKey(-1);
		if (KeyPressed == 27 or KeyPressed == 81 or KeyPressed == 113 ): #Esc, q or Q
			DoAnAcquisition = False
			FinishedWaitingForKeyPress = True
		if (KeyPressed==68 or KeyPressed==100): #D or d
			DrawPlot(CscopeUnitA,CscopeUnitB,CscopeUnitC,CscopeUnitD,CscopeUnitE)
			FinishedWaitingForKeyPress=False
		if (KeyPressed==32 or KeyPressed==13 or KeyPressed==10): #Space, Enter or return
			DoAnAcquisition = True
			FinishedWaitingForKeyPress = True

########### Close all hardware and close the driver
# Close Hardware
print("\r\n# Close Cleverscope Hardware... #")
CscopeUnitA.SendCleverscopeCommand(T_Command.T_Command_Close)
CscopeUnitB.SendCleverscopeCommand(T_Command.T_Command_Close)
CscopeUnitC.SendCleverscopeCommand(T_Command.T_Command_Close)
CscopeUnitD.SendCleverscopeCommand(T_Command.T_Command_Close)


print("\r\n###### FINISHED ######\n")
print("###### GOODBYE ######\n")
