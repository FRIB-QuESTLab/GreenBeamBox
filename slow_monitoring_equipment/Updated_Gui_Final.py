# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 16:16:36 2026

@author: QUESTLAB
"""

#Necessary Imports
import tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import os
import numpy as np
from datetime import datetime

#Create Class
class Temp_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title('CBGB Temp monitor')

        # Initialize Files
        self.current_temp_file = None
        self.current_pressure_file = None
        
        # Set screen width to autosize
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        fig_w = (screen_w / 2) / 100
        fig_grid_h = (screen_h * 0.65) / 100
        fig_summary_h = (screen_h * 0.30) / 100

        # Adding Horizontal and Vertical Scrollbars
        container = tkinter.Frame(root)
        container.grid(row=0, column=0, sticky="nsew")

        self.canvas = tkinter.Canvas(container)
        v_scrollbar = tkinter.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        h_scrollbar = tkinter.Scrollbar(container, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Create Searchbar
        self.outer_frame = tkinter.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.outer_frame, anchor="nw")
        self.outer_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # Quit Button (row 0)
        self.quit = tkinter.Button(self.outer_frame, text="Quit", command=self._quit)
        self.quit.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        # Search bars (row 1)
        self._build_searchbar(column=0, label="Temp file (YYYY-MM-DD):", attr="temp_search")
        self._build_searchbar(column=1, label="Pressure file (YYYY-MM-DD):", attr="pressure_search")
        
        # Section Headings (row 2)
        tkinter.Label(self.outer_frame, text="Temperature", font=("Arial", 14, "bold")).grid(row=2, column=0)
        tkinter.Label(self.outer_frame, text="Pressure", font=("Arial", 14, "bold")).grid(row=2, column=1)
        
        # First figure (Temp channels)
        self.fig, self.ax = plt.subplots(3, 3, figsize=(fig_w, fig_grid_h), dpi=100)
        self.canvas_fig1 = FigureCanvasTkAgg(self.fig, master=self.outer_frame)
        self.canvas_fig1.get_tk_widget().grid(row=3, column=0)

        # Second figure (Pressure all)
        self.fig2, self.ax2 = plt.subplots(1, 1, figsize=(fig_w, fig_summary_h), dpi=100)
        self.canvas_fig2 = FigureCanvasTkAgg(self.fig2, master=self.outer_frame)
        self.canvas_fig2.get_tk_widget().grid(row=4, column=0)

        # Third figure (Pressure channels)
        self.fig3, self.ax3 = plt.subplots(3, 3, figsize=(fig_w, fig_grid_h), dpi=100)
        self.canvas_fig3 = FigureCanvasTkAgg(self.fig3, master=self.outer_frame)
        self.canvas_fig3.get_tk_widget().grid(row=3, column=1)

        # Fourth figure (Temp all)
        self.fig4, self.ax4 = plt.subplots(1, 1, figsize=(fig_w, fig_summary_h), dpi=100)
        self.canvas_fig4 = FigureCanvasTkAgg(self.fig4, master=self.outer_frame)
        self.canvas_fig4.get_tk_widget().grid(row=4, column=1)

        self._update_plots()
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)
        self.root.after(250, self._autosize_window)

    # Make Typing in the Searchbar Do Something
    def _build_searchbar(self, column, label, attr):
        frame = tkinter.Frame(self.outer_frame)
        frame.grid(row=1, column=column, sticky="w", padx=5, pady=4)

        tkinter.Label(frame, text=label).pack(side="left")

        entry = tkinter.Entry(frame, width=14)
        entry.pack(side="left", padx=4)
        setattr(self, attr, entry)  # e.g. self.temp_search, self.pressure_search

        kind = "temp" if "temp" in attr else "pressure"
        btn = tkinter.Button(frame, text="Search", command=lambda k=kind: self._search_file(k))
        btn.pack(side="left")

        # Allow pressing Enter in the box to trigger search
        entry.bind("<Return>", lambda e, k=kind: self._search_file(k))

        # Status label to show found/not-found feedback
        status = tkinter.Label(frame, text="", width=22, anchor="w", fg="gray")
        status.pack(side="left", padx=4)
        setattr(self, f"{attr}_status", status)
        
    # Make that Something looking in these file paths for a specific type of file
    def _search_file(self, kind):
        import glob, os
        # Base Directories
        temp_dir     = r"I:\QuESTlab\Data\GreenBeamBox\slow_monitoring_acquisition\lakeshore_218"
        pressure_dir = r"I:\QuESTlab\Data\GreenBeamBox\slow_monitoring_acquisition\agilent_xgs_600"

        # Search Temperature Directory
        if kind == "temp":
            date_str     = self.temp_search.get().strip()
            status_label = self.temp_search_status
            search_dir   = temp_dir
        # Search Pressure Directory
        else:
            date_str     = self.pressure_search.get().strip()
            status_label = self.pressure_search_status
            search_dir   = pressure_dir
        # If date is not entered, turn text red to show unavailability
        if not date_str:
            status_label.config(text="Enter a date first.", fg="red")
            return
            
        # Match text in searchbar to file
        matches = glob.glob(os.path.join(search_dir, f"*{date_str}*.txt"))

        # If there arent any matches, display that for clarity
        if not matches:
            status_label.config(text=f"No file found for {date_str}", fg="red")
        # Otherwise, turn text green, and create an access point to that file
        else:
            filepath = matches[0]
            status_label.config(text=os.path.basename(filepath), fg="green")
            
            if kind == "temp":
                self.current_temp_file = filepath
            else:
                self.current_pressure_file = filepath
                
            # Trigger the plots to refresh with the new file
            self._update_plots()

    def _autosize_window(self):
        self.root.update_idletasks()
        self.root.state('zoomed')

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _quit(self):
        self.root.quit()
        self.root.destroy()

    # Given a temp filepath, break the data into channels
    def get_temp_from_txt(self, filepath):
        f = open(filepath, 'r')
        a = f.readlines()
        f.close()
        
        t = []
        ch1 = []
        ch2 = []
        ch3 = []
        ch4 = []
        ch5 = []
        ch6 = []
        ch7 = []
        ch8 = []
        
        for i in range(len(a)):
            b = a[i].strip().split(',')
            t.append(b[0])
            ch1.append(float(b[1]))
            ch2.append(float(b[2]))
            ch3.append(float(b[3]))
            ch4.append(float(b[4]))
            ch5.append(float(b[5]))
            ch6.append(float(b[6]))
            ch7.append(float(b[7]))
            ch8.append(float(b[8]))
    
        t_seconds = []
        for i in range(len(t)):
            temp = t[i].split(':')
            seconds = float(temp[0])*3600 + float(temp[1])*60 + float(temp[2])
            t_seconds.append(seconds)
            
        t_seconds = np.array(t_seconds)
        ch1 = np.array(ch1)
        ch2 = np.array(ch2)
        ch3 = np.array(ch3)
        ch4 = np.array(ch4)
        ch5 = np.array(ch5)
        ch6 = np.array(ch6)
        ch7 = np.array(ch7)
        ch8 = np.array(ch8)
    
        return t_seconds, ch1, ch2, ch3, ch4, ch5, ch6, ch7, ch8

    # Given a pressure filepath, break it into channels
    def get_pressure_from_txt(self, filepath):
        with open(filepath, 'r') as f:
            a = f.readlines()

        t = []
        ch = [[] for _ in range(8)]

        for line in a:
            b = line.strip().split(',')
            t.append(b[0])
    
            for i in range(8):
                ch[i].append(float(b[i+1]))
    
        t_seconds = []
        for i in range(len(t)):
            pres = t[i].split(':')
            seconds = float(pres[0])*3600 + float(pres[1])*60 + float(pres[2])
            t_seconds.append(seconds)
    
        t_seconds = np.array(t_seconds)
    
        for i in range(8):
            ch[i] = np.array(ch[i])
    
        return t_seconds, ch

    # Plot channel data function
    def plot_channel_data(self, ax, ch_array, ch_label, t, ylim1, ylim2, ylabel, xlim1=8):
        ax.plot(t, ch_array, '.')
        ax.set_title(ch_label)
        ax.set_ylabel(ylabel)
        ax.set_xlabel('Time (hours)')
        ax.set_ylim(ylim1, ylim2)
        ax.set_xlim(left=xlim1)
        ax.grid()
        # plt.gca().invert_yaxis()   # Invert the y-axis
        # plt.gca().yaxis.set_major_locator(MaxNLocator(nbins=10))

    def plot_channel_data_pressure(self, ax, ch_array, ch_label, t, ylim1, ylim2, ylabel, xlim1=8):
        ax.plot(t, ch_array, '.')
        ax.set_title(ch_label)
        ax.set_ylabel(ylabel)
        ax.set_xlabel('Time (hours)')
        ax.set_ylim(ylim1, ylim2)
        ax.set_xlim(left=xlim1)
        ax.set_yscale('log')
        ax.grid()
        # plt.gca().invert_yaxis()   # Invert the y-axis
        # plt.gca().yaxis.set_major_locator(MaxNLocator(nbins=10))
        
    # Plot all channels on the same plot function
    def plot_all_channels(self, ax, all_channels, t, ylim1, ylim2, xlim1=8):
        for i in range(8):
            ax.plot(t, all_channels[i], '.', label='ch'+str(i+1))
            
        ax.set_title('All Channels')
        ax.set_xlabel('Time (hours)')
        ax.set_ylabel('Pressure (Torr)')
        ax.set_ylim(ylim1, ylim2)
        ax.set_xlim(left=xlim1)
        ax.grid()
        ax.legend()

    def plot_all_channels_pressure(self, ax, all_channels, t, ylim1, ylim2, xlim1=8):
        for i in range(8):
            ax.plot(t, all_channels[i], '.', label='ch'+str(i+1))
            
        ax.set_title('All Channels')
        ax.set_xlabel('Time (hours)')
        ax.set_ylabel('Pressure (Torr)')
        ax.set_ylim(ylim1, ylim2)
        ax.set_xlim(left=xlim1)
        ax.set_yscale('log')
        ax.grid()
        ax.legend()

    # Update the plots, given the prompting in the searchbar, to display the data
    def _update_plots(self):
        for ax_row in self.ax: 
            for a in ax_row: a.clear()
        for ax_row in self.ax3: 
            for a in ax_row: a.clear()
        self.ax2.clear()
        self.ax4.clear()
    
        left_xaxis_lim = 9.5
        
        if self.current_temp_file and os.path.exists(self.current_temp_file):
            low_4k, hi_4k = 0, 7
            low_40k, hi_40k = 25, 45
            
            data1 = self.get_temp_from_txt(self.current_temp_file)
            t_hours = data1[0] / 3600
            all_channels = data1[1:] 

            self.plot_all_channels(self.ax2, all_channels, t_hours, 0, 315, left_xaxis_lim)
            self.ax2.set_ylabel('Temperature (Kelvin)')
            self.plot_channel_data(self.ax[0,1], all_channels[0], 'ch1', t_hours, low_40k, hi_40k, 'Temperature (Kelvin)', left_xaxis_lim)
            self.plot_channel_data(self.ax[0,2], all_channels[1], 'ch2', t_hours, low_4k, hi_4k, 'Temperature (Kelvin)', left_xaxis_lim)
            self.plot_channel_data(self.ax[1,0], all_channels[2], 'ch3', t_hours, low_4k, hi_4k, 'Temperature (Kelvin)', left_xaxis_lim)
            self.plot_channel_data(self.ax[1,1], all_channels[3], 'ch4', t_hours, low_4k, hi_4k, 'Temperature (Kelvin)', left_xaxis_lim)
            self.plot_channel_data(self.ax[1,2], all_channels[4], 'ch5', t_hours, low_4k, hi_4k, 'Temperature (Kelvin)', left_xaxis_lim)
            self.plot_channel_data(self.ax[2,0], all_channels[5], 'ch6', t_hours, low_40k, hi_40k, 'Temperature (Kelvin)', left_xaxis_lim)
            self.plot_channel_data(self.ax[2,1], all_channels[6], 'ch7', t_hours, low_4k, hi_4k, 'Temperature (Kelvin)', left_xaxis_lim)
            self.plot_channel_data(self.ax[2,2], all_channels[7], 'ch8', t_hours, low_4k, hi_4k, 'Temperature (Kelvin)', left_xaxis_lim)

        if self.current_pressure_file and os.path.exists(self.current_pressure_file):
            low_pressure = 1e-7
            hi_pressure = 1e1
            
            pressure_data = self.get_pressure_from_txt(self.current_pressure_file)
            t_pres_hours = pressure_data[0] / 3600
            pres_channels = pressure_data[1]
           
            self.plot_all_channels_pressure(self.ax4, pres_channels, t_pres_hours, low_pressure, hi_pressure, left_xaxis_lim)
            self.plot_channel_data_pressure(self.ax3[0,1], pres_channels[0], 'ch1', t_pres_hours, low_pressure, hi_pressure, 'Pressure (Torr)', left_xaxis_lim)
            self.plot_channel_data_pressure(self.ax3[0,2], pres_channels[1], 'ch2', t_pres_hours, low_pressure, hi_pressure, 'Pressure (Torr)', left_xaxis_lim)
            self.plot_channel_data_pressure(self.ax3[1,0], pres_channels[2], 'ch3', t_pres_hours, low_pressure, hi_pressure, 'Pressure (Torr)', left_xaxis_lim)
            self.plot_channel_data_pressure(self.ax3[1,1], pres_channels[3], 'ch4', t_pres_hours, low_pressure, hi_pressure, 'Pressure (Torr)', left_xaxis_lim)
            self.plot_channel_data_pressure(self.ax3[1,2], pres_channels[4], 'ch5', t_pres_hours, low_pressure, hi_pressure, 'Pressure (Torr)', left_xaxis_lim)
            self.plot_channel_data_pressure(self.ax3[2,0], pres_channels[5], 'ch6', t_pres_hours, low_pressure, hi_pressure, 'Pressure (Torr)', left_xaxis_lim)
            self.plot_channel_data_pressure(self.ax3[2,1], pres_channels[6], 'ch7', t_pres_hours, low_pressure, hi_pressure, 'Pressure (Torr)', left_xaxis_lim)
            self.plot_channel_data_pressure(self.ax3[2,2], pres_channels[7], 'ch8', t_pres_hours, low_pressure, hi_pressure, 'Pressure (Torr)', left_xaxis_lim)

        self.fig.tight_layout()
        self.fig3.tight_layout()
        self.canvas_fig1.draw()
        self.canvas_fig2.draw()
        self.canvas_fig3.draw()
        self.canvas_fig4.draw()
        
        # Refresh and loop so that we'll always get current data
        self.root.after(15000, self._update_plots)
        
        
        
root = tkinter.Tk()
app = Temp_GUI(root)
root.mainloop()