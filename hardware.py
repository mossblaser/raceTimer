#!/usr/bin/python

from serial import Serial

class Hardware(object):
	
	def __init__(self, port = None):
		self.con = Serial(port, 9600)
		
		self.reset()
	
	
	def reset(self):
		self.last_lane_time = {}
	
	
	def get_event(self):
		"""
		Get next lap event.
		
		Returns (lane, laptime) with laptime in sec and 0 at start of first lap
		"""
		
		lane, time = map(int, self.con.readline().strip().split(" "))
		#self.last_lane_time[
		
		last_time = self.last_lane_time.setdefault(lane, time)
		self.last_lane_time[lane] = time
		
		return lane, (time - last_time) / 1000.0
	
	
	def close(self):
		self.con.close()


if __name__=="__main__":
	h = Hardware("/dev/ttyUSB0")
	try:
		while True:
			print h.get_event()
		
	finally:
		h.close()
