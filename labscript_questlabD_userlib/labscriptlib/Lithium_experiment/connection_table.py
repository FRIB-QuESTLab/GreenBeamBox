from labscript import *
from user_devices.MokuGo_AIO.labscript_devices import MokuGoAIO
from user_devices.CleverScope_CS328A.labscript_devices import CleverScope_CS328A
from user_devices.LaserFreqIntermediateDevice.labscript_devices import LaserFreqIntermediateDevice
from user_devices import ScopeChannel
from user_devices import FrequencyOut

from labscript_devices.PrawnBlaster.labscript_devices import PrawnBlaster
from labscript_devices.DummyIntermediateDevice import DummyIntermediateDevice
from labscript_devices.PrawnDO.labscript_devices import PrawnDO


def ConnectionTable():
    PrawnBlaster(name='prawnblaster', com_port='COM5', pico_board='pico2', num_pseudoclocks=4, out_pins=[9,11,13,15])
    
    PrawnDO(name='prawn_do', com_port='COM4', pico_board='pico2', clock_line=prawnblaster.clocklines[1])
    DigitalOut('do9', prawn_do.outputs, 'do9')
    DigitalOut('do11', prawn_do.outputs, 'do11')
    DigitalOut('do13', prawn_do.outputs, 'do13')
    DigitalOut('do15', prawn_do.outputs, 'do15')

    
    CleverScope_CS328A(name='cs328A',
                       serialNumber='LW8675',
                       parent_device=prawnblaster.clocklines[0],
                       num_AI=2, 
                       startTime = -0.0005,
                       stopTime = (10/30)*1.01,  # duration of the shot, plus a little more
                       minVoltage_a = -0.95,
                       maxVoltage_a = 0.05,
                       minVoltage_b = -0.05,
                       maxVoltage_b = 0.95,
                       numSamples = int(2e6),
                       triggerChannel = 'ext',
                       triggerLevel=0.5,
                       triggerMode = 'Single',
                       coupling='DC')
    AnalogIn(name='cs328A_chA', parent_device=cs328A, connection='chA')
    AnalogIn(name='cs328A_chB', parent_device=cs328A, connection='chB')
    
        
    LaserFreqIntermediateDevice(name='laserFreqControl', ip='192.168.100.71', port=49153)
    FrequencyOut(name='laser_ch15', parent_device=laserFreqControl, connection='15')
    
    
    DummyIntermediateDevice(name='dummy', parent_device=prawnblaster.clocklines[0])
    AnalogOut(name='dummy_ao0', parent_device=dummy, connection='')
    AnalogOut(name='dummy_ao1', parent_device=dummy, connection='')



if __name__ == '__main__':
    ConnectionTable()
    # Begin issuing labscript primitives
    # start() elicits the commencement of the shot
    start()
    # Stop the experiment shot with stop()
    stop(1)
