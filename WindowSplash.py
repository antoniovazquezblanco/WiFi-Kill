#!/usr/bin/python2
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from utils.SystemChecks import SystemChecks
import threading
import os
import signal


class WindowSplash(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="WiFi Kill")
		self.set_decorated(False)
		self.set_position(Gtk.WindowPosition.CENTER)
		# TODO: Add an image to the splash screen...
		self.show_all()
		t = threading.Thread(target=self.__initialize)
		t.start()
		Gtk.main()
		t.join()
		self.destroy()

	def __initialize(self):
		try:
			SystemChecks.post_test()
		except Exception as e:
			print("[!] Error: " + str(e))
			# TODO: Interrupt in a clean way!
			os.kill(os.getpid(), signal.SIGKILL)
		Gtk.main_quit()

	# TODO: Show a dialog on error and lock thread until a button is pressed and then exit the program
	#class ErrorDialog(Gtk.MessageDialog):
	#	def __init__(self, msg):
	#		Gtk.MessageDialog.__init__(self, type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK)
	#		self.set_markup(msg)
	#		self.run()
