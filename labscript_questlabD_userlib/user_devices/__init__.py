# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 13:58:51 2026

@author: mikisilv

from NAQSlab devices __init__.py
https://github.com/naqslab/naqslab_devices/blob/master/__init__.py
"""
from labscript import Device, AnalogIn, StaticAnalogOut, StaticDDS, LabscriptError


class ScopeChannel(AnalogIn):
    """Subclass of labscript.AnalogIn that marks an acquiring scope channel.
    """
    description = 'Scope Acquisition Channel Class'

    def __init__(self, name, parent_device, connection):
        """This instantiates a scope channel to acquire during a buffered shot.

        Args:
            name (str): Name to assign channel
            parent_device (obj): Handle to parent device
            connection (str): Which physical scope channel is acquiring.
                              Generally of the form \'Channel n\' where n is
                              the channel label.
        """
        Device.__init__(self,name,parent_device,connection)
        self.acquisitions = []    
    
    
class FrequencyOut(StaticAnalogOut):
    """Subclass of labscript.AnalogIn that marks an acquiring scope channel.
    """
    description = 'Channel to send out set frequency instructions'

    def __init__(self, name, parent_device, connection):
        """This instantiates a scope channel to acquire during a buffered shot.

        Args:
            name (str): Name to assign channel
            parent_device (obj): Handle to parent device
            connection (str): Laser channel number. Ex: 1, 5, 11, 15
        """
        StaticAnalogOut.__init__(self,name,parent_device,connection)
        
        try: 
            con_int = int(connection)
        except ValueError:
            print()
            raise LabscriptError('connection must be a numeral string from 0 to 15. Ex: 1, 5, 15')
            
        if (con_int < 0) and (15 < con_int):
            raise LabscriptError('connection must be a numeral string from 0 to 15. Ex: 1, 5, 15')
            
    def set_frequency_constant(self,value):
        # wrapper function, just so the name in experimental sequence makes more sense.
        self.constant(value)

