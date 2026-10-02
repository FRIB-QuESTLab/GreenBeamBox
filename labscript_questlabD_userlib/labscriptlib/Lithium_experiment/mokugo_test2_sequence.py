from labscript import start, stop, add_time_marker, AnalogOut, DigitalOut, IntermediateDevice
from labscriptlib.Questlab.connection_table import ConnectionTable


ConnectionTable()


# Begin issuing labscript primitives
# A timing variable t is used for convenience
# start() elicits the commencement of the shot
t = 0
# add_time_marker(t, "Start", verbose=True)
start()
moku_analog_out1.constant(value=3)
moku_analog_out2.constant(value=1)
# moku_analog_in1.acquire('Input 1 acquisition', start_time=0, end_time=1)
# moku_analog_in2.acquire('Input 2 acquisition', start_time=0, end_time=1)

# Wait for 1 second with all devices in their default state


t += 1
# Stop the experiment shot with stop()
stop(t)