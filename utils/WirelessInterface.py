#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from subprocess import Popen, PIPE
from scapy.all import *
from subprocess import call


DEVNULL = open(os.devnull, 'w')


class WirelessInterface:
	def __init__(self, name):
		self.name = name
		self.mac = '<unknown>'
		self.mode = '<unknown>'

	def set_mac(self, mac):
		self.mac = mac

	def set_mode(self, mode):
		self.mode = mode

	def get_as_tuple(self):
		return self.name, self.mac, self.mode

	def mac_randomize(self):
		random.seed()
		new_mac = self.mac
		while new_mac == self.mac:
			new_mac = ''
			for i in range(0, 12):
				if i % 2 == 0 and i != 0:
					new_mac += ':'
				new_mac += '0123456789ABCDEF'[random.randint(0, 15)]
		call(['ifconfig', self.name, 'down'])
		call(['ifconfig', self.name, 'hw', 'ether', new_mac])
		call(['ifconfig', self.name, 'up'])
		print("[!] WirelessInterface.mac_randomize(): TODO: Implement checking!")

	@staticmethod
	def get_interfaces():
		# Find the interface list....
		process = Popen(['iwconfig'], stdout=PIPE, stderr=DEVNULL)
		process.wait()
		interfaces = []
		for line in process.communicate()[0].split('\n'):
			if len(line) == 0:
				continue
			if ord(line[0]) != 32:				# Doesn't start with space
				interfaces.append(WirelessInterface(line[:line.find(' ')]))	# Is the interface
		# Get the mac address of every device...
		for i in interfaces:
			mac = ''
			process = Popen(['ifconfig', i.name], stdout=PIPE, stderr=DEVNULL)
			process.wait()
			output = process.communicate()[0]
			if output.find('HWaddr') != -1:		# Old ifconfig...
				line = output.split('\n')[0]
				for word in line.split(' '):
					if word != '':
						mac = word
					if mac.find('-') != -1:
						mac = mac.replace('-', ':')
					if len(mac) > 17:
						mac = mac[0:17]
			else:					# New ifconfig...
				line = output.split('\n')[3]
				for word in line.split(' '):
					if word != '' and word.find(':') != -1:
						mac = word.upper()
						break
			i.set_mac(mac)
		# Get interface mode...
		for i in interfaces:
			process = Popen(['iwconfig', i.name], stdout=PIPE, stderr=DEVNULL)
			process.wait()
			if process.communicate()[0].find('Mode:Monitor') != -1:
				i.set_mode('Monitor')
			else:
				i.set_mode('Managed')
		return interfaces

