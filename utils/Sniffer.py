#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
from utils.WirelessInterface import WirelessInterface
from utils.AccessPoint import AccessPoint
from scapy.all import *
from scapy.layers.dot11 import Dot11


class Dot11Fields():

	class Type():
		Management = 0x00

	class SubType():
		Beacon = 0x08

	class Elt():
		SSID = 0x00
		DSset = 0x03


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
		if pkt.haslayer(Dot11) and pkt.type == Dot11Fields.Type.Management and pkt.subtype == Dot11Fields.SubType.Beacon:
			# TODO: Why addr2 instead of addr3????
			if not pkt.addr2 in self.list_ap:
				self.list_ap[pkt.addr2] = AccessPoint(pkt.addr2)
			for p in pkt.getlayer(Dot11Elt):
				if p.ID == Dot11Fields.Elt.SSID:
					self.list_ap[pkt.addr2].set_ssid(p.info)
				elif p.ID == Dot11Fields.Elt.DSset:
					self.list_ap[pkt.addr2].set_channel(ord(p.info))
				'''
				    crypto = set()
				    while isinstance(p, Dot11Elt):
				        elif p.ID == 48:
				            crypto.add("WPA2")
				        elif p.ID == 221 and p.info.startswith('\x00P\xf2\x01\x01\x00'):
				            crypto.add("WPA")
				        p = p.payload
				    if not crypto:
				        if 'privacy' in cap:
				            crypto.add("WEP")
				        else:
				            crypto.add("OPN")
				'''
			self.list_ap[pkt.addr2].incr_pkts()
			pkt.show()
			print("------------------------------------------------")

	def __callback_stop(self, param):
		return not self.__active

