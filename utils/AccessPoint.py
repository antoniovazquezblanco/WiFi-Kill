#!/usr/bin/python
# -*- coding: utf-8 -*-


class AccessPoint:
    def __init__(self, bssid):
        self.bssid = bssid
        self.essid = '<unknown>'
        self.power = 0
        self.packets = 0

    def get_as_tuple(self):
        return self.bssid, self.essid, self.power, self.packets
