#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from subprocess import Popen, PIPE
from scapy.all import *
from subprocess import call


DEVNULL = open(os.devnull, 'w')


class WirelessInterface:
	def __init__(self):
		self.name = '<unknown>'
		self.mac = '<unknown>'
		self.mode = '<unknown>'

	def set_name(self, name):
		self.name = name

	def set_mac(self, mac):
		self.mac = mac

	def set_mode(self, mode):
		self.mode = mode

	def get_as_tuple(self):
		return self.name, self.mac, self.mode

	def randomize_mac(self):
		random.seed()
		new_mac = self.mac[:8]
		for i in xrange(0, 6):
			if i % 2 == 0:
				new_mac += ':'
			new_mac += '0123456789ABCDEF'[random.randint(0, 15)]
		call(['ifconfig', self.name, 'down'])
		call(['ifconfig', self.name, 'hw', 'ether', new_mac])
		call(['ifconfig', self.name, 'up'])

	def change_mode(self, mode):
		call(['ifconfig', self.name, 'down'])
		call(['iwconfig', self.name, 'mode', mode])
		call(['ifconfig', self.name, 'up'])

	@staticmethod
	def get_from_name(name):
		interface = WirelessInterface()
		interface.set_name(name)
		# Get the mac address...
		mac = ''
		process = Popen(['ifconfig', name], stdout=PIPE, stderr=DEVNULL)
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
		elif output.find('ether') != -1:	# New ifconfig...
			for line in output.split('\n'):
				if line.find('ether') != -1:
					for word in line.split(' '):
						if word != '' and word.find(':') != -1:
							mac = word.upper()
							break
		else:					# New ifconfig in monitor mode...
			for line in output.split('\n'):
				if line.find('unspec') != -1:
					for word in line.split(' '):
						if word != '' and word.find('-') != -1:
							mac = word.replace('-', ':').upper()[0:17]
							break
		interface.set_mac(mac)
		# Get interface mode...
		process = Popen(['iwconfig', name], stdout=PIPE, stderr=DEVNULL)
		process.wait()
		if process.communicate()[0].find('Mode:Monitor') != -1:
			interface.set_mode('Monitor')
		else:
			interface.set_mode('Managed')
		return interface

	@staticmethod
	def get_interfaces():
		# Find the interface list....
		process = Popen(['iwconfig'], stdout=PIPE, stderr=DEVNULL)
		process.wait()
		interfaces = []
		for line in process.communicate()[0].split('\n'):
			if len(line) == 0:
				continue
			if ord(line[0]) != 32:									# Doesn't start with space
				interfaces.append(WirelessInterface.get_from_name(line[:line.find(' ')]))	# Is the interface
		return interfaces

