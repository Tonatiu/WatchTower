#!/usr/bin/env python
# -*- coding: utf-8 -*-
from snmp_agent_managment import agent_manager
from Tkinter import *
import threading
import numpy as np
import time
from matplotlib import pyplot as plt
from matplotlib import animation
import tkSimpleDialog
import tkMessageBox
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

matplotlib.rcParams['font.size'] = 9.0

agente_manager = agent_manager.agent_manager()
#La clase permite generar gráficos de ciertos valores monitoreados
class PlotterWindow(Tk):
	def __init__(self, _id):
		Tk.__init__(self)
		self.TCP_labels = ["TCP Inputs", "TCP In errors", "TCP Outputs"]
		self.TCP_colors = ['yellowgreen', 'red', 'lightskyblue']
		self.TCP_values = [0, 0, 0]
		self.TCP_inputs = []
		self.TCP_Pie = None
		self.TCP_input_time_chart = None
		self.TCP_input_line = None

		self.UDP_labels = ["UDP Inputs", "UDP In errors", "UDP Outputs"]
		self.UDP_colors = ['gold', 'red', 'violet']
		self.UDP_values = [0, 0, 0]
		self.UDP_inputs = []
		self.UDP_Pie = None
		self.UDP_input_time_chart = None
		self.UDP_input_line = None

		self.init_inputs()
		self.time = np.linspace(0, 60, 60)		
		self.canvas = None
		self._id = _id
		self.active = True
		
		self.initUI()

	def initUI(self):
		figure = Figure(figsize=(8.5, 5), dpi=100)
		
		self.TCP_Pie = figure.add_subplot(221)
		self.TCP_Pie.set_aspect('equal')
		self.TCP_input_time_chart = figure.add_subplot(223)
		self.TCP_input_time_chart.set_ylabel('Segmentos por segundo')
		self.TCP_input_line, = self.TCP_input_time_chart.plot(self.time, self.TCP_inputs)
		
		self.UDP_Pie = figure.add_subplot(222)
		self.UDP_Pie.set_aspect('equal')
		self.UDP_input_time_chart = figure.add_subplot(224)
		self.UDP_input_time_chart.set_ylabel('Datagramas por segundo')
		self.UDP_input_line, = self.UDP_input_time_chart.plot(self.time, self.UDP_inputs)
		
		self.canvas = FigureCanvasTkAgg(figure, self)
		self.canvas.show()
		self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=0)

	def init_inputs(self):
		for i in range(60):
		    self.TCP_inputs.append(0)
		    self.UDP_inputs.append(0)

	def update(self):
		time_counter = 0
		tcp_inputs_persec = 0
		tcp_inputs_i = agente_manager.get_agent_tcpSegmentRecibed(self._id)
		tcp_inputs_f = 0
		
		udp_inputs_persec = 0
		udp_inputs_i = agente_manager.get_agent_udpInDatagrams(self._id)
		udp_inputs_f = 0

		tcp_limit = 10
		udp_limit = 10

		while self.active:
			self.TCP_Pie.clear()
			self.TCP_Pie.axis('off')
			self.UDP_Pie.clear()
			self.UDP_Pie.axis('off')
			if tcp_inputs_persec > tcp_limit:
				tcp_limit = tcp_inputs_persec + 50
			if udp_inputs_persec > udp_limit:
				udp_limit = udp_inputs_persec + 50
			self.TCP_input_time_chart.set_ylim([-.5, tcp_limit])
			self.UDP_input_time_chart.set_ylim([-.5, udp_limit])


			self.TCP_values[0] = agente_manager.get_agent_tcpSegmentRecibed(self._id)
			self.TCP_values[1] = agente_manager.get_agent_tcpErrorsRecibed(self._id)
			self.TCP_values[2] = agente_manager.get_agent_tcpOutSegs(self._id)
			tcp_inputs_f = agente_manager.get_agent_tcpSegmentRecibed(self._id)

			self.UDP_values[0] = agente_manager.get_agent_udpInDatagrams(self._id)
			self.UDP_values[1] = agente_manager.get_agent_udpInErrors(self._id)
			self.UDP_values[2] = agente_manager.get_agent_udpOutDatagrams(self._id)
			udp_inputs_f = agente_manager.get_agent_udpInDatagrams(self._id)

			self.TCP_Pie.pie(self.TCP_values, labels=self.TCP_labels, colors=self.TCP_colors,
			autopct='%.3f%%', shadow=True, startangle=100,
			radius=0.4, center=(.5, .5), frame=True, pctdistance=.45, labeldistance=.93)

			self.UDP_Pie.pie(self.UDP_values, labels=self.UDP_labels, colors=self.UDP_colors,
			autopct='%.3f%%', shadow=True, startangle=100,
			radius=0.4, center=(.5, .5), frame=True, pctdistance=.45, labeldistance=.93)

			if(tcp_inputs_f != tcp_inputs_i):
				tcp_inputs_persec = (tcp_inputs_f - tcp_inputs_i)
			if(udp_inputs_f != udp_inputs_i):
				udp_inputs_persec = (udp_inputs_f - udp_inputs_i)

			self.TCP_inputs.pop(0)
			self.TCP_inputs.append(tcp_inputs_persec)
			self.UDP_inputs.pop(0)
			self.UDP_inputs.append(udp_inputs_persec)
			
			self.TCP_input_line.set_ydata(self.TCP_inputs)
			self.UDP_input_line.set_ydata(self.UDP_inputs)
			
			tcp_inputs_i = tcp_inputs_f
			udp_inputs_i = udp_inputs_f
			self.canvas.draw()

	def start_draw(self):
		updater = threading.Thread(target=self.update)
		updater.start()
		self.wm_title("WatchTower SNMP Monitor: Gráficas")
		self.mainloop()

	def stop(self):
		self.active = False
