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


class WindowSplash(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="WiFi Kill")
		self.set_decorated(False)
		self.set_position(Gtk.WindowPosition.CENTER)
		# TODO: Add an image to the splash screen...
		self.show_all()
		q = Queue()
		t = threading.Thread(target=self.__initialize, args=(q,))
		t.start()
		Gtk.main()
		t.join()
		if not q.empty():
			t = q.get()
			d = WindowSplash.ErrorDialog(self, t)
			d.run()
			d.destroy()
			raise Exception(t)
		self.destroy()

	def __initialize(self, q):
		time.sleep(0.1)
		try:
			SystemChecks.post_test()
		except Exception as e:
			q.put(str(e))
		Gtk.main_quit()

	class ErrorDialog(Gtk.Dialog):
		def __init__(self, parent, error):
			Gtk.Dialog.__init__(self, "Error", parent, 0, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
			self.set_default_size(150, 100)
			label = Gtk.Label(str(error))
			box = self.get_content_area()
			box.add(label)
			self.show_all()

