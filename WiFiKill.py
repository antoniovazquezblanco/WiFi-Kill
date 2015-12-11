#!/usr/bin/python
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from utils import WirelessInterface
from utils import Sniffer


class WiFiKill:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("WiFiKill.glade")
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("window_main")
        self.log_text = self.builder.get_object("window_main_notebook_log_text")
        self.log_text_buff = self.log_text.get_buffer()
        self.interface_liststore = self.builder.get_object("window_main_liststore_interfaces")
        self.sniffer_thread = Sniffer()

    def loop(self):
        self.window.show_all()
        Gtk.main()

    def interfaces_clear(self):
        self.interface_liststore.clear()

    def interface_append(self, interface):
        self.interface_liststore.append(interface)

    def log_append(self, text):
        end_iter = self.log_text_buff.get_end_iter()
        self.log_text_buff.insert(end_iter, text)

    @staticmethod
    def on_destroy(*args):
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

if __name__ == "__main__":
    win = WiFiKill()
    win.loop()
