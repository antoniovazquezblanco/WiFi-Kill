#!/usr/bin/python2
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from utils import WirelessInterface
from utils import Sniffer


class WiFiKill:
	def __init__(self):
		self.window_splash = self.SplashScreen()
		# Heavy initialization code ahead...
		import time
		time.sleep(5)
		self.builder = Gtk.Builder()
		self.builder.add_from_file("WiFiKill.glade")
		self.builder.connect_signals(self)
		self.window = self.builder.get_object("window_main")
		self.log_text = self.builder.get_object("window_main_notebook_log_text")
		self.log_text_buff = self.log_text.get_buffer()
		self.interface_treeview = self.builder.get_object("window_main_notebook_interfaces_treeview")
		self.interface_liststore = self.builder.get_object("window_main_liststore_interfaces")
		self.sniffer_thread = Sniffer()

	def loop(self):
		self.window.show_all()
		self.window_splash.destroy()
		Gtk.main()

	def interfaces_clear(self):
		self.interface_liststore.clear()

	def interface_append(self, interface):
		self.interface_liststore.append(interface)

	def log_append(self, text):
		end_iter = self.log_text_buff.get_end_iter()
		self.log_text_buff.insert(end_iter, text)

	def on_destroy(self, *args):
		self.log_append("[+] Stopping sniffer...\n")
		self.sniffer_thread.stop()
		Gtk.main_quit(*args)

	def window_main_toolbar_interfaces_update_clicked(self, button):
		self.log_append("[+] Updating interfaces...\n")
		interfaces = WirelessInterface.get_interfaces()
		self.interfaces_clear()
		for i in interfaces:
			self.interface_append(i.get_as_tuple())

	def window_main_toolbar_scan_clicked(self, button):
		self.log_append("[+] Starting sniffer...\n")
		self.sniffer_thread.start()

	def window_main_notebook_interfaces_randomize_mac_clicked(self, button):
		self.log_append("[+] TODO: Implement MAC randomization...\n")
		# Get the selected rows
		model, paths = self.interface_treeview.get_selection().get_selected_rows()
		for path in paths:
			WirelessInterface.get_from_name(model.get(model.get_iter(path), 0)[0]).mac_randomize()
		self.window_main_toolbar_interfaces_update_clicked(button)
		print("[!] TODO: Show dialog if no interface is selected...")

	def window_main_notebook_interfaces_monitor_start_clicked(self, button):
		print("[!] TODO: Implement monitor start...\n")

	def window_main_notebook_interfaces_monitor_stop_clicked(self, button):
		print("[+] TODO: Implement monitor stop...\n")

	class SplashScreen:
		def __init__(self):
			# Create an undecorated window...
			self.window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
			self.window.set_title('WiFi Kill')
			self.window.set_position(Gtk.WindowPosition.CENTER)
			self.window.set_decorated(False)
			self.window.add(Gtk.Image.new_from_file('resources/splash.png'))
			# Transparent background...
			self.window.set_app_paintable(True)
			screen = self.window.get_screen()
			visual = screen.get_rgba_visual()
			if visual != None and screen.is_composited():
				self.window.set_visual(visual)
			# Show the window and render it...
			# TODO: It seems like the window gets created but it doesn't render until y click on it and call main_iteration after it... It needs fixing...
			self.window.show_all()
			while Gtk.events_pending():
				Gtk.main_iteration()
			self.window.present()
			self.window.grab_focus()
			self.window.set_keep_above(True)
			self.window.set_accept_focus(True)
			self.window.present()
			while Gtk.events_pending():
				Gtk.main_iteration()
			#import time
			#time.sleep(19)
			while Gtk.events_pending():
				Gtk.main_iteration()

		def destroy(self):
			self.window.destroy()


if __name__ == "__main__":
	win = WiFiKill()
	win.loop()
