# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 16:02:40 2026

@author: mikisilv
"""

import labscript_devices

labscript_devices.register_classes(
    'CleverScope_CS328A',
    BLACS_tab='user_devices.CleverScope_CS328A.blacs_tab.CleverScope_CS328ATab',
    runviewer_parser='')