#!/usr/bin/python


class RaceNotStarted(Exception):
	pass


class Race(object):
	
	def __init__(self, lanes):
		"""
		A race model. Takes a list of lane lengths.
		"""
		
		self.reset(lanes)
	
	
	def reset(self, lanes):
		self.lanes = map(float, lanes)
		self.laps = [[] for _ in range(len(lanes))]
	
	
	def add_lap(self, lane, time):
		if time == 0.0:
			self.laps[lane] = []
		else:
			self.laps[lane].append(time)
	
	
	@property
	def num_laps(self):
		return map(len, self.laps)
	
	
	@property
	def total_time(self):
		return map(sum, self.laps)
	
	
	@property
	def avg_time(self):
		return map((lambda (t,n): t/n if n != 0 else 0), zip(self.total_time, self.num_laps))
	
	
	@property
	def best_time(self):
		return map((lambda l: min(l) if l else 0), self.laps)
	
	
	@property
	def speeds(self):
		return map((lambda (ts,d): map((lambda t: d/t), ts)), zip(self.laps, self.lanes))
	
	
	@property
	def max_speed(self):
		return map((lambda l: max(l) if l else 0.0) , self.speeds)
	
	
	@property
	def avg_speed(self):
		return map((lambda (s,l): s/l if l != 0 else 0.0), zip(map(sum, self.speeds), self.num_laps))


if __name__=="__main__":
	
	import hardware
	h = hardware.Hardware("/dev/ttyUSB0")
	r = Race([1.0,1.0])
	try:
		while True:
			evt = h.get_event()
			if evt:
				r.add_lap(*evt)
				
				print "r.num_laps  ", r.num_laps
				print "r.total_time", r.total_time
				print "r.avg_time  ", r.avg_time
				print "r.max_speed ", r.max_speed
				print "r.avg_speed ", r.avg_speed
				print
	
	finally:
		h.close()

