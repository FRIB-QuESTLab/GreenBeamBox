# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 16:02:40 2026

@author: mikisilv
"""

import labscript_devices

labscript_devices.register_classes(
    'MokuGoAIO',
    # BLACS_tab='naqslab_devices.TektronixTDS.blacs_tab.TDS_ScopeTab',
    BLACS_tab='user_devices.MokuGo_AIO.blacs_tab.MokuGoAIOTab',
    runviewer_parser='')