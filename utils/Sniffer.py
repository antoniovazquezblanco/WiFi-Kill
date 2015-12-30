#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
from utils.WirelessInterface import WirelessInterface
from utils.AccessPoint import AccessPoint
from scapy.all import *
from scapy.layers.dot11 import Dot11


class Sniffer():
	def __init__(self):
		self.list_ap = {}
		self.__active = False
		self.__thread = None

	def start(self):
		if self.__thread is None or not self.__thread.is_alive():
			print("[D] Sniffer start...")
			self.__active = True
			self.__thread = threading.Thread(target=self.__sniff)
			self.__thread.start()
			return True
		return False

	def stop(self):
		if self.__active and self.__thread is not None and self.__thread.is_alive():
			self.__active = False
			print("[D] Sniffer stop...")
			self.__thread.join()
			return True
		return False

	def get_networks(self):
		return self.list_ap.values()

	def __sniff(self):
		interfaces = WirelessInterface.get_interfaces()
		mon = False
		for i in interfaces:
			if i.get_mode() == "Monitor":
				mon = True
		if not mon:
			print("[!] Sniffer.__sniff(): No monitor interfaces, show dialog...")
			return
		sniff(prn=self.__callback_packet, stop_filter=self.__callback_stop)

	def __callback_packet(self, pkt):
		if pkt.haslayer(Dot11):
			if pkt.type == 0 and pkt.subtype == 8:
				if not pkt.addr2 in self.list_ap:
					self.list_ap[pkt.addr2] = AccessPoint(pkt.addr2)
				self.list_ap[pkt.addr2].set_ssid(pkt.info)
				self.list_ap[pkt.addr2].incr_pkts()
				print("[D] Pkt: "+pkt.summary())

	def __callback_stop(self, param):
		return not self.__active