#La clase permite mostrar un dialogo para agregar un host
class AddHostDialog(tkSimpleDialog.Dialog):
	def __init__(self, parent):
		tkSimpleDialog.Dialog.__init__(self, parent)
		self.parent = parent

	def body(self, master):

		Label(master, text="Host name:").grid(row=0)
		Label(master, text="Community:").grid(row=1)
		Label(master, text="Port:").grid(row=2)

		self.e1 = Entry(master)
		self.e2 = Entry(master)
		self.e3 = Entry(master)

		self.e1.grid(row=0, column=1)
		self.e2.grid(row=1, column=1)
		self.e3.grid(row=2, column=1)

		return self.e1 # initial focus

	def apply(self):
		host = str(self.e1.get())
		community = str(self.e2.get())
		if str(self.e3.get()) == "":
			port = 161
		else:
			port = int(self.e3.get())
		if community == "":
			community = "public"
		if host != "":
			self.parent.add_host_frame(host, community, int(port))
		else:
			tkMessageBox.showinfo("Parámetros requeridos", "Host name es un campo obligatorio")
#Esta clase genera un LabelFrame con los elementos necesarios para mostrar la información de un host
class InfoFrame(LabelFrame):
	def __init__(self, parent, label, id_):
		LabelFrame.__init__(self, parent, text=label)
		self.width = 350
		self.height = 200
		self.text = label
		self.id = id_
		self.values = []
		self.update = True
		self.initComps()
	#Permite inicializar los componentes del frame
	def initComps(self):
		#Creación de los labels para cada valor monitoreado
		info_lbl = Label(self, text="Tiempo de actividad:")
		info_lbl.grid(row=0, column=0)
		info_lbl = Label(self, text="Datagramas recibidos:")
		info_lbl.grid(row=1, column=0)
		info_lbl = Label(self, text="Datagramas corruptos:")
		info_lbl.grid(row=2, column=0)
		info_lbl = Label(self, text="Paquetes TCP recibidos:")
		info_lbl.grid(row=3, column=0)
		info_lbl = Label(self, text="Paquetes TCP corruptos:")
		info_lbl.grid(row=4, column=0)
		info_lbl = Label(self, text="Respuestas SNMP:")
		info_lbl.grid(row=5, column=0)
		#Creacion de los contenedores para los valores
		for i in range(6):
			value_lbl = Label(self, text="0")
			value_lbl.grid(row=i, column=1)
			self.values.append(value_lbl)
		#Creación de botones para eliminar y plotear
		plot_btn = Button(self, text="Grafica", command = self.plot)
		plot_btn.grid(row=6, column=0)
		del_btn = Button(self, text="X", command = self.delete_host)
		del_btn.grid(row=6, column=1)
	#Pide y actualiza constantemente la información contenida en el frame
	def update_data(self):
		host_info = agente_manager.get_agent_info(self.id)
		self.config(text = str(self.id) + ": " + host_info)
		while self.update:
			sys_time = agente_manager.get_agent_sysUpTime(self.id)
			self.values[0].config(text=sys_time)
			in_dgrams = agente_manager.get_agent_udpInDatagrams(self.id)
			self.values[1].config(text=str(in_dgrams))
			err_dgrams = agente_manager.get_agent_udpInErrors(self.id)
			self.values[2].config(text=str(err_dgrams))
			tcp_recb = agente_manager.get_agent_tcpSegmentRecibed(self.id)
			self.values[3].config(text=str(tcp_recb))
			tcp_err = agente_manager.get_agent_tcpErrorsRecibed(self.id)
			self.values[4].config(text=str(tcp_err))
			snmp_resp = agente_manager.get_agent_snmpOutGetResponses(self.id)
			self.values[5].config(text=str(snmp_resp))
	#Inicia un hilo que permite actualizar la información sin interrumpir a la aplicación
	def start_update(self):
		updater = threading.Thread(target=self.update_data)
		updater.start()
	#Permite detener la actualización de la información y que muera el hilo hijo
	def stop_update(self):
		self.update = False
	#Elimina todo rastro del host agregado previamente
	def delete_host(self):
		self.stop_update()
		agente_manager.delete_agent(self.id)
		self.pack_forget()
		self.destroy()
	def plot(self):
		plotter = PlotterWindow(self.id)
		plotter.start_draw()
