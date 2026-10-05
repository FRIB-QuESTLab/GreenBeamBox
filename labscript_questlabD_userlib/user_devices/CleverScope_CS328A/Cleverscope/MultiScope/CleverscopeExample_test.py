'''
Created on 04.11.2020
Added two scope and eight channel capability
Shifted generic graph parameters into mpl.rcParams
Added DLL Version
Updated August 2021 RHC 
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

#Install these addional Packages:
import platform               
import msvcrt
import numpy as np 
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler

# Set the default color cycle to Labview colour convention
mpl.rcParams['axes.prop_cycle'] = cycler('color',['#FF0000', '#0000FF', '#037100', '#FF8000','#B34B00','#5200A4','#723636','#800000'])

#set colors for chart parameters
params = {'text.color':'white', 'xtick.color':'white', 'ytick.color':'white', 'figure.facecolor':'green', 'axes.facecolor':'0.7'} 
mpl.rcParams.update(params)                                

############ Definition of sub-routines  #########

def DrawPlot(UnitA, UnitB, DualScope, FourChannel, Cautype):

    # ------------------------------------------------------------
    # 1. Time axis creation
    # ------------------------------------------------------------
    StartTime = UnitA.T0dt.T0
    StopTime  = UnitA.T0dt.T0 + (UnitA.T0dt.n * UnitA.T0dt.dt)
    TimeIndex = np.arange(start=StartTime, stop=StopTime, step=UnitA.T0dt.dt)

    # ------------------------------------------------------------
    # 2. Build channel list
    # ------------------------------------------------------------
    channels = []
    ChannelsTitle = " Two"
    channels = [
        ("Chan A", UnitA.ChannelAData),
        ("Chan B", UnitA.ChannelBData),
        ]

    # ------------------------------------------------------------
    # 3. Create DataFrame (empty at first)
    # ------------------------------------------------------------
    df = pd.DataFrame(index=TimeIndex)

    # Populate only if array lengths match
    for name, data in channels:
        a = np.asarray(data)
        print(a[~np.isnan(a)])
        if data is not None:
            df[name] = np.asarray(data)[:len(TimeIndex)]   # crop any unused array items
        else:
            df[name] = np.nan  # placeholder

    # ------------------------------------------------------------
    # 4. Plotting safely
    # ------------------------------------------------------------
    fig, ax = plt.subplots()

    plotted_any = False
    for col in df.columns:
        series = df[col].dropna()
        # print(len(series))
        # print(len(series.index))
        # print(len(series.values))
        if len(series) > 0:
            ax.plot(series.index, series.values, label=col, 
                    marker='.', linewidth=0, markersize=0.03)
            plotted_any = True
            

    # If nothing plotted, create a clean empty view
    if not plotted_any:
        ax.set_xlim(StartTime, StopTime)
        ax.set_ylim(-1, 1)  # safe default
        ax.text(
            0.5, 0.5, 
            "No data available",
            ha='center', va='center',
            transform=ax.transAxes,
            fontsize=12
        )

    if plotted_any:
        ax.legend()

        
    # ------------------------------------------------------------
    # 5. Set titles and labels
    # ------------------------------------------------------------
    plt.gcf().canvas.manager.set_window_title("Cleverscope Python Demonstration")
    ax.set_xlabel("Time")
    ax.set_ylabel("Voltage")
    ax.set_title(f"{Cautype}{ChannelsTitle} Channel Oscilloscope")
    plt.show()
    return
 

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
        #    print(KeyPressed)
        if (Timeout>0) and (time()-StartTime >Timeout):
            break
    return KeyPressed

### Print the T0dt to the display
def    PrintT0dt(Label, CscopeUnit):
    print(Label)
    print("  T0dt.dt: ",CscopeUnit.T0dt.dt)
    print("  T0dt.n: ",CscopeUnit.T0dt.n)
    print("  T0dt.T0: ",CscopeUnit.T0dt.T0)
    print("  T0dt.TTrig: ",CscopeUnit.T0dt.TTrig)
    print("  T0dt.Frame: ",CscopeUnit.T0dt.Frame)

### Get DC Average of samples
def CalculateSampleAverage(Samples):
    Average=sum(Samples)/len(Samples)
    return Average

### Get Peak to Peak Amplitide of waveform
def CalculateAmplitude(Samples):
    Amplitude=max(Samples)-min(Samples)
    return Amplitude


################# End of Sub-routines



#################  Main Code ########################
print("###### CLEVERSCOPE EXAMPLE ######\n")
AcquisitionUnitA = 0
AcquisitionUnitB = 1


########### Ask the user to select either single scope, or Dual Scope
DualScope = False
LinkedDualScope = False
FourChannel = False
Debug = False                                             

print("SINGLE SCOPE")
print("Debug NOT Active")
print("___________________")
print("# Initialising... #\n")


###########  Set triggering Parameters
UnitATriggerChannel = T_TrigChannel.T_TrigChan_ChanA     # Unit A will Trigger on Channel A (if LinkedDualScope then the Triggering Unit will impact on this setting)
AcquisitionTypeToDo = T_AcquireAction.T_AcquireAction_Automatic #Choose Single, Automatic, or Triggered


# Set some Parameters
StartTime = -0.001
StopTime = 0.175
ProbeMinVoltage = -5
ProbeMaxVoltage = 5
Numsamples = int(2e6)  # number of points to collect and store in buffer.
MaximumSamples = int(4e6)  # this is model specific.
FrameNum = 0

# SCOPE UNIT A
CscopeUnitA = CleverscopeInterface.Cleverscope(AcquisitionUnitA,
                                               InterfaceSource = T_Interface.T_Interface_EthernetOrUSBUseSerialNumber,
                                               IPAddr = '0.0.0.0',  # not using TCP
                                               TCP_Port = 53270, 
                                               SerialNumber='LW8675',  #CR10038  GT7948
                                               StartTime = StartTime,
                                               StopTime =StopTime,  
                                               FrameNum = FrameNum, 
                                               NumSamples = Numsamples,
                                               MaximumSamples = MaximumSamples,
                                               TriggerSource = UnitATriggerChannel, 
                                               TriggerLevel = .5, 
                                               LinkPort = T_LinkPort.T_LinkPort_Debug,
                                               ProbeMinVoltage = ProbeMinVoltage,
                                               ProbeMaxVoltage = ProbeMaxVoltage, 
                                               ProbeAGain = T_Probe.T_Probe_x1,
                                               ProbeBGain = T_Probe.T_Probe_x1,
                                               ProbeCGain = T_Probe.T_Probe_x1,
                                               ProbeDGain = T_Probe.T_Probe_x1,
                                               ProbeCoupling = T_Coupling.T_Coupling_DC)

CscopeUnitB = 0


########### Connect to the Hardware for each of the scopes
CscopeUnitA.ConnectToHardware()

    ### Advise Versions  ####
print('Python Version:  ',platform.python_version())

########### Wait for each unit to complete their connection
# SCOPE UNIT A
CscopeUnitA.WaitForConnectionToComplete(5)
if CscopeUnitA.IsConnected():
    print("______________________________")  # Provide some details of Unit A
    print("Hardware (Unit A) connected OK")
    SerialNumber = CscopeUnitA.GetSerialNumber()
    SigGenType = CscopeUnitA.GetSigGenType()
    CAUType = CscopeUnitA.GetCAUType()
    if (CAUType[:3] == "CS3"):
        CSType = CAUType[:6]
    else:
        CSType = CAUType[:5]
    print("Model:", CAUType,"Serial#:",SerialNumber,"Sig Gen:", SigGenType)
    NumberOfChannels = CscopeUnitA.GetNumberOfChannels()
    print("Channels:",NumberOfChannels)
    IPAddressA = CscopeUnitA.GetIPAddress()
    if IPAddressA.find('.')<1:
        print ("USB Connected")
    else:
        print("ethernet Connected")
        print("IP Address is ",IPAddressA)
    GetAndDisplayUnitInfo(CscopeUnitA)

else:
    print("Unit A Failed to connect")



################# Final Configuration of scope
AcquireStartTime = -0.005;
AcquireStopTime = 0.175;

########### Check the triggering is setup corectly for Dual Scope (with and without linking):
########### Figure Out how the units will trigger based on if the units are linked or not, and which unit is triggering:

#Single Scope: Ensure Unit A has Master Slave turned off
CscopeUnitA.SetDualScopelink(T_LinkMasterSlave.T_LinkMasterSlave_Unlinked, UnitATriggerChannel)
DoAnAcquisition = CscopeUnitA.IsConnected()

CscopeUnitA.ChannelSpecArray[0].Max=0.5
CscopeUnitA.ChannelSpecArray[0].Min=-0.5

print()
print('Channel max A through D:')
print(CscopeUnitA.ChannelSpecArray[0].Max)
print(CscopeUnitA.ChannelSpecArray[1].Max)
print(CscopeUnitA.ChannelSpecArray[2].Max)
print(CscopeUnitA.ChannelSpecArray[3].Max)
print()
print('Channel min A through D:')
print(CscopeUnitA.ChannelSpecArray[0].Min)
print(CscopeUnitA.ChannelSpecArray[1].Min)
print(CscopeUnitA.ChannelSpecArray[2].Min)
print(CscopeUnitA.ChannelSpecArray[3].Min)

###########  Start the Acquisition  ########### 
########### Keep Looping doing acquisitions ########### 
while DoAnAcquisition: 
    
################# Configuration of acquistion
    
    # Change Acquistion Values
    CscopeUnitA.AcquireSpec.StartTime = ctypes.c_double(AcquireStartTime)  # controls time related to acquisition
    CscopeUnitA.AcquireSpec.StopTime = ctypes.c_double(AcquireStopTime)
    CscopeUnitA.ReplaySpec.StartTime = ctypes.c_double(AcquireStartTime)  # controls time span related to the data buffer and returned data
    CscopeUnitA.ReplaySpec.StopTime = ctypes.c_double(AcquireStopTime)
    
    ########### Begin Acquisition    ########### Same as arming oscilloscope
    print("\r\n# Sampling Started... #")

    if CscopeUnitA.IsConnected():
        UnitA_WaitingForSamples = True;
        CscopeUnitA.BeginSampleCapture(AcquisitionTypeToDo);
    else:
        UnitA_WaitingForSamples = False;
    print("Oscilloscope has been armed")


    ########### Wait For Acquisition to Finish
    # Note: if the trigger mode is set to "Triggered" then the trigger may never occur if the parameters for capture are out
    # of bounds of the signal. If the Capture Mnode is "Auto" then the time to acquire should be roughly twice the sample period
    # as well as allow some time for communications with hardware.
    print ("Waiting for sampling to complete.")

    FinishedSampling=False
    CancelledByKeypress = False
    TimeLimit = 360 # 20 Second timeout
    StartTime = time()
    LastTime = StartTime
    TimedOut = False

    while (not TimedOut) and (UnitA_WaitingForSamples):
        if UnitA_WaitingForSamples:
            if CscopeUnitA.CheckForSampleCaptureComplete():
                UnitA_WaitingForSamples = False
                print("UnitA Sample Capture Complete")


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

    
    # CS320/CS328
    print("ChannelA: Average:%.4fV Amplitude:%.4fV" % ( CalculateSampleAverage(CscopeUnitA.ChannelAData) , CalculateAmplitude(CscopeUnitA.ChannelAData) ) )
    print("ChannelB: Average:%.4fV Amplitude:%.4fV" % ( CalculateSampleAverage(CscopeUnitA.ChannelBData) , CalculateAmplitude(CscopeUnitA.ChannelBData) ) )
        
# Update values ready for next acquisition

    FinishedWaitingForKeyPress = False
    while not FinishedWaitingForKeyPress:
        print("\r\n[d]=Display Plot, [enter] or [space] to Capture samples again or [esc] or [q] to quit")
        KeyPressed = WaitForKey(-1);
        if (KeyPressed == 27 or KeyPressed == 81 or KeyPressed == 113 ): #Esc, q or Q
            DoAnAcquisition = False
            FinishedWaitingForKeyPress = True
        if (KeyPressed==68 or KeyPressed==100): #D or d
            DrawPlot(CscopeUnitA,CscopeUnitB,DualScope,FourChannel,CSType)
        #    FinishedWaitingForKeyPress=False
        if (KeyPressed==32 or KeyPressed==13 or KeyPressed==10): #Space, Enter or return
            DoAnAcquisition = True
            FinishedWaitingForKeyPress = True


########### Close all hardware and close the driver
# Close Hardware
print("\r\n# Close Cleverscope Hardware... #")
CscopeUnitA.SendCleverscopeCommand(T_Command.T_Command_Close)
CscopeUnitA.SendCleverscopeCommand(T_Command.T_Command_Finish)


print("\r\n###### FINISHED ######\n")