class agent:
	def __init__(self, community, name, port):
		self.community = community
		self.name = name
		self.port = port
		self.so_developper = ""
		self.so = ""
		self.sys_name = ""
		self.so_date_time = ""
		self.so_arch = ""


	def set_description(self, descr_str):
		values = descr_str.split()
		self.so_developper = values[0]
		self.so = values[3]
		self.sys_name = values[1]
		self.so_date_time = values[5] +" "+ values[6] +" "+ values[7] +" "+ values[8] +" "+ values[9] +" "+ values[10]
		self.so_arch = values[11]

	def descr_to_str(self):
		return self.so_developper + " " + self.so + " " + self.sys_name + " " + self.so_date_time + " " + self.so_arch