#Clase de una ventana principal que implementa las clases anteriores
class GridPaneWindow(Tk):
	def __init__(self):
		Tk.__init__(self)
		self.paneRows = []
		self.infoFrames = []
		self.colCount = 0	
		self.rowCount = -1
		self.hostCount = 0
		self.initUI()		
	#Permite inicializar todos los componentes
	def initUI(self):
		menubar = Menu(self)
		start = Menu(menubar, tearoff=0)
		
		start.add_command(label="Agregar host", command=self.show_add_form)

		start.add_separator()
		start.add_command(label="Salir", command=self.quit)
		menubar.add_cascade(label="Inicio", menu=start)
			
		self.config(menu=menubar)
	#Genera y muestra un cuadro de dialogo para agregar un host
	def show_add_form(self):
		dialog = AddHostDialog(self)
	#Permite agregar un host, el método se invoca desde el diálogo
	def add_host_frame(self, host, community, port):
		if (len(self.paneRows) == 0):		
			new_row = PanedWindow(self)
			self.paneRows.append(new_row)
			self.rowCount = self.rowCount + 1
			self.add_host_frame(host, community, port)
		elif (self.colCount == 5):
			new_row = PanedWindow(self)
			self.paneRows.append(new_row)
			self.colCount = 0
			self.rowCount = self.rowCount + 1			
			self.add_host_frame(host, community, port)			
		else:
			agente_manager.add_agent(community, host, port, self.hostCount)
			infoframe = InfoFrame(self.paneRows[self.rowCount], "Info panel", self.hostCount)
			self.paneRows[self.rowCount].add(infoframe)						
			self.paneRows[self.rowCount].pack()
			infoframe.pack(side=LEFT)
			infoframe.start_update()
			self.colCount = self.colCount + 1
			self.hostCount = self.hostCount + 1
			self.infoFrames.append(infoframe)


