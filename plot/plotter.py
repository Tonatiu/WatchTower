from Tkinter import *
import matplotlib
from matplotlib.figure import Figure
import numpy as np
import threading

class PlotterWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.TCP_labels = ["TCP Inputs", "TCP In errors", "TCP Outputs"]
        self.TCP_colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
        self.TCP_labels = ["UDP Inputs", "UDP In errors", "UDP Outputs"]
        self.TCP_colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
        self.initUI()

    def initUI(self):
        figure = Figure(figsize=(6, 5), dpi=100)
        TCP_Pie = figure.add_subplot(121)
        TCP_Pie.set_aspect('equal')
        UDP_Pie = figure.add_subplot(122)
        UDP_Pie.set_aspect('equal')
        canvas = FigureCanvasTkAgg(figure, self)
        canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=0)



    def update(self):
        counter = 0
        while True:
            TCP_Pie.clear()
            UDP_Pie.clear()
            
            TCP_Pie.pie(sizes, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90,
            radius=0.45, center=(.5, .5), frame=True)

            UDP_Pie.pie(sizes, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90,
            radius=0.45, center=(.5, .5), frame=True)
            sizes[counter % 4] = ((sizes[counter % 4] * counter) % 200) + 1
            canvas.draw()
            counter = (counter + 1) % 200

    def start_draw():
        updater = threading.Thread(target=update)
        updater.start()
