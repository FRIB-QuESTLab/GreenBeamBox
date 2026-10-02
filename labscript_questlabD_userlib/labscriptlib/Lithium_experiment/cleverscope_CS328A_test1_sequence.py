from labscript import start, stop, add_time_marker, AnalogOut, DigitalOut, IntermediateDevice
from labscriptlib.Questlab.connection_table import ConnectionTable


ConnectionTable()

# Begin issuing labscript primitives
# A timing variable t is used for convenience
# start() elicits the commencement of the shot

t = 0
start()
cs328A_chA.acquire(label='',start_time=-1,end_time=-1)  # this arms the oscilloscope. It will wait for a trigger to start acquiring. 
cs328A_chB.acquire(label='',start_time=-1,end_time=-1)  

# t+=1
# dummy_ao0.constant(t, 1)

# t+=1
# dummy_ao1.constant(t, 1)

t+=2
do9.go_high(t=t)  # this trigger oscilloscope to start acquiring

t+=0.003
do9.go_low(t=t)


t+=3
do9.go_high(t=t)  

t+=0.003
do9.go_low(t=t)

t+=0.003
# Stop the experiment shot with stop()
stop(t)

