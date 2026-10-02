# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 13:25:45 2026

@author: mikisilv
"""

from blacs.device_base_class import DeviceTab
from user_devices.MokuGo_AIO.blacs_worker import MokuGoAIOWorker

import labscript_utils.h5_lock
import h5py
from labscript_utils import dedent

class MokuGoAIOTab(DeviceTab):       
    def initialise_GUI(self):
        # Get capabilities from connection table properties:
        connection_table = self.settings['connection_table']
        properties = connection_table.find_by_name(self.device_name).properties
        
        self.ip6_address = self.BLACS_connection

        num_AO = 2
        num_AI = 2
        AO_base_units = 'V'
        AO_base_min, AO_base_max = -5,5
        AO_base_step = 0.001
        AO_base_decimals = 3

        # Create output object properties:
        AO_prop = {}
        for i in range(1,num_AO+1):
            AO_prop['Analog Channel %d' % i] = {
                'base_unit': AO_base_units,
                'min': AO_base_min,
                'max': AO_base_max,
                'step': AO_base_step,
                'decimals': AO_base_decimals,
            }

        # Create the output objects
        self.create_analog_outputs(AO_prop)

        # Create widgets for outputs defined so far (i.e. analog outputs only)
        _, AO_widgets, _ = self.auto_create_widgets()

        # Auto place the widgets in the UI, specifying sort keys for ordering them:
        self.auto_place_widgets(('MokuGO, Analog Output', AO_widgets))

        # Create and set the primary worker
        self.create_worker(
            "main_worker",
            'user_devices.MokuGo_AIO.blacs_worker.MokuGoAIOWorker',
            {
                'name': self.device_name,
                'ip6_address' : self.ip6_address,
                'Vmin': AO_base_min,
                'Vmax': AO_base_max,
                'num_AO': num_AO,
            },
        )
        self.primary_worker = "main_worker"

        # Only need an acquisition worker if we have analog inputs. It is important that
        # the acquisition worker is created after the wait monitor worker if there is
        # one, because the creation order determines the order that transition_to_manual
        # runs, and the acquisition processing requires processing that is done in the
        # wait monitor during transition_to_manual.
        # if num_AI > 0:
        #     self.create_worker(
        #         "acquisition_worker",
        #         'user_devices.MokuGo_AIO.blacs_workers.MokuGoAIWorker',
        #         {
        #             'name': self.device_name,
        #             'num_AI': num_AI,
        #         },
        #     )
        #     self.add_secondary_worker("acquisition_worker")

        
        
        