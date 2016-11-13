from threading import Thread
import time
import snmp_admin
from config import constants

class admin_thread(Thread):
	
	def __init__(self, agente):
		Thread.__init__(self)
		self.agent_admin = snmp_admin.snmp_admin(agente)
		self.agente = agente
		self.sysUpTime = ""
		self.udpInDatagrams = 0
		self.udpInErrors = 0
		self.udpOutDatagrams = 0
		self.tcpErrorsRecibed = 0
		self.tcpSegmentRecibed = 0
		self.tcpOutSegs = 0
		self.snmpOutGetResponses = 0
		self.live = True

	def run(self):
		self.get_system_description()
		while self.live:					
			data = self.agent_admin.snmpget(constants.mibObjects)
			rawsysUpTime = int(data[0])
			secs, hundsecs = divmod(rawsysUpTime, 100)
			mins, secs = divmod(secs, 60)
			hrs, mins = divmod(mins, 60)
			self.sysUpTime = "%d:%02d:%02d" % (hrs, mins, secs)
			self.udpInDatagrams = int(data[1])
			self.udpInErrors = int(data[2])
			self.udpOutDatagrams = int(data[3])
			self.tcpErrorsRecibed = int(data[4])
			self.tcpSegmentRecibed = int(data[5])
			self.tcpOutSegs = int(data[6])
			self.snmpOutGetResponses = int(data[7])
			time.sleep(.02)

	def get_system_description(self):
		sys_descr = self.agent_admin.snmpget(constants.sysDscr)
		self.agente.set_description(str(sys_descr[0]))

	def stop(self):
		self.live = False		
