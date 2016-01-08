#!/usr/bin/python2
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from utils.WirelessInterface import WirelessInterface


class DialogInterfaces:
	def __init__(self):
		builder = Gtk.Builder()
		builder.add_from_file("DialogInterfaces.glade")
		builder.connect_signals(self)
		self.liststore = builder.get_object("dialog_interfaces_liststore")
		self.treeview = builder.get_object("dialog_interfaces_treeview")
		self.dialog = builder.get_object("dialog_interfaces")
		self.interfaces_update()
		self.dialog.run()
		self.dialog.destroy()

	def dialog_interfaces_button_ok_clicked(self, button):
		self.dialog.destroy()

	def dialog_interfaces_button_monitorstop_clicked(self, button):
		# Get the selected rows
		model, paths = self.treeview.get_selection().get_selected_rows()
		for path in paths:
			WirelessInterface.get_from_name(model.get(model.get_iter(path), 0)[0]).change_mode("Managed")
		self.interfaces_update()
		print("[D] DialogInterfaces.dialog_interfaces_button_monitorstop_clicked(): TODO: Show dialog if no interface is selected...")

	def dialog_interfaces_button_monitorstart_clicked(self, button):
		# Get the selected rows
		model, paths = self.treeview.get_selection().get_selected_rows()
		for path in paths:
			WirelessInterface.get_from_name(model.get(model.get_iter(path), 0)[0]).change_mode("Monitor")
		self.interfaces_update()
		print("[D] DialogInterfaces.dialog_interfaces_button_monitorstart_clicked(): TODO: Show dialog if no interface is selected...")

	def dialog_interfaces_button_macrand_clicked(self, button):
		# Get the selected rows
		model, paths = self.treeview.get_selection().get_selected_rows()
		for path in paths:
			WirelessInterface.get_from_name(model.get(model.get_iter(path), 0)[0]).randomize_mac()
		self.interfaces_update()
		print("[D] DialogInterfaces.dialog_interfaces_button_macrand_clicked(): TODO: Show dialog if no interface is selected...")

	def interfaces_clear(self):
		self.liststore.clear()

	def interface_append(self, interface):
		self.liststore.append(interface)

	def interfaces_update(self):
		interfaces = WirelessInterface.get_interfaces()
		self.interfaces_clear()
		for i in interfaces:
			self.interface_append(i.get_as_tuple())

