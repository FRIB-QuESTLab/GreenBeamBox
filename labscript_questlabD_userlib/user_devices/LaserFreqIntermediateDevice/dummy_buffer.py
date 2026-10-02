# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 16:09:36 2026

@author: mikisilv
"""
import socket
from moku.instruments import Oscilloscope
import time

def build_msg(frequency_THz, channel):
    '''
    builds message that is parsed by laser control labview VI
    frequency_THz: float, set frequency
    channel: int, laser channel to set.
    '''
     
    base_str = 'CMD:FREQ' + str(channel) + '=' + '{:.6f}'.format(frequency_THz) + '\r\n'
    return base_str.encode()
         
            
def connect_to_scope(ip_moku):
    scope = Oscilloscope(ip_moku, force_connect=True)
    print('connected to scope')
    scope.set_timebase(t1=0,t2=1e-7,max_length=128)
    scope.set_trigger(level=0.5,source='Input1',mode='Normal')
    scope.set_acquisition_mode('Normal')
    time.sleep(3)   # wait for Moku stuff to settle. DO NOT SKIP THIS STEP
    
    ## testing the timing of get_data():
    # t0 = time.perf_counter()
    # scope.get_data(wait_complete=False)  # wait for trigger. Will block until trigger is received.
    # tf = time.perf_counter()
    # print(tf-t0)
    print('scope trigger and acquisition settings set')

    return scope


def receive_from_labscript(ip_local, port_local, delimiter=b'\r'):
    buffer = b''
    # set local server with local ip and some port to listen for labscript msg
    s_local = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_local.bind((ip_local,port_local))
    s_local.listen(1)
    print('server listening...')

    s_labscript, ip_labscript = s_local.accept()
    print('connected to: ', ip_labscript)
    s_local.close()

    # retrieve data from buffer until end-of-message character is received
    while delimiter not in buffer:
        data = s_labscript.recv(4096)
        s_labscript.close()
        if not data:
            raise ConnectionError('Socket closed before delimiter found')
        buffer += data
    buffer = buffer.decode()
    freq_msg, delimiter_ = buffer.partition('-')[::2]
    
    print('received:\n', repr(freq_msg))
    return freq_msg
    
    

# Connection settings
ip_moku = '[fe80::7269:79ff:feb9:5e32]'  # corresponds to moku 006028
scope = connect_to_scope(ip_moku)

ip_laser = ''  
port_laser = -1
ch = -1

ip_local = '127.0.0.1'
port_local = 5050                 


# receive message from labscript containing all frequencies in frequency scan.
freq_msg = receive_from_labscript(ip_local, port_local).split()

# set range to skip last step. Last step corresponds to the stop() command in 
# the experimental sequence, which should not change the laser frequency
print('Last step from message removed. Last step corresponds to the stop() command in the experimental sequence, which should not change the laser frequency')
for ith_step in range(len(freq_msg)-1):  
    # wait for trigger. Will block until trigger is received.
    scope.get_data(wait_complete=False)  
    print('scope triggered')
    
    f_per_channel = freq_msg[ith_step].split(',')[:-1]  # remove last entry, should be empty string
    for ith_channel in range(0,len(f_per_channel),2):  # len(f_per_channel) should always be multiple of 2
        ch = int(f_per_channel[ith_channel])
        f = float(f_per_channel[ith_channel+1])
        msg_to_laser_computer = build_msg(f,ch)
        print(msg_to_laser_computer)
    print('\n')
        

# # wait for trigger, send TCP msg to laser computer when trigger is received.
# for f_THz in freq_scan:
#     
    
#     print('received trigger')
#     try:  # when unblocked, send message to laser computer
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         s.connect((ip_laser, port_laser))
#         msg = build_msg(f_THz,ch)
#         s.sendall(msg)
#         s.close()
#         print('message sent to laser computer')
        
#     except socket.error as e:
#         print(f"Failed to send TCP message: {e}")

#     # Optional: Add a brief break or condition if you only want 
#     # to catch a single trigger, otherwise it will loop for the next one.
#     break 


scope.relinquish_ownership()

