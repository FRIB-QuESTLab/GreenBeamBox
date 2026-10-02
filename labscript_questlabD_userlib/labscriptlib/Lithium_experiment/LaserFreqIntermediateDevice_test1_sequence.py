from labscript import start, stop, add_time_marker, AnalogOut, DigitalOut, IntermediateDevice
from labscriptlib.Questlab.connection_table import ConnectionTable

ConnectionTable()


# Begin issuing labscript primitives
# A timing variable t is used for convenience
# start() elicits the commencement of the shot

t = 0
start()

# MUST INITIALIZE ALL LASER CHANNEL FREQUENCIES
laser_ch15.set_frequency_constant(f_scan)

t+=0.05

# TODO: do triggers at 20 Hz
for i in range(n_averages):
    do9.go_high(t)
    t+= trigger_duration 
    do9.go_low(t)
    t += 1/repetition_rate - trigger_duration
    
t += 0.05

# Stop the experiment shot with stop()
stop(t)

