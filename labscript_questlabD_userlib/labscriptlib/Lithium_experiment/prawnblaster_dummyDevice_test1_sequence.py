# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 11:43:00 2026

@author: mikisilv
"""

from labscript import start, stop, add_time_marker, AnalogOut, DigitalOut, IntermediateDevice
from labscriptlib.Questlab.connection_table import ConnectionTable


ConnectionTable()


# Begin issuing labscript primitives
# A timing variable t is used for convenience
# start() elicits the commencement of the shot
t = 0
dt = 20e-3
# add_time_marker(t, "Start", verbose=True)
start()
dummy_ai0.acquire(name='dummy acquire', start_time=1*dt, end_time=5*dt)


t += 3*dt
dummy_ao1.constant(t=t, value=1)

t += 4*dt
# Stop the experiment shot with stop()
stop(t)