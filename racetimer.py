#!/usr/bin/python

from race     import Race
from hardware import Hardware

import wx
from ui import RaceTimerFrame


import threading


class RaceThread(Race, threading.Thread):
	
	def __init__(self, hardware, *args, **kwargs):
		self.lock = threading.Lock()
		self.on_update = None
		self.hardware = hardware
		
		Race.__init__(self, [1,1])
		threading.Thread.__init__(self)
		
		self.start()
	
	
	def reset(self, lanes):
		Race.reset(self, lanes)
		self.hardware.reset()
	
	
	def run(self):
		while True:
			event = self.hardware.get_event()
			with self.lock:
				self.add_lap(*event)
			
			if self.on_update:
				self.on_update()



class RaceTimer(RaceTimerFrame):
	
	def __init__(self, app, race, *args, **kwargs):
		RaceTimerFrame.__init__(self, *args, **kwargs)
		
		self.app = app
		self.race = race
		
		self.RACE_CHANGE = wx.NewEventType()
		self.EVT_RACE_CHANGE = wx.PyEventBinder(self.RACE_CHANGE, 0)
		self.Bind(self.EVT_RACE_CHANGE, self.on_race_change)
		
		def fire_race_change():
			evt = wx.CommandEvent(self.RACE_CHANGE)
			wx.PostEvent(self, evt)
		
		self.race.on_update = fire_race_change
		
		self.p1_lap_list.InsertColumn(0, "Lap", width=-1)
		self.p1_lap_list.InsertColumn(1, "Time", width=-1)
		self.p1_lap_list.InsertColumn(2, "Duration", width=-1)
		
		self.p2_lap_list.InsertColumn(0, "Lap", width=-1)
		self.p2_lap_list.InsertColumn(1, "Time", width=-1)
		self.p2_lap_list.InsertColumn(2, "Duration", width=-1)
		
		self.on_reset_btn_clicked(None)
	
	
	def on_quit_btn_clicked(self, event):
		self.app.Exit()
	
	
	def on_reset_btn_clicked(self, event):
		with self.race.lock:
			self.race.reset([1,1])
			self.last_num_laps = self.race.num_laps
		
		self.p1_lap_list.DeleteAllItems()
		self.p2_lap_list.DeleteAllItems()
		self.on_race_change(None)
	
	
	def on_race_change(self, event):
		with self.race.lock:
			p1, p2 = self.race.num_laps
			self.p1_laps.SetLabel("%d"%p1)
			self.p2_laps.SetLabel("%d"%p2)
			
			p1, p2 = self.race.avg_time
			self.p1_avg_time.SetLabel("%0.2f sec"%p1)
			self.p2_avg_time.SetLabel("%0.2f sec"%p2)
			
			p1, p2 = self.race.best_time
			self.p1_best_time.SetLabel("%0.2f sec"%p1)
			self.p2_best_time.SetLabel("%0.2f sec"%p2)
			
			for num, (old,new) in enumerate(zip(self.last_num_laps, self.race.num_laps)):
				if old != new:
					lap_list = [self.p1_lap_list, self.p2_lap_list][num]
					pos = lap_list.InsertStringItem(0, "%d"%new)
					lap_list.SetStringItem(pos,     1, "%0.2f"%(sum(self.race.laps[num])))
					lap_list.SetStringItem(pos,     2, "%0.2f"%(self.race.laps[num][-1]))
			self.last_num_laps = self.race.num_laps



if __name__=="__main__":
	hardware = Hardware("/dev/ttyUSB0")
	race = RaceThread(hardware, [1,1])
	
	try:
		app = wx.PySimpleApp(0)
		wx.InitAllImageHandlers()
		rt = RaceTimer(app, race, None, -1, "")
		app.SetTopWindow(rt)
		rt.Show()
		app.MainLoop()
	finally:
		hardware.close()

