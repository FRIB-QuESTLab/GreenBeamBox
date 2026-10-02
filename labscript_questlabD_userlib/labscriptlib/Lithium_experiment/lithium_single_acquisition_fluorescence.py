from labscript import start, stop, add_time_marker, AnalogOut, DigitalOut, IntermediateDevice, AnalogIn
from labscriptlib.Lithium_experiment.connection_table import ConnectionTable

ConnectionTable()



# Begin issuing labscript primitives
# A timing variable t is used for convenience
# start() elicits the commencement of the shot

t = 0
start()

# MUST INITIALIZE ALL LASER CHANNEL FREQUENCIES
laser_ch15.set_frequency_constant(f_scan)  # initialize frequency
cs328A_chA.acquire(label='fluorescence',start_time=-1,end_time=-1)  # will save data from channel A. Start and end times do nothing
cs328A_chB.acquire(label='absorption',start_time=-1,end_time=-1)  # will save data from channel B. Start and end times do nothing

# t+=10  # Make sure to wait enough time for laser frequency to settle. 

# send trigger pulses to YAG and oscilloscope at 20 Hz. Oscilloscope will 
# trigger only from the first pulse, then continously acquire until the shot is 
# done.  
for i in range(n_averages):
    do9.go_high(t)
    t += trigger_duration 
    do9.go_low(t)
    t += 1/YAG_repetitionRate - trigger_duration
    
t += 0.1

# Stop the experiment shot with stop()
stop(t)

