from snmp_admin import snmp_admin_thread
from snmp_admin import agent

class agent_manager:
	def __init__(self):
		self.agent_list = {}

	def add_agent(self, community, host_name, port, agent_id):
		agente = agent.agent(community, host_name, port)
		agente_trhead = snmp_admin_thread.admin_thread(agente)
		self.agent_list[agent_id] = agente_trhead
		agente_trhead.start()

	def get_agent_sysUpTime(self, agent_id):
		if(self.agent_list.has_key(agent_id)):
			return self.agent_list[agent_id].sysUpTime

	def get_agent_udpInDatagrams(self, agent_id):
		if(self.agent_list.has_key(agent_id)):
			return self.agent_list[agent_id].udpInDatagrams

	def get_agent_udpInErrors(self, agent_id):
		if(self.agent_list.has_key(agent_id)):
			return self.agent_list[agent_id].udpInErrors

	def get_agent_udpOutDatagrams(self, agent_id):
		if(self.agent_list.has_key(agent_id)):
			return self.agent_list[agent_id].udpOutDatagrams

	def get_agent_tcpErrorsRecibed(self, agent_id):
		#print("Agent: " + str(agent_id))
		if(self.agent_list.has_key(agent_id)):
			return self.agent_list[agent_id].tcpErrorsRecibed

	def get_agent_tcpSegmentRecibed(self, agent_id):
		#print("Agent: " + str(agent_id))
		if(self.agent_list.has_key(agent_id)):
			return self.agent_list[agent_id].tcpSegmentRecibed

	def get_agent_tcpOutSegs(self, agent_id):
		#print("Agent: " + str(agent_id))
		if(self.agent_list.has_key(agent_id)):
			return self.agent_list[agent_id].tcpOutSegs

	def get_agent_snmpOutGetResponses(self, agent_id):
		if(self.agent_list.has_key(agent_id)):
			return self.agent_list[agent_id].snmpOutGetResponses

	def get_agent_info(self, agent_id):
		if(self.agent_list.has_key(agent_id)):
			return self.agent_list[agent_id].agente.descr_to_str()

	def delete_agent(self, agent_id):
		if(self.agent_list.has_key(agent_id)):
			self.agent_list[agent_id].stop()
			del self.agent_list[agent_id]