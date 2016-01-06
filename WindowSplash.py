#!/usr/bin/python2
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from utils.SystemChecks import SystemChecks
import threading
import os
import signal
from Queue import Queue
import sys
import time
import traceback


class WindowSplash(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="WiFi Kill")
		self.set_decorated(False)
		self.set_position(Gtk.WindowPosition.CENTER)
		self.set_default_size(640, 500)#Esto creo que no es necesario
		# TODO: Add an image to the splash screen...
		logo = Gtk.Image.new_from_file('resources/logo.png')
		self.add(logo)
		self.show_all()
		q = Queue()
		t = threading.Thread(target=self.__initialize, args=(q,))
		t.start()
		Gtk.main()
		t.join()
		if not q.empty():
			e, tb = q.get()
			d = WindowSplash.ErrorDialog(self, e, tb)
			d.run()
			d.destroy()
			print(tb)
			raise e
		self.destroy()

	def __initialize(self, q):
		time.sleep(0.1)
		try:
			SystemChecks.post_test()
		except Exception as e:
			q.put((e, traceback.format_exc()))
		Gtk.main_quit()

	class ErrorDialog(Gtk.Dialog):
		def __init__(self, parent, error, traceback):
			Gtk.Dialog.__init__(self, "Error", parent, 0, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
			self.set_default_size(150, 100)
			box = self.get_content_area()
			label = Gtk.Label(str(error))
			box.add(label)
			expander = Gtk.Expander()
			expander.set_label("Traceback")
			label_tb = Gtk.Label(str(traceback))
			expander.add(label_tb)
			box.add(expander)
			self.show_all()

