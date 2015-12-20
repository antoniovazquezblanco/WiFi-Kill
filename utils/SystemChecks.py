#!/usr/bin/python2
# -*- coding: utf-8 -*-
import os
class SystemChecks:
	@staticmethod
	def pre_test():
		print("[D] SystemChecks.pre_test(): TODO: Implement!")
		# TODO: Chek if GTK is installed...

	@staticmethod
	def post_test():
		SystemChecks.__check_root()
		SystemChecks.__check_modules()
		SystemChecks.__check_binaries()
		

	@staticmethod
	def __check_root():		
		if os.geteuid() != 0:
			raise Exception("[E] SystemChecks.__check_root(): No root access")

	@staticmethod
	def __check_modules():
		# TODO: Is scapy installed?
		print("[D] SystemChecks.__check_modules(): TODO: Implement!")

	@staticmethod
	def __check_binaries():
		print("[D] SystemChecks.__check_binaries(): TODO: Implement!")
		# TODO: Is ifconfig present?
		# TODO: Is iwconfig present? -> sudo apt-get install wireless-tools
		# TODO: WTF? iwconfig and ifconfig in debian is in /sbin/ and not in path...
