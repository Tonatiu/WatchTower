#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rrdtool
import os.path
from config import constants

class rrd_db:
	def __init__(self):
		self.rrd_path = "../WatchTower/rrdutils/rrdDataBase/"
		self.rrd_image_path = "../WatchTower/rrdutils/rrdImages/"
		self.name = "";
	def create(self, dbname):
		if not os.path.isfile(self.rrd_path + dbname + ".rrd"):
			self.name = dbname
			error_status = rrdtool.create(
				self.rrd_path + dbname + ".rrd",
				"--start", "now", 
				"--step", str(constants.sleeptime),
				"DS:cpu1Usage:DERIVE:4:0:90",
				"DS:cpu2Usage:DERIVE:4:0:90",
				"DS:ramUsage:DERIVE:4:0:4000000",
				"DS:HDUsage:DERIVE:4:0:20000000",
				"RRA:AVERAGE:0.5:1:30", #minuto = 2*30*1
				"RRA:AVERAGE:0.5:30:60", #Hora = 2*30*60
				"RRA:AVERAGE:0.5:1800:24", #Día = 2*1800*24
				"RRA:AVERAGE:0.5:43200:7" #Semana = 2*43200*7
			)
			if error_status:
				print rrdtool.error()
				return -1
		else:
			print("Database " + dbname + " already exists")
			return -2
		return 0


	def update(self, dbname, values):
		if os.path.isfile(self.rrd_path + dbname + ".rrd"):
			error_status = rrdtool.update(self.rrd_path + dbname + ".rrd", values)
			if error_status:
				print rrdtool.error()
		else:
			print "Not database found"

	def plotGraph(self, dbname):
		image_name = dbname + "_graph.png"
		error_status = rrdtool.graph(
			self.rrd_image_path + image_name, "--start", "-1d", "--vertical-label=Usage",
			"DEF:cpu1=" + self.rrd_path + dbname + ".rrd:cpu1Usage:AVERAGE",
			"DEF:cpu2=" + self.rrd_path + dbname + ".rrd:cpu2Usage:AVERAGE",
			"DEF:RAM=" + self.rrd_path + dbname + ".rrd:ramUsage:AVERAGE",
			"DEF:HDD=" + self.rrd_path + dbname + ".rrd:HDUsage:AVERAGE",
			"LINE1:cpu1#00868B:CPU_1 Load",
			"LINE1:cpu2#00C5CD:CPU_2 Load",
			"LINE1:RAM#BCEE68:RAM Usage",
			"LINE1:HDD#9ACD32:HDD Usage"
			#"GPRINT:cpu1:LAST:CPU_1 last usage: %6.0lf"
			#"GPRINT:cpu2:LAST:CPU_2 last usage: %6.0lf"
			)
		if error_status:
			rrdtool.error()

"""manager = rrd_db()
manager.create("test_db")
manager.update("test_db", 'N:%s:%s:%s:%s'%(10,10,100,100))
manager.plotGraph("test_db")"""