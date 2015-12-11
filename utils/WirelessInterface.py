#!/usr/bin/python
# -*- coding: utf-8 -*-

#from subprocess import Popen, PIPE, DEVNULL
from scapy.all import *
from subprocess import call


class WirelessInterface:
    def __init__(self, name, mac, mode):
        self.name = name
        self.mac = mac
        self.mode = mode

    def get_as_tuple(self):
        return self.name, self.mac, self.mode

    def mac_randomize(self):
        random.seed()
        new_mac = self.mac
        while new_mac == self.mac:
            new_mac = ''
            for i in range(0, 12):
                if i % 2 == 0 and i != 0:
                    new_mac += ':'
                new_mac += '0123456789ABCDEF'[random.randint(0, 15)]
        call(['ifconfig', self.name, 'down'])
        call(['ifconfig', self.name, 'hw', 'ether', new_mac])
        call(['ifconfig', self.name, 'up'])
        print("[!] WirelessInterface.mac_randomize(): TODO: Implement checking!")

    @staticmethod
    def get_interfaces():
        """
        try:
            process = Popen(['iwconfig'], stdout=PIPE, stderr=DEVNULL)
            interface = ''
            mac = ''
            interface_list = []
            for line in process.communicate()[0].split('\n'):
                if len(line) == 0:
                    continue
                if ord(line[0]) != 32:                  # Doesn't start with space
                    interface = line[:line.find(' ')]   # Is the interface
                    if_process = Popen(['ifconfig', interface], stdout=PIPE, stderr=DEVNULL)
                    if_process.wait()
                    first_line = if_process.communicate()[0].split('\n')[0]
                    for word in first_line.split(' '):
                        if word != '':
                            mac = word
                        if mac.find('-') != -1:
                            mac = mac.replace('-', ':')
                        if len(mac) > 17:
                            mac = mac[0:17]
                if line.find('Mode:Monitor') != -1:
                    interface_list.append(WirelessInterface(interface, mac, 'monitor'))
                else:
                    interface_list.append(WirelessInterface(interface, mac, 'managed'))

            return interface_list
        except FileNotFoundError:
            print("[!] utils.WirelessInterface.get_interfaces(): FileNotFoundError: TODO: Warn user of fix!")
            return []
        """
        interfaces = []
        for iface_name in sorted(ifaces.data.keys()):
            dev = ifaces.data[iface_name]
            interfaces.append(WirelessInterface(dev.name, dev.mac, 'Unsuported'))
        print("[!] WirelessInterface.get_interfaces(): TODO: Implement mode detection!")
        return interfaces