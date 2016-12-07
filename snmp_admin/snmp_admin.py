from pysnmp.entity.rfc3413.oneliner import cmdgen
from agent import agent

class snmp_admin:
	def __init__(self, agente):
		self.comandGen = cmdgen.CommandGenerator()
		self.agente = agente

	def snmpget(self, mib_objects):
		values = []
		errorIndication, errorStatus, errorIndex, varBinds = self.comandGen.getCmd(
			cmdgen.CommunityData(self.agente.community),
			cmdgen.UdpTransportTarget((self.agente.name, self.agente.port)),
			*mib_objects
		)
		if errorIndication:
		    print(errorIndication)
		else:
		    if errorStatus:
		        print('%s at %s' % (
		            errorStatus.prettyPrint(),
		            errorIndex and varBinds[int(errorIndex)-1] or '?'
		            )
		        )
		    else:
		        for name, val in varBinds:
		        	values.append(val)
		return values
		