#!/usr/bin/python

from serial import Serial

class Hardware(object):
	
	def __init__(self, port = None, timeout = 0.1):
		self.con = Serial(port, 9600, timeout = timeout)
		
		self.buf = ""
		
		self.reset()
	
	def reset(self):
		self.last_lane_time = {}
	
	
	def get_event(self):
		"""
		Get next lap event.
		
		Returns (lane, laptime) with laptime in sec and 0 at start of first lap
		"""
		
		val = self.con.read(1)
		if val:
			self.buf += val
		
		if val != "\n":
			return None
		
		lane, time = map(int, self.buf.strip().split(" "))
		self.buf = ""
		
		last_time = self.last_lane_time.setdefault(lane, time)
		self.last_lane_time[lane] = time
		
		
		return lane, (time - last_time) / 1000.0
	
	
	def close(self):
		self.con.close()


if __name__=="__main__":
	h = Hardware("/dev/ttyUSB0")
	try:
		while True:
			evt = h.get_event()
			if evt:
				print evt
		
	finally:
		h.close()
