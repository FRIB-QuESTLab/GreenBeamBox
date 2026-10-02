#ifndef __Cscope_control_driver_64_h
#define __Cscope_control_driver_64_h
#ifdef __cplusplus
extern "C" {
#endif

typedef char bool_t;
typedef struct {
	int 	cnt;		 //number of bytes that follow 
	char	str[1];		 //cnt bytes 
	} LStr, LStrPtra, LStrHandle;

typedef long            MgErr;
typedef long            bool32_t;
typedef char            int8_t;
typedef unsigned char   uint8_t;
typedef short           int16_t;
typedef unsigned short  uint16_t;
typedef long            int32_t;
typedef unsigned long   uint32_t;
typedef long long       int64_t;
typedef unsigned        long long uint64_t;

typedef uint16_t  T_Command;
#define T_Command_Initialize 0
#define T_Command_Acquire 1
#define T_Command_Replay 2
#define T_Command_WaitForSamples 3
#define T_Command_Update 4
#define T_Command_Close 5
#define T_Command_Status 6
#define T_Command_Function 7
#define T_Command_GetFrame 8
#define T_Command_Finish 9
#define T_Command_FunctionResult 10
#define T_Command_Spectrum 11
#define T_Command_CAUInfo 12
#define T_Command_ReplayFrame 13
#define T_Command_GetSampleStatus 14
#define T_Command_UpdatePulseWaveform 15
#define T_Command_StartStopPulseWaveform 16
#define T_Command_ManualStatePulseWaveform 17
#define T_Command_OutputMultiplexerSetup 18
#define T_Command_ProbeCompSetup 19
typedef uint16_t  T_AcquireAction;
#define T_AcquireAction_Single 0
#define T_AcquireAction_Automatic 1
#define T_AcquireAction_Triggered 2
#define T_AcquireAction_Stop 3
#define T_AcquireAction_SingleStop 4
#define T_AcquireAction_Replay 5
#define T_AcquireAction_Chart 6
typedef uint16_t  T_AcquireMode;
#define T_AcquireMode_Sampled 0
#define T_AcquireMode_PeakCaptured 1
#define T_AcquireMode_Filtered 2
#define T_AcquireMode_Repetitive 3
#define T_AcquireMode_WaveformAvg 4
typedef uint16_t  T_Acquirer;
#define T_Acquirer_InternalSigGen 0
#define T_Acquirer_APC901 1
#define T_Acquirer_APC901A 2
#define T_Acquirer_SoundCard 3
#define T_Acquirer_Cleverscope 4
typedef uint16_t  T_TransferChans;
#define T_TransferChans_ChanA 0
#define T_TransferChans_ChanB 1
#define T_TransferChans_ChanAB 2
typedef uint32_t  T_Channel;
#define T_Channel_ChanA 0
#define T_Channel_ChanB 1
#define T_Channel_ExtTrigger 2
#define T_Channel_DigTrig 3
#define T_Channel_LinkInput 4
#define T_Channel_ChanC 5
#define T_Channel_ChanD 6
#define T_Channel_ChanE 7
#define T_Channel_ChanF 8
#define T_Channel_ChanG 9
#define T_Channel_ChanH 10
#define T_Channel_ChanI 11
#define T_Channel_ChanJ 12
#define T_Channel_ChanK 13
#define T_Channel_ChanL 14
#define T_Channel_Dig2 15
typedef uint16_t  T_TriggerFilter;
#define T_TriggerFilter_None 0
#define T_TriggerFilter_LowPass 1
#define T_TriggerFilter_HiPass 2
#define T_TriggerFilter_Noise 3
typedef uint16_t  T_SigGenWaveform;
#define T_SigGenWaveform_sine 0
#define T_SigGenWaveform_triangle 1
#define T_SigGenWaveform_square 2
#define T_SigGenWaveform_DC 3
#define T_SigGenWaveform_OFF 4
typedef uint16_t  T_SigGenSweep;
#define T_SigGenSweep_Linear 0
#define T_SigGenSweep_Log 1
typedef uint16_t  T_SigGenFunc;
#define T_SigGenFunc_Standard 0
#define T_SigGenFunc_AutoAdvance 1
#define T_SigGenFunc_FreqModIn8 2
#define T_SigGenFunc_PhaseModIn8 3
typedef uint16_t  T_Trig2Function;
#define T_Trig2Function_None 0
#define T_Trig2Function_Trig12Min 1
#define T_Trig2Function_minT12Max 2
#define T_Trig2Function_Trig12Max 3
#define T_Trig2Function_CountTrig1 4
#define T_Trig2Function_CountTrig2 5
typedef uint16_t  T_Trigger2Source;
#define T_Trigger2Source_Trigger1Inverted 0
#define T_Trigger2Source_Trig2Defn 1
typedef uint8_t  T_LinkPort;
#define T_LinkPort_Debug 0
#define T_LinkPort_LinkOut 1
#define T_LinkPort_Disabled 2
#define T_LinkPort_Slave 3
#define T_LinkPort_Master 4
#define T_LinkPort_Uart 5
#define T_LinkPort_SPI 6
#define T_LinkPort_I2C 7
#define T_LinkPort_Digital 8
#define T_LinkPort_SigGen 9
typedef uint8_t  T_ExtSampleClock;
#define T_ExtSampleClock_IntClock 0
#define T_ExtSampleClock_ExtClockConst 1
#define T_ExtSampleClock_ExtClockVar 2
typedef uint16_t  T_SamplerResolution;
#define T_SamplerResolution__8Bit 0
#define T_SamplerResolution__10Bit 1
#define T_SamplerResolution__12Bit 2
#define T_SamplerResolution__14Bit 3
#define T_SamplerResolution__16Bit 4
typedef uint16_t  T_TransferSize;
#define T_TransferSize_Normal 0
#define T_TransferSize__100Buffer 1
#define T_TransferSize__50Buffer 2
#define T_TransferSize__10Buffer 3
#define T_TransferSize__5Buffer 4
#define T_TransferSize__2Buffer 5
#define T_TransferSize_Sequence 6
typedef struct {
	T_AcquireAction AcquireAction;
	T_AcquireMode AcquireMode;
	T_Acquirer Acquirer;
	double StartTime;
	double StopTime;
	T_TransferChans TransferChans;
	T_Channel TriggerSource;
	double TriggerAmplitude;
	T_TriggerFilter TriggerFilter;
	bool_t TrigSlope;
	double TriggerHoldoff;
	bool_t DigPatternRqd;
	uint32_t DigPattern;
	double ExtTrigThreshold;
	double DigInputThreshold;
	int16_t NumSeqFrames;
	int32_t NumBuffers;
	double SigGenFreq;
	double SigGenAmp;
	double SigGenOffset;
	T_SigGenWaveform SigGenWaveform;
	T_SigGenSweep SigGenSweep;
	T_SigGenFunc SigGenFunc;
	double SigGenDuty;
	double SigGenPhase;
	double SigGenFreqStep;
	T_Trig2Function Trig2Function;
	double MinTriggerPeriod;
	double MaxTriggerPeriod;
	uint32_t TriggerCount;
	bool_t Trig2Slope;
	T_Channel Trig2SourceChan;
	double Trig2Level;
	bool_t DigPattern2Rqd;
	uint32_t DigPattern2;
	T_Trigger2Source Trigger2Source;
	int32_t WaveformAverages;
	double FreqSpan;
	double FreqRes;
	double Duration;
	double Resolution;
	T_LinkPort LinkPort;
	T_ExtSampleClock ExtSampleClock;
	T_SamplerResolution SamplerResolution;
	T_TransferSize TransferSize;
	double FunctionNumber;
	double FunctionParameter;
	double FunctionResult;
	uint32_t LinkStart;
	uint32_t LinkTimebase;
	uint32_t LinkTimer;
	uint32_t LinkSetup;
	uint32_t SpareU321;
	uint32_t SpareU322;
	uint32_t SpareU323;
	uint32_t SpareU324;
	double ChartSampleRate;
	double SpareDBL2;
	double SpareDBL3;
	double SpareDBL4;
} T_AcquireSpec;
typedef struct {
	double StartTime;
	double StopTime;
	int32_t NumSamples;
	int32_t FrameNum;
} T_ReplaySpec;
typedef uint16_t  T_Interface;
#define T_Interface_USBFirstFound 0
#define T_Interface_EthernetFirstFound 1
#define T_Interface_EthernetIPAddress 2
#define T_Interface_EthernetOrUSBUseSerialNumber 3
#define T_Interface_EthernetOrUSBFirstFound 4
typedef struct {
	T_Interface Source;
	uint32_t TCPAdr;
	uint32_t TCPPort;
	uint32_t CAUSerNumHi;
	uint32_t CAUSerNumLo;
} T_InterfaceSpec;
typedef uint16_t  T_Probe;
#define T_Probe_x1 0
#define T_Probe_x10 1
#define T_Probe_x100 2
#define T_Probe_x1K 3
#define T_Probe_x2 4
#define T_Probe_x20 5
#define T_Probe_x50 6
#define T_Probe_x200 7
#define T_Probe_Vsat_0_15 8
#define T_Probe_Vsat_1_50 9
#define T_Probe_Vsat_15_0 10
#define T_Probe_Vsat_x2 11
typedef uint16_t  T_Coupling;
#define T_Coupling_AC 0
#define T_Coupling_DC 1
typedef uint16_t  T_FilterOption;
#define T_FilterOption_NoFilter 0
#define T_FilterOption__4xMA_2xExp 1
#define T_FilterOption__8xMA_4xExp 2
#define T_FilterOption__16xMA_8xExp 3
#define T_FilterOption__32xMA_16xExp 4
#define T_FilterOption__64xMA_32xExp 5
#define T_FilterOption__128xMA_64xExp 6
#define T_FilterOption_XXXxMA_128xExp 7
typedef struct {
	double Max;
	double Min;
	T_Probe Probe;
	T_Coupling Coupling;
	bool_t GlobalFilter;
	bool_t PreFilter20MHz;
	bool_t MA_Filter;
	bool_t Exp_Filter;
	T_FilterOption FilterOption;
} T_ChannelSpec;
typedef uint16_t  T_CAUStatus;
#define T_CAUStatus_RuntimeClosed 0
#define T_CAUStatus_Closed 1
#define T_CAUStatus_Open 2
#define T_CAUStatus_Fault 3
#define T_CAUStatus_FaultClosed 4
#define T_CAUStatus_OpenInit 5
typedef struct {
	double T0;
	double dt;
	int32_t n;
	double TTrig;
	int32_t Frame;
	int32_t NumFrames;
} T_T0dt;
typedef uint16_t  T_FunctionCommand;
#define T_FunctionCommand_GetID 0
#define T_FunctionCommand_GetFirmwareVer 1
#define T_FunctionCommand_GetDriverVer 2
#define T_FunctionCommand_GetResolution 3
#define T_FunctionCommand_GetFrameLength 4
#define T_FunctionCommand_GetTemperature 5
#define T_FunctionCommand_StartLinkSend 6
#define T_FunctionCommand_SendLinkData 7
#define T_FunctionCommand_ReadLinkData 8
#define T_FunctionCommand_ActiveMessage 9
#define T_FunctionCommand_Calibrate 10
#define T_FunctionCommand_SetCalRef 11
#define T_FunctionCommand_SamplingStatus 12
#define T_FunctionCommand_TfOrDTCapture 13
#define T_FunctionCommand_SigDC 14
#define T_FunctionCommand_SigRMS 15
#define T_FunctionCommand_SigMax 16
#define T_FunctionCommand_SigMin 17
#define T_FunctionCommand_SigPkPk 18
#define T_FunctionCommand_SigStdDev 19
#define T_FunctionCommand_SigFreq 20
#define T_FunctionCommand_SigAmplitude 21
#define T_FunctionCommand_SigPulseFrequency 22
#define T_FunctionCommand_SigDutyCycle 23
#define T_FunctionCommand_SigPulsePeriod 24
#define T_FunctionCommand_SigPulseLength 25
#define T_FunctionCommand_SigRiseTime 26
#define T_FunctionCommand_SigFallTime 27
#define T_FunctionCommand_Sig1Level 28
#define T_FunctionCommand_Sig0Level 29
#define T_FunctionCommand_SigVSwing 30
#define T_FunctionCommand_SigOvershoot 31
#define T_FunctionCommand_SigSlewRate 32
#define T_FunctionCommand_SigFreq2ndHarmonic 33
#define T_FunctionCommand_SigAmp2ndHarmonic 34
#define T_FunctionCommand_SigFreq3rdHarmonic 35
#define T_FunctionCommand_SigAmp3ndHarmonic 36
#define T_FunctionCommand_SigSinad 37
#define T_FunctionCommand_SigTHD 38
#define T_FunctionCommand_SigHD23 39
typedef uint16_t  T_SpectrumType;
#define T_SpectrumType_RMS 0
#define T_SpectrumType_Power 1
#define T_SpectrumType_GainPhase 2
#define T_SpectrumType_ReIm 3
typedef uint16_t  T_FFTWindow;
#define T_FFTWindow_None 0
#define T_FFTWindow_Hanning 1
#define T_FFTWindow_Hamming 2
#define T_FFTWindow_BlackmanHarris 3
#define T_FFTWindow_ExactBlackman 4
#define T_FFTWindow_Blackman 5
#define T_FFTWindow_FlatTop 6
#define T_FFTWindow__4TermBHarris 7
#define T_FFTWindow__7TermBHarris 8
#define T_FFTWindow_LowSidelobe 9
typedef uint32_t  T_ConnectionInterface;
#define T_ConnectionInterface_Any 0
#define T_ConnectionInterface_USB 1
#define T_ConnectionInterface_Ethernet 2
typedef uint16_t  T_ConnectionMethod;
#define T_ConnectionMethod_FirstFound 0
#define T_ConnectionMethod_SerialNumber 1
#define T_ConnectionMethod_IPAddress 2
typedef uint32_t  T_SampleStatus;
#define T_SampleStatus_NotReady 0
#define T_SampleStatus_Ready 1
typedef uint16_t  T_ProbeIntExt;
#define T_ProbeIntExt_On_Internal 0
#define T_ProbeIntExt_On_Remote 1
#define T_ProbeIntExt_Off_Internal 2
#define T_ProbeIntExt_Sleep_Remote 3
typedef uint16_t  T_InterfaceType;
#define T_InterfaceType_Unknown 0
#define T_InterfaceType_USB 1
#define T_InterfaceType_TCP 2
#define T_InterfaceType_USBTCP 3
typedef uint16_t  T_CAU_Model;
#define T_CAU_Model_UnknownCAU 0
#define T_CAU_Model_CS328 1
#define T_CAU_Model_CS328A 2
#define T_CAU_Model_CS448 3
#define T_CAU_Model_CS548 4
typedef uint16_t  T_EthernetStatus;
#define T_EthernetStatus_NA 0
#define T_EthernetStatus_StaticAddress 1
#define T_EthernetStatus_DHCPWaitingForAddress 2
#define T_EthernetStatus_DHCPHaveAddress 3
typedef uint16_t  T_ProbeCompVCal;
#define T_ProbeCompVCal_VCal_0V 0
#define T_ProbeCompVCal_VCal_680mV 1
#define T_ProbeCompVCal_VCal_7500mV 2
typedef uint16_t  T_AcquireTask;
#define T_AcquireTask_Stop 0
#define T_AcquireTask_Single 1
#define T_AcquireTask_Automatic 2
#define T_AcquireTask_Triggered 3
#define T_AcquireTask_Chart 4
#define T_AcquireTask_Replay 5

/*!
 * CscopeControlDriver
 * 
 * Main command dispatcher for an opened Cleverscope acquisition unit.
 * This is the low-level entry point used by higher-level helper functions
 * (e.g. SetTrigger*, SetCapture*, GetSamples*). The behaviour is selected by
 * the Command enum (T_Command_*). Depending on Command, some structures and
 * buffers are treated as inputs, outputs, or both.
 * 
 * @brief Legacy monolithic driver interface (DEPRECATED).
 * 
 * @warning This function is retained for backward compatibility only.
 *          It provides a command-dispatch interface that handles
 *          acquisition, replay, configuration, control, and data transfer
 *          operations through a single entry point.
 * 
 * @deprecated New applications should use the dedicated, task-specific
 *             driver functions (e.g., Open, Close, Configure, Acquire,
 *             GetStatus, TransferData, etc.) instead of this function.
 * 
 * Design Notes:
 *  - This interface predates the modular driver architecture.
 *  - It routes commands internally based on the T_Command enum.
 *  - It requires multiple large parameter structures even when
 *    only a subset are relevant to the requested operation.
 *  - Error handling and behaviour depend on the specific command issued.
 * 
 * 
 * Recommendation:
 *  - Use this only for maintaining legacy software.
 *  - Do not use in new development.
 * CscopeControlDriver
 * 
 * Parameters:
 *  - AcquisitionUnit:
 *      Index/handle of an opened unit (returned by CscopeOpen).
 *  - Command:
 *      One of T_Command_* (Initialize/Acquire/WaitForSamples/Update/...).
 *  - AcquireSpec / ReplaySpec / InterfaceSpec:
 *      In/out configuration blocks for the requested operation.
 *  - ChannelSpec[] / ChannelSpecLength:
 *      Per-channel configuration array; length must match number of elements
 *      passed in ChannelSpec[].
 *  - GotSamples (out):
 *      Set TRUE when sample buffers are valid for reading.
 *  - CAUStatus (out):
 *      Current driver state/status (T_CAUStatus).
 *  - ChanA..ChanD (out):
 *      Sample buffers for analog channels (float). Only channels enabled /
 *      requested by the current spec are meaningful.
 *  - DigitalData (out):
 *      Digital sample buffer (uint16).
 *  - SampleBufferSize:
 *      Number of samples available in each provided buffer.
 *  - T0dt (out):
 *      Timing structure describing the returned samples (timebase, t0, dt, 
 * etc).
 * 
 * Returns:
 *  - 0 on success
 */
int32_t __stdcall CscopeControlDriver(int32_t AcquisitionUnit, 
	T_Command Command, T_AcquireSpec *AcquireSpec, T_ReplaySpec *ReplaySpec, 
	T_InterfaceSpec *InterfaceSpec, T_ChannelSpec ChannelSpec[], 
	int32_t ChannelSpecLength, bool_t *GotSamples, T_CAUStatus *CAUStatus, 
	float ChanA[], float ChanB[], float ChanC[], float ChanD[], 
	uint16_t DigitalData[], int32_t SampleBufferSize, T_T0dt *T0dt);
/*!
 * CscopeFunction
 * 
 * Sends a "function" command to the driver/firmware and returns a result.
 * 
 * This is used for miscellaneous operations that don't fit the core acquire/
 * replay command set (e.g. device-specific utilities, link port transactions,
 * querying special registers, etc.). The meaning of Parameter and returned
 * values depends on FunctionCommand.
 * 
 * Parameters:
 *  - AcquisitionUnit:
 *      Opened unit index/handle.
 *  - FunctionCommand:
 *      One of T_FunctionCommand_* selecting the function to execute.
 *  - Parameter:
 *      Numeric parameter passed to the function (meaning is 
 * command-specific).
 *  - LinkDataSend[] / LengthOfLinkDataSend:
 *      Optional payload to send over the link port (UART/SPI/I2C/etc).
 *  - FunctionResult (out):
 *      Primary numeric result for the function.
 *  - LinkDataReceived[] / LengthOfLinkDataReceived:
 *      Optional receive buffer for link port responses.
 *  - ResultA..ResultD (out):
 *      Additional numeric results (command-specific).
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeFunction(int32_t AcquisitionUnit, 
	T_FunctionCommand FunctionCommand, double Parameter, uint8_t LinkDataSend[], 
	int32_t LengthOfLinkDataSend, double *FunctionResult, 
	uint8_t LinkDataReceived[], int32_t LengthOfLinkDataReceived, 
	double *ResultA, double *ResultB, double *ResultC, double *ResultD);
/*!
 * CscopeGetDriverVersion
 * 
 * Returns the Cleverscope driver DLL version number.
 * 
 * Parameters:
 *  - DriverVersion (out):
 *      Double containing the driver version (e.g. 1.23). 
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeGetDriverVersion(double *DriverVersion);
/*!
 * CscopeGetSpectrum
 * 
 * Calculates FFT/spectrum results for the most recent acquired samples for 
 * the
 * specified acquisition unit.
 * 
 * The output arrays can represent real/imaginary components or 
 * magnitude/phase
 * (or power) depending on SpectrumType and display flags.
 * 
 * Parameters:
 *  - AcquisitionUnit:
 *      Opened unit index/handle.
 *  - SpectrumType:
 *      One of T_SpectrumType_* controlling the output representation.
 *  - FFTWindow:
 *      One of T_FFTWindow_* selecting the window function.
 *  - dBOn / DegreesOn / UnwrapPhase:
 *      Output formatting options.
 *  - dF (out):
 *      Frequency bin spacing (Hz).
 *  - n (out):
 *      Number of valid bins written to each output array.
 *  - Chan*RealOrMagnitudeOrPower[] / Chan*ImaginaryOrPhase[]:
 *      Output arrays for channels A..D.
 *  - BufferSize:
 *      Capacity (number of doubles) for each provided output array.
 * 
 */
int32_t __stdcall CscopeGetSpectrum(int32_t AcquisitionUnit, 
	T_SpectrumType SpectrumType, T_FFTWindow FFTWindow, bool_t dBOn, 
	bool_t DegreesOn, bool_t UnwrapPhase, double *dF, int32_t *n, 
	double ChanARealOrMagnitudeOrPower[], double ChanAImaginaryOrPhase[], 
	double ChanBRealOrMagnitudeOrPower[], double ChanBImaginaryOrPhase[], 
	double ChanCRealOrMagnitudeOrPower[], double ChanCImaginaryOrPhase[], 
	double ChanDRealOrMagnitudeOrPower[], double ChanDImaginaryOrPhase[], 
	int32_t BufferSize);
/*!
 * CscopeGetHardwareInformation
 * 
 * Returns basic hardware information for an opened Cleverscope unit.
 * 
 * Parameters:
 *  - AcquisitionUnit:
 *      Opened unit index/handle.
 *  - SerialNumber[] / SerialNumberLength (out):
 *      ASCII serial number string (buffer should be at least 8 bytes).
 *  - CAUType[] / CAUTypeLength (out):
 *      ASCII model/type string (buffer length as allocated by caller).
 *  - NumChannels (out):
 *      Number of analog channels supported by the unit.
 *  - ADCResolution (out):
 *      ADC resolution in bits (e.g. 8/10/12/14/16).
 *  - SigGenType[] / SigGenTypeLength (out):
 *      ASCII signal generator type string (if fitted).
 *  - IPAddress[] / IPAddressLength (out):
 *      ASCII IP address string for Ethernet units (buffer >= 16 recommended).
 *  - TCPPort (out):
 *      TCP port used for Ethernet communications.
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeGetHardwareInformation(int32_t AcquisitionUnit, 
	uint8_t SerialNumber[], int32_t SerialNumberLength, uint8_t CAUType[], 
	int32_t CAUTypeLength, int32_t *NumChannels, int32_t *ADCResolution, 
	uint8_t SigGenType[], int32_t SigGenTypeLength, uint8_t IPAddress[], 
	int32_t IPAddressLength, int32_t *TCPPort);
/*!
 * CscopeGetStatus
 * 
 * Queries the current driver state/status for an opened acquisition unit.
 * 
 * Parameters:
 *  - AcquisitionUnit:
 *      Opened unit index/handle.
 *  - CAUStatus (out):
 *      Current status (T_CAUStatus).
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeGetStatus(int32_t AcquisitionUnit, 
	T_CAUStatus *CAUStatus);
/*!
 * CscopeGetSamples
 * 
 * Retrieves the latest available sample buffers after an 
 * acquire/replay/stream
 * operation.
 * 
 * This is a convenience wrapper for the common case of returning up to 4 
 * analog
 * channels plus digital data in one call.
 * 
 * Parameters:
 *  - AcquisitionUnit:
 *      Opened unit index/handle.
 *  - GotSamples (out):
 *      Set TRUE if sample buffers are valid.
 *  - CAUStatus (out):
 *      Current status (T_CAUStatus).
 *  - ChanA..ChanD (out):
 *      Analog sample buffers (float).
 *  - DigitalData (out):
 *      Digital sample buffer (uint16). Each bit represents the state of one 
 * of each of the digital inputs.
 *  - SampleBufferSize:
 *      Capacity (samples) of each provided buffer.
 *  - T0dt (out):
 *      Timing information for the returned buffers.
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeGetSamples(int32_t AcquisitionUnit, 
	bool_t *GotSamples, T_CAUStatus *CAUStatus, float ChanA[], float ChanB[], 
	float ChanC[], float ChanD[], uint16_t DigitalData[], 
	int32_t SampleBufferSize, T_T0dt *T0dt);
/*!
 * CscopeOpen
 * 
 * Opens a connection to a Cleverscope unit and returns an
 * AcquisitionUnit handle/index used by subsequent calls.
 * 
 * Parameters:
 *  - UnitNum:
 *      Requested unit index (typically 0). For multi-unit systems this 
 *      selects the driver slot/handle
 *  - Interface (T_ConnectionInterface):
 *      Use one of the T_ConnectionInterface_* constants 
 *      (e.g. T_ConnectionInterface_Any, _USB, _Ethernet).
 *  - Method (T_ConnectionMethod):
 *      Use one of the T_ConnectionMethod_* constants 
 *      (e.g. T_ConnectionMethod_FirstFound, _SerialNumber, _IPAddress).
 *  - SerialNumber[]:
 *      Optional ASCII serial number string (can be empty if not used). 
 *      A Serial Number is typically 6 o7 characters, but up 8.
 *  - IPAddress[]:
 *      Optional ASCII IP address string (for Ethernet connections).
 *  - TCPPort:
 *      TCP port to connect to (The default 53270, unless otherwise 
 * configured).
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 */
int32_t __stdcall CscopeOpen(int32_t UnitNum, 
	T_ConnectionInterface Interface, T_ConnectionMethod Method, 
	char SerialNumber[], char IPAddress[], uint16_t TCPPort);
/*!
 * CscopeGetSampleStatus
 * 
 * Returns metadata about the current sample buffers for an opened unit, such
 * as whether samples are ready/valid and what capture mode they belong to.
 * 
 * Parameters:
 *  - UnitNum:
 *      Opened unit index/handle.
 *  - SampleStatus (out):
 *      Returned status structure (T_SampleStatus).
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeGetSampleStatus(int32_t UnitNum, 
	T_SampleStatus *SampleStatus);
/*!
 * CscopeSetInternalExternalDigitizer
 * 
 * Selects which digitizer is used for a given analog channel on the connected
 * Cleverscope (internal ADC vs an external digitizer module such as CS1200, 
 * if fitted).
 * 
 * Parameters:
 *  - UnitNum:
 *      Opened unit index/handle (typically 0 for a single connected unit).
 *  - Channel:
 *      Analog channel index (Chan A..D => 0..3).
 *  - IntExt:
 *      CscopeProbeInternalExternalControlUserInterface:
 *        0=On Internal, 1=On External, 2=Off Internal, 3=Sleep External.
 *  - Spare:
 *      Reserved for future use (set to 0).
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeSetInternalExternalDigitizer(int32_t UnitNum, 
	int32_t Channel, T_ProbeIntExt IntExt, int32_t Spare);
/*!
 * CscopeSearchForUnits
 * 
 * Scans for available Cleverscope units on supported interfaces (USB and/or
 * Ethernet) and returns the number of units found.
 * 
 * After a scan, call CscopeGetUnitDetails() and/or 
 * CscopeGetUnitEthernetDetails()
 * with SearchIndex values in the range [0 .. UnitCount-1] to retrieve 
 * details.
 * 
 * Parameters:
 *  - msSearchDuration:
 *      Maximum time (ms) to wait for the Ethernet scan portion (USB discovery 
 * is
 *      typically faster). A minimum internal scan period may apply depending 
 * on the 
 *      number interfaces. Expect approximately 5 seconds minimum.
 *  - DoScan:
 *      TRUE to perform a new scan; FALSE to reuse the previous scan results.
 *  - pUnitCount (out):
 *      Number of units found.
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeSearchForUnits(int32_t msSearchDuration, 
	bool_t DoScan, int32_t *pUnitCount);
/*!
 * CscopeGetUnitDetails
 * 
 * Returns basic details for a unit found by the most recent 
 * CscopeSearchForUnits().
 * 
 * Parameters:
 *  - SearchIndex:
 *      Index into the last scan results (0..UnitCount-1).
 *  - pAvailable (out):
 *      TRUE if the unit is currently available for opening.
 *  - pInterfaceType (out):
 *      Interface type (USB/Ethernet/etc).
 *  - pModel (out):
 *      Unit model identifier (CAUModel).
 *  - pSerialNumber[] / SerialNumberLength (out):
 *      ASCII serial number. Buffer should be at least 8 bytes.
 *  - pSamplePeriod (out):
 *      Smallest sample period (seconds) possible by the digitiser.
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeGetUnitDetails(int32_t SearchIndex, 
	bool_t *pAvailable, T_InterfaceType *pInterfaceType, T_CAU_Model *pModel, 
	char pSerialNumber[], int32_t SerialNumberLength, double *pSamplePeriod);
/*!
 * CscopeGetUnitEthernetDetails
 * 
 * Returns Ethernet configuration details for a unit found by the most 
 * recent
 * CscopeSearchForUnits().
 * 
 * Parameters:
 *  - SearchIndex:
 *      Index into the last scan results (0..UnitCount-1).
 *  - pDHCP (out):
 *      DHCP status (EthernetDHCPStatus).
 *  - pIPAddress[] / pIPAddressLength (out):
 *      ASCII IP address string. Buffer should be at least 16 bytes.
 *  - pTCPPort (out):
 *      TCP port reported by the unit.
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeGetUnitEthernetDetails(int32_t SearchIndex, 
	T_EthernetStatus *pDHCP, char pIPAddress[], int32_t pIPAddressLength, 
	uint16_t *pTCPPort);
/*!
 * CscopeClose
 * 
 * Closes an opened Cleverscope connection and releases resources associated
 * with the unit index/handle.
 * 
 * Parameters:
 *  - UnitNum:
 *      Opened unit index/handle.
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeClose(int32_t UnitNum);
/*!
 * CscopeSetProbeCompOutput
 * 
 * Configures the probe compensation / calibration output waveform.
 * 
 * This typically drives a calibration square-wave or similar reference signal
 * used to adjust probe compensation.
 * 
 * Parameters:
 *  - UnitNum:
 *      Opened unit index/handle.
 *  - Frequency:
 *      Output frequency in Hz.
 *  - Amplitude:
 *      Output amplitude in volts.
 *  - DutyPercent:
 *      Duty cycle in percent (0..100).
 *  - VCal:
 *      Calibration voltage selection (T_ProbeCompVCal).
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeSetProbeCompOutput(int32_t UnitNum, double Frequency, 
	double Amplitude, double DutyPercent, T_ProbeCompVCal VCal);
/*!
 * CscopeSetAnalogChannels
 * 
 * Applies analog front-end settings for a specific channel (coupling, range,
 * attenuation, offset, bandwidth limit, etc.) as described by T_ChannelSpec.
 * 
 * Parameters:
 *  - UnitNum:
 *      Opened unit index/handle.
 *  - Channel:
 *      Channel index (0..n-1).
 *  - Settings:
 *      Pointer to a T_ChannelSpec structure containing desired settings.
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeSetAnalogChannels(int32_t UnitNum, int32_t Channel, 
	T_ChannelSpec *Settings);
/*!
 * CscopeSetCapturePeriod
 * 
 * Sets the acquisition time window for captures (start and stop time). Note 
 * that this does not specify the range of samples that will be returned once 
 * a sample acquisition has occured (known as a replay). To define the period 
 * that will be replayed when fetching the samples (such as using 
 * CscopeGetSamples, or CscopeGetSamples2AnalogChannels or similar functions) 
 * then ensure you call the function "CscopeSetReplayDetails" also.  Those 
 * replay Start and Stop times define which period of the capture is replayed 
 * (fetched) from the Cleverscope hardware.  Typically the Start and Stop 
 * times of both functions will be the same.
 * 
 * Parameters:
 *  - UnitNum:
 *      Opened unit index/handle.
 *  - AcquireStartTime:
 *      Start time relative to trigger/event (seconds).
 *  - AcquireStopTime:
 *      Stop time relative to trigger/event (seconds). Must be greater than 
 * Start time.
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeSetCapturePeriod(int32_t UnitNum, 
	double AcquireStartTime, double AcquireStopTime);
/*!
 * CscopeSetCaptureType
 * 
 * Selects the capture mode and buffer/sequence configuration.
 * 
 * Parameters:
 *  - UnitNum:
 *      Opened unit index/handle.
 *  - AcquireMode:
 *      T_AcquireMode_* (Sampled/PeakCaptured/Filtered/Repetitive/etc).
 *  - SamplerResolution:
 *      T_SamplerResolution_* (8/10/12/14/16 bit).
 *  - NumberOfBuffers:
 *      Number of acquisition buffers to use (for streaming/charting/etc).
 *  - NumberOfSequenceFrames:
 *      Number of frames in a sequence acquisition (for segmented memory).
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeSetCaptureType(int32_t UnitNum, 
	T_AcquireMode AcquireMode, T_SamplerResolution SamplerResolution, 
	int32_t NumberOfBuffers, int16_t NumberOfSequenceFrames);
/*!
 * CscopeSetReplayDetails
 * 
 * Configures what samples are actually returned following a capture. It is 
 * important to call this function before performing an acquisition, and 
 * retrieving samples from the Driver. The replay Start and Stop times define 
 * which period of the capture is replayed (fetched) from the Cleverscope 
 * hardware. These Start and Stop 
 * times need to be within the Start and Stop Times that are specified in the  
 * "CscopeSetCapturePeriod" function. This function needs to be called along 
 * with the "CscopeSetCapturePeriod" before starting an aquisition. Typically 
 * the Start and Stop times of both functions will be the same. However this 
 * function allows the user to drill down into the captured sample set to 
 * return specific parts of the waveform, with a specified number of samples 
 * being returned.
 * 
 * Parameters:
 *  - UnitNum:
 *      Opened unit index/handle.
 *  - FrameNumber:
 *      Frame index to replay (1-based). 0 = the current Frame.
 *  - ReplayStartTime / ReplayStopTime:
 *      Time window for the replay (seconds).
 *  - NumberOfSamples:
 *      Number of samples to return in replay mode.
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeSetReplayDetails(int32_t UnitNum, 
	int32_t FrameNumber, double ReplayStartTime, double ReplayStopTime, 
	int32_t NumberOfSamples);
/*!
 * CscopeSetSignalGenerator
 * 
 * Configures the internal signal generator output waveform.
 * 
 * Parameters:
 *  - UnitNum:
 *      Opened unit index/handle.
 *  - Waveform:
 *      T_SigGenWaveform_* (sine/triangle/square/DC/OFF).
 *  - Frequency:
 *      Output frequency in Hz (ignored for DC/OFF).
 *  - Amplitude:
 *      Output amplitude in volts.
 *  - DutyPercentage:
 *      Duty cycle in percent for square wave.
 *  - DCOffset:
 *      DC offset applied to the waveform (volts).
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeSetSignalGenerator(int32_t UnitNum, 
	T_SigGenWaveform Waveform, double Frequency, double Amplitude, 
	double DutyPercentage, double DCOffset);
/*!
 * CscopeSetTransferSize
 * 
 * Selects the transfer size / buffering strategy used when moving sample 
 * data
 * from the device to the host (affects throughput vs latency).
 * 
 * Parameters:
 *  - UnitNum:
 *      Opened unit index/handle.
 *  - TransferSize:
 *      T_TransferSize_* (Normal / 100Buffer / 50Buffer / ... / Sequence).
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeSetTransferSize(int32_t UnitNum, 
	T_TransferSize TransferSize);
/*!
 * CscopeSetTriggerOnePattern
 * 
 * Enables and sets the digital pattern used by Trigger 1 (if supported).
 * 
 * Parameters:
 *  - UnitNum:
 *      Opened unit index/handle.
 *  - Active:
 *      TRUE to enable digital pattern qualification.
 *  - Pattern:
 *      Bit pattern
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeSetTriggerOnePattern(int32_t UnitNum, 
	bool_t Active, uint32_t Pattern);
/*!
 * CscopeSetTriggerOne
 * 
 * Configures Trigger 1 (source, slope, threshold, filter, and holdoff).
 * 
 * Parameters:
 *  - UnitNum:
 *      Opened unit index/handle.
 *  - Source:
 *      Trigger source channel (T_Channel_*).
 *  - Slope:
 *      FALSE = rising, TRUE = falling (or vice versa).
 *  - Amplitude:
 *      Trigger threshold level (volts).
 *  - Filter:
 *      Trigger input filter (T_TriggerFilter_*).
 *  - Holdoff:
 *      Holdoff time (seconds) between triggers.
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeSetTriggerOne(int32_t UnitNum, T_Channel Source, 
	bool_t Slope, double Amplitude, T_TriggerFilter Filter, double Holdoff);
/*!
 * CscopeSetTriggerTwoPattern
 * 
 * Enables and sets the digital pattern used by Trigger 2 (if supported).
 * 
 * Parameters:
 *  - UnitNum:
 *      Opened unit index/handle.
 *  - Active:
 *      TRUE to enable digital pattern qualification.
 *  - Pattern:
 *      Bit pattern to match.
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeSetTriggerTwoPattern(int32_t UnitNum, 
	bool_t Active, uint32_t Pattern);
/*!
 * CscopeSetTriggerTwo
 * 
 * Configures Trigger 2 (secondary trigger) parameters.
 * 
 * Trigger 2 can be used for period measurement, qualifying Trigger 1, 
 * counting,
 * or other advanced triggering depending on Trig2Function.
 * 
 * Parameters:
 *  - UnitNum:
 *      Opened unit index/handle.
 *  - SourceChannel:
 *      Source channel for Trigger 2 (T_Channel_*).
 *  - Amplitude:
 *      Trigger 2 threshold level (volts).
 *  - Slope:
 *      FALSE = rising, TRUE = falling
 *  - Trig2Function:
 *      T_Trig2Function_* selection (None/Min/Max/Count/etc).
 *  - TriggerCount:
 *      Count limit for counting modes.
 *  - MinTriggerPeriod / MaxTriggerPeriod:
 *      Period qualification limits (seconds) for min/max modes.
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeSetTriggerTwo(int32_t UnitNum, 
	T_Channel SourceChannel, double Amplitude, bool_t Slope, 
	T_Trig2Function Trig2Function, uint32_t TriggerCount, 
	double MinTriggerPeriod, double MaxTriggerPeriod);
/*!
 * CscopeSetLinkPort
 * 
 * Configures the link port mode (e.g. debug, UART, SPI, I2C, digital, 
 * sig-gen).
 * 
 * Parameters:
 *  - UnitNum:
 *      Opened unit index/handle.
 *  - Mode:
 *      Link port mode (T_LinkPort_*).
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeSetLinkPort(int32_t UnitNum, T_LinkPort Mode);
/*!
 * CscopeSetExternalSampleClock
 * 
 * Selects the sample clock source (internal vs external clocking).
 * 
 * Parameters:
 *  - UnitNum:
 *      Opened unit index/handle.
 *  - Mode:
 *      T_ExtSampleClock_* (internal, external constant, external variable).
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeSetExternalSampleClock(int32_t UnitNum, 
	T_ExtSampleClock Mode);
/*!
 * CscopeSetChartSampleRate
 * 
 * Sets the sample rate used for "chart" / streaming mode (if supported).
 * 
 * Parameters:
 *  - UnitNum:
 *      Opened unit index/handle.
 *  - SampleRateHz:
 *      Requested sample rate in Hz.
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeSetChartSampleRate(int32_t UnitNum, 
	double SampleRateHz);
/*!
 * CscopeGetClockAndSampleRate
 * 
 * Returns sample clock and pulse generator clock information for the unit.
 * 
 * Parameters:
 *  - UnitNum:
 *      Opened unit index/handle.
 *  - SampleClockPeriod / SampleClockFrequency (out):
 *      Sample clock period (s) and frequency (Hz).
 *  - PulseGeneratorClockPeriod / PulseGeneratorClockFrequency (out):
 *      Probe-comp / pulse generator clock period (s) and frequency (Hz).
 *  - MinimumPulseClockPeriods (out):
 *      Minimum number of pulse clock periods per transition.
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeGetClockAndSampleRate(int32_t UnitNum, 
	double *SampleClockPeriod, double *SampleClockFrequency, 
	double *PulseGeneratorClockPeriod, double *PulseGeneratorClockFrequency, 
	uint32_t *MinimumPulseClockPeriods);
/*!
 * CscopeFinish
 * 
 * Shuts down the driver runtime and releases global resources.
 * 
 * Call this once when the application is closing (after closing all units).
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeFinish(void);
/*!
 * CscopeWaitForStatus
 * 
 * Blocks until the acquisition unit reaches a specified status or times out.
 * 
 * Parameters:
 *  - AcquisitionUnit:
 *      Opened unit index/handle.
 *  - StatusToWaitFor:
 *      Target status (T_CAUStatus).
 *  - Timeout_ms:
 *      Maximum time to wait in milliseconds.
 *  - StatusMatch (out):
 *      TRUE if target status was reached before timeout.
 *  - TimeWaited (out):
 *      Actual time waited in milliseconds.
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeWaitForStatus(int32_t AcquisitionUnit, 
	T_CAUStatus StatusToWaitFor, int32_t Timeout_ms, bool_t *StatusMatch, 
	int32_t *TimeWaited);
/*!
 * CscopeWaitForSamplesReady
 * 
 * Convenience wait that blocks until samples are ready to be read (or 
 * timeout).
 * 
 * Parameters:
 *  - AcquisitionUnit:
 *      Opened unit index/handle.
 *  - Timeout_ms:
 *      Maximum time to wait in milliseconds.
 *  - StatusMatch (out):
 *      TRUE if samples became ready before timeout.
 *  - TimeWaited (out):
 *      Actual time waited in milliseconds.
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeWaitForSamplesReady(int32_t AcquisitionUnit, 
	int32_t Timeout_ms, bool_t *StatusMatch, int32_t *TimeWaited);
/*!
 * CscopeSetAcquireTask
 * 
 * Requests the driver to start/stop an acquisition task (single, automatic,
 * triggered, chart/streaming, replay).
 * 
 * Parameters:
 *  - UnitNum:
 *      Opened unit index/handle.
 *  - AcquireTask:
 *      T_AcquireTask_* selection.
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeSetAcquireTask(int32_t UnitNum, 
	T_AcquireTask AcquireTask);
/*!
 * CscopeGetSamples1AnalogChannel
 * 
 * Retrieves samples for a single analog channel into a caller-provided 
 * buffer.
 * 
 * Use this when you only need one channel and want to avoid transferring or
 * allocating buffers for other channels.
 * 
 * Parameters:
 *  - AcquisitionUnit:
 *      Opened unit index/handle.
 *  - Channel:
 *      Channel identifier (T_Channel_*). For analog channels use 
 * ChanA..ChanD.
 *  - Final:
 *      TRUE if this is the last GetSamples* call for the current capture; 
 * this
 *      will implicitly finalise/release the current sample set.
 *  - T0dt (out):
 *      Timing information for the returned buffer.
 *  - SamplesValid (out):
 *      TRUE if the returned buffer contains valid samples.
 *  - SampleBuffer[] / SampleBufferSize (out):
 *      Output float buffer and its capacity in samples.
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeGetSamples1AnalogChannel(int32_t AcquisitionUnit, 
	uint32_t Channel, bool_t Final, T_T0dt *T0dt, bool_t *SamplesValid, 
	float SampleBuffer[], int32_t SampleBufferSize);
/*!
 * CscopeGetSamples2AnalogChannels
 * 
 * Retrieves samples for two analog channels into caller-provided buffers.
 * 
 * Parameters:
 *  - AcquisitionUnit:
 *      Opened unit index/handle.
 *  - Channel1 / Channel2:
 *      Channel identifiers (T_Channel_*).
 *  - Final:
 *      TRUE to finalise/release the current sample set after this call.
 *  - T0dt (out):
 *      Timing information for the returned buffers.
 *  - SamplesValid (out):
 *      TRUE if the returned buffers contain valid samples.
 *  - SampleBuffer1[] / SampleBuffer2[] / SampleBufferSize (out):
 *      Output float buffers and their capacity in samples.
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeGetSamples2AnalogChannels(int32_t AcquisitionUnit, 
	uint32_t Channel1, uint32_t Channel2, bool_t Final, T_T0dt *T0dt, 
	bool_t *SamplesValid, float SampleBuffer1[], float SampleBuffer2[], 
	int32_t SampleBufferSize);
/*!
 * CscopeGetSamples4AnalogChannels
 * 
 * Retrieves samples for up to four analog channels into caller-provided 
 * buffers.
 * 
 * Parameters:
 *  - AcquisitionUnit:
 *      Opened unit index/handle.
 *  - Channel1..Channel4:
 *      Channel identifiers (T_Channel_*).
 *  - Final:
 *      TRUE to finalise/release the current sample set after this call.
 *  - T0dt (out):
 *      Timing information for the returned buffers.
 *  - SamplesValid (out):
 *      TRUE if the returned buffers contain valid samples.
 *  - SampleBuffer1..SampleBuffer4[] / SampleBufferSize (out):
 *      Output float buffers and their capacity in samples.
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeGetSamples4AnalogChannels(int32_t AcquisitionUnit, 
	uint32_t Channel1, uint32_t Channel2, uint32_t Channel3, uint32_t Channel4, 
	bool_t Final, T_T0dt *T0dt, bool_t *SamplesValid, 
	float SampleBuffer1[], float SampleBuffer2[], float SampleBuffer3[], 
	float SampleBuffer4[], int32_t SampleBufferSize);
/*!
 * CscopeGetSamplesDigitalChannel
 * 
 * Retrieves digital samples into a caller-provided buffer.
 * 
 * Parameters:
 *  - AcquisitionUnit:
 *      Opened unit index/handle.
 *  - Channel:
 *      Digital channel identifier. Set as 0. This is for future use.
 *      if there are multiple digital busses that can be returned.
 *  - Final:
 *      TRUE to finalise/release the current sample set after this call.
 *  - T0dt (out):
 *      Timing information for the returned buffer.
 *  - SamplesValid (out):
 *      TRUE if the returned buffer contains valid samples.
 *  - SampleBuffer[] / SampleBufferLength (out):
 *      Output uint16 buffer and its capacity in samples/words.
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeGetSamplesDigitalChannel(int32_t AcquisitionUnit, 
	uint32_t Channel, bool_t Final, T_T0dt *T0dt, bool_t *SamplesValid, 
	uint16_t SampleBuffer[], int32_t SampleBufferLength);
/*!
 * CscopeGetSamplesFinalise
 * 
 * Releases the current capture's sample buffers within the driver.
 * 
 * Call this after you have finished reading samples using any of the
 * CscopeGetSamples*() functions, unless you set Final=TRUE on your last
 * GetSamples* call (which performs the finalise automatically).
 * 
 * Parameters:
 *  - AcquisitionUnit:
 *      Opened unit index/handle.
 * 
 * Returns:
 *  - 0 on success; non-zero error code on failure.
 * 
 */
int32_t __stdcall CscopeGetSamplesFinalise(int32_t AcquisitionUnit);
/*!
 * CscopeDisplayDebugWindow
 * 
 * Show a debug logging window, and enable logging in the driver. Each 
 * connected
 * Cleverscope device will have it's own logging window displayed.s
 * 
 * Parameters:
 *  - ShowWindow:
 *      Set true to display the driver debug log windows.
 *      This will open a seperate window for each connected Cleverscope.
 * 
 * Returns:
 *  - >=0 AcquisitionUnit index/handle on success.
 * 
 */
int32_t __stdcall CscopeDisplayDebugWindow(bool_t ShowWindow);

/*!
 * LVDLLStatus
 *
 * LabVIEW-generated helper used to retrieve a textual description of the last
 * DLL error/status for this module.
 *
 * Parameters:
 *  - errStr / errStrLen (out):
 *      Caller-provided buffer to receive a null-terminated error string.
 *  - module:
 *      Module handle provided by LabVIEW runtime.
 *
 * Returns:
 *  - LabVIEW MgErr code (0 on success).
 */
MgErr __cdecl LVDLLStatus(char *errStr, int errStrLen, void *module);



/*!
 * SetExecuteVIsInPrivateExecutionSystem
 *
 * LabVIEW-generated helper that controls whether VIs started by this DLL run
 * in the private execution system.
 *
 * Parameters:
 *  - value:
 *      TRUE to execute VIs in the private execution system, FALSE to use the
 *      default execution system.
 */
void __cdecl SetExecuteVIsInPrivateExecutionSystem(bool32_t value);

#ifdef __cplusplus
} // extern "C"
#endif


#endif