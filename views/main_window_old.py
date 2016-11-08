from snmp_agent_managment import agent_manager
from Tkinter import *
import threading
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

agente_manager = agent_manager.agent_manager()

class LeftFrame(Frame):
	"""docstring for ClassName"""
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent
		self.host_name_entr = None
		self.community_entr = None
		self.initUI()

	def initUI(self):
		#self.parent.title("WatchTower SNMP monitor")

		self.columnconfigure(0, pad=3)
		self.columnconfigure(1, pad=3)
		self.columnconfigure(2, pad=3)
		self.columnconfigure(3, pad=3)
		self.columnconfigure(4, pad=3)

		self.rowconfigure(0, pad=3)
		self.rowconfigure(1, pad=3)


		host_name_lbl = Label(self, text = "Host name/address")
		host_name_lbl.grid(row=0, column=0)
		self.host_name_entr = Entry(self)
		self.host_name_entr.grid(row=0, column=1)

		community_lbl = Label(self, text="Community")
		community_lbl.grid(row=0, column=2)
		self.community_entr = Entry(self)
		self.community_entr.grid(row=0, column=3)

		self.pack()

	def get_host_name(self):
		return self.host_name_entr.get()

	def get_community(self):
		return self.community_entr.get()

class RightFrame(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent
		self.initUI()
		self.row = 1
		self.agent_count = 0
		self.hosts_components = []
		self.thread_list = []


	def initUI(self):
		hosts_lbl = Label(self, text="Registered Hosts")
		hosts_lbl.grid(row=0, column=0)
		hosts_lbl = Label(self, text="Community")
		hosts_lbl.grid(row=0, column=1)
		self.pack()

	def add_host(self, host_name, community):
		host_component = []
		if len(host_name) == 0 or len(community) == 0:
			return

		agente_manager.add_agent(community, host_name, 161)

		host_lbl = Label(self, text=host_name)
		host_lbl.grid(row=self.row, column=0)
		community_lbl = Label(self, text=community)
		community_lbl.grid(row=self.row, column=1)
		#host_component.append(community_lbl)
		

		host_info_lbl = Label(self, text="Detalles: ")
		host_info_lbl.grid(row=self.row + 1, column=0)
		agent_info = agente_manager.get_agent_info(self.agent_count)
		host_info = Label(self, text=agent_info)
		host_info.grid(row=self.row + 1, column=1)
		host_component.append(host_info)

		host_cpuUsage_lbl = Label(self, text="%CPU: ")
		host_cpuUsage_lbl.grid(row=self.row + 2, column=0)
		agent_cpuUsage = agente_manager.get_agent_cpuUsage(self.agent_count)
		host_cpuUsage = Label(self, text=str(agent_cpuUsage))
		host_cpuUsage.grid(row=self.row + 2, column=1)
		host_component.append(host_cpuUsage)

		host_totalRam = Label(self, text="RAM total: ")
		host_totalRam.grid(row=self.row + 3, column=0)
		agent_totalRam = agente_manager.get_agent_totalRam(self.agent_count)
		host_totalRam_lbl = Label(self, text=str(agent_totalRam))
		host_totalRam_lbl.grid(row=self.row + 3, column=1)
		host_component.append(host_totalRam_lbl)

		host_ramUsed = Label(self, text="RAM en uso: ")
		host_ramUsed.grid(row=self.row + 4, column=0)
		agent_ramUsed = agente_manager.get_agent_ramUsed(self.agent_count)
		host_ramUsed_lbl = Label(self, text=str(agent_ramUsed))
		host_ramUsed_lbl.grid(row=self.row + 4, column=1)
		host_component.append(host_ramUsed_lbl)

		host_ramFree = Label(self, text="RAM libre: ")
		host_ramFree.grid(row=self.row + 5, column=0)
		agent_ramFree = agente_manager.get_agent_ramFree(self.agent_count)
		host_ramFree_lbl = Label(self, text=str(agent_ramFree))
		host_ramFree_lbl.grid(row=self.row + 5, column=1)
		host_component.append(host_ramFree_lbl)

		host_tcpSegmentRecibed = Label(self, text="TCP recibidos: ")
		host_tcpSegmentRecibed.grid(row=self.row + 6, column=0)
		agent_tcpSegmentRecibed = agente_manager.get_agent_tcpSegmentRecibed(self.agent_count)
		host_tcpSegmentRecibed_lbl = Label(self, text=str(agent_tcpSegmentRecibed))
		host_tcpSegmentRecibed_lbl.grid(row=self.row + 6, column=1)
		host_component.append(host_tcpSegmentRecibed_lbl)

		host_tcpErrorsRecibed = Label(self, text="TCP corruptos: ")
		host_tcpErrorsRecibed.grid(row=self.row + 7, column=0)
		agent_tcpErrorsRecibed = agente_manager.get_agent_tcpErrorsRecibed(self.agent_count)
		host_tcpErrorsRecibed_lbl = Label(self, text=str(agent_tcpErrorsRecibed))
		host_tcpErrorsRecibed_lbl.grid(row=self.row + 7, column=1)
		host_component.append(host_tcpErrorsRecibed_lbl)

		plot_button = Button(self, text="Show graphs", command=lambda:self.plot(0))
		plot_button.grid(row=self.row + 8, column=0)

		self.hosts_components.append(host_component)
		#self.rowconfigure(self.row, pad=3)
		self.row = self.row + 9
		updater = threading.Thread(target=self.update_data, args=(self.agent_count,))
		self.thread_list.append(updater)
		updater.start()
		self.agent_count = self.agent_count + 1

	def update_data(self, host_id):
		#print(host_id)
		while True:
			agent_info = agente_manager.get_agent_info(host_id)
			self.hosts_components[host_id][0].config(text=agent_info)
			agent_cpuUsage = agente_manager.get_agent_cpuUsage(host_id)
			self.hosts_components[host_id][1].config(text=str(agent_cpuUsage))
			agent_totalRam = agente_manager.get_agent_totalRam(host_id)
			self.hosts_components[host_id][2].config(text='%.3f'%(agent_totalRam) + " MB")
			agent_ramUsed = agente_manager.get_agent_ramUsed(host_id)
			self.hosts_components[host_id][3].config(text='%.3f'%(agent_ramUsed) + " MB")
			agent_ramFree = agente_manager.get_agent_ramFree(host_id)
			self.hosts_components[host_id][4].config(text='%.3f'%(agent_ramFree) + " MB")				
			agent_tcpSegmentRecibed = agente_manager.get_agent_tcpSegmentRecibed(host_id)
			self.hosts_components[host_id][5].config(text=str(agent_tcpSegmentRecibed))
			agent_tcpErrorsRecibed = agente_manager.get_agent_tcpErrorsRecibed(host_id)
			self.hosts_components[host_id][6].config(text=str(agent_tcpErrorsRecibed))

	def plot(self, host_id):
		# First set up the figure, the axis, and the plot element we want to animate
		print("ID: " + str(host_id)) 
		fig = plt.figure()
		ax = plt.axes(xlim=(0, 60.1), ylim=(-2, 100.1))
		line, = ax.plot([], [], lw=2)
		# initialization function: plot the background of each frame
		def init():
		    line.set_data([], [])
		    return line,
		# animation function.  This is called sequentially
		cpuUsage = []
		for i in range(3000):
		    cpuUsage.append(0)
		def animate(i):
		    x = np.linspace(0, 60, 3000)
		    #y = np.sin(2 * np.pi * (x - 0.01 * i))
		    cpuUsage.pop(0)
		    cpuUsage.append(agente_manager.get_agent_cpuUsage(host_id))
		    line.set_data(x, cpuUsage)
		    return line,
		# call the animator.  blit=True means only re-draw the parts that have changed.
		anim = animation.FuncAnimation(fig, animate, init_func=init,
		                               frames=200, interval=20, blit=True)
		#anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
		plt.show()



class WatchTowerWindow(Tk):
	"""docstring for ClassName"""
	def __init__(self):
		Tk.__init__(self)
		self.title("WatchTower SNMP monitor")
	
	def init(self):
		left_pane = PanedWindow(self)
		left_pane.pack(fill=BOTH, expand=1)
		right_pane = PanedWindow(self, orient=VERTICAL)
		
		left_frame = LeftFrame(left_pane)
		
		right_frame = RightFrame(right_pane)

		add_host_button = Button(left_frame, text="Add host", command=lambda:right_frame.add_host(left_frame.get_host_name(), left_frame.get_community()))
		add_host_button.grid(row=1, column=1)
		left_frame.pack()


		right_pane.add(right_frame)
		left_pane.add(right_pane)
		left_pane.add(left_frame)