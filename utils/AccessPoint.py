#!/usr/bin/python
# -*- coding: utf-8 -*-


class AccessPoint:
	def __init__(self, bssid):
		self.bssid = bssid
		self.essid = '<unknown>'
		self.power = 0
		self.packets = 0
		self.channel = 0

	def set_ssid(self, ssid):
		self.essid = ssid

	def set_channel(self, channel):
		print("CH:"+str(channel))
		self.channel = channel

	def incr_pkts(self, incr=1):
		self.packets = self.packets + 1

	def get_as_tuple(self):
		return self.bssid, self.essid, self.channel, self.packets, self.power
