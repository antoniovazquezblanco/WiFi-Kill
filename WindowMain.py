#!/usr/bin/python2
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from utils.WirelessInterface import WirelessInterface
from utils.Sniffer import Sniffer


class WindowMain:
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("WindowMain.glade")
		self.builder.connect_signals(self)
		self.window = self.builder.get_object("window_main")
		self.log_text = self.builder.get_object("window_main_notebook_log_text")
		self.log_text_buff = self.log_text.get_buffer()
		self.interface_treeview = self.builder.get_object("window_main_notebook_interfaces_treeview")
		self.interface_liststore = self.builder.get_object("window_main_liststore_interfaces")
		self.sniffer_thread = Sniffer()
		self.__loop()

	def __loop(self):
		self.window.show_all()
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
		self.log_append("[+] Randomizing MAC address...\n")
		# Get the selected rows
		model, paths = self.interface_treeview.get_selection().get_selected_rows()
		for path in paths:
			WirelessInterface.get_from_name(model.get(model.get_iter(path), 0)[0]).randomize_mac()
		self.window_main_toolbar_interfaces_update_clicked(button)
		print("[D] WindowMain.window_main_notebook_interfaces_randomize_mac_clicked(): TODO: Show dialog if no interface is selected...")

	def window_main_notebook_interfaces_monitor_start_clicked(self, button):
		self.log_append("[+] Putting interfaces in monitor mode...\n")
		# Get the selected rows
		model, paths = self.interface_treeview.get_selection().get_selected_rows()
		for path in paths:
			WirelessInterface.get_from_name(model.get(model.get_iter(path), 0)[0]).change_mode("Monitor")
		self.window_main_toolbar_interfaces_update_clicked(button)
		print("[D] WindowMain.window_main_notebook_interfaces_monitor_start_clicked(): TODO: Show dialog if no interface is selected...")

	def window_main_notebook_interfaces_monitor_stop_clicked(self, button):
		self.log_append("[+] Putting interfaces in managed mode...\n")
		# Get the selected rows
		model, paths = self.interface_treeview.get_selection().get_selected_rows()
		for path in paths:
			WirelessInterface.get_from_name(model.get(model.get_iter(path), 0)[0]).change_mode("Monitor")
		self.window_main_toolbar_interfaces_update_clicked(button)
		print("[D] WindowMain.window_main_notebook_interfaces_monitor_stop_clicked(): TODO: Show dialog if no interface is selected...")

