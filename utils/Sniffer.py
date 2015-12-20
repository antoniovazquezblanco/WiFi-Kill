#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
from scapy.all import *
from scapy.layers.dot11 import Dot11


class Sniffer():
	def __init__(self):
		self.list_ap = []
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

	def __sniff(self):
		sniff(prn=self.__callback_packet, stop_filter=self.__callback_stop)

	def __callback_packet(self, pkt):
		if pkt.haslayer(Dot11):
			if pkt.type == 0 and pkt.subtype == 8:
				# if pkt.addr2 not in ap_list :
					# ap_list.append(pkt.addr2)
				print("[D] AP MAC: %s SSID: %s " % (pkt.addr2, pkt.info))
		print("[!] Sniffer.__callback_packet(): TODO: Implement!")

	def __callback_stop(self, param):
		print("[D] Sniffer: "+str(self.__active))
		return not self.__active

