#!/usr/bin/env python

import sys
from pprint import pprint

class IOStatReport(object):
    def __init__(self, filename):
        self.fd = open(filename, 'r')
        self.read_system_info()
        self.run = []

        header_buffer = []
        reading_header = True
        data_buffer = []
        reading_data = False

        line = self.fd.readline()
        while line:
            if reading_header:
                if line == '\n':
                    reading_header = False
                    self.read_header(header_buffer)
                    header_buffer = []
                    reading_data = True
                else:
                    header_buffer.append(line)
            elif reading_data:
                if line == '\n':
                    reading_data = False
                    self.read_data(data_buffer)
                    data_buffer = []
                    reading_header = True
                else:
                    data_buffer.append(line)

            line = self.fd.readline()

    def read_system_info(self):
        line = self.fd.readline()[:-1]
        data = line.split()

        system = {}
        system['kernel'] = data[0]
        system['version'] = data[1]
        system['hostname'] = data[2][1:-1]
        system['date'] = data[3]

        self.system = system
        self.fd.readline()

    def read_header(self, lines):
        time = lines[0].split()
        keys = lines[1].split()[1:]
        values = lines[2].split()

        header_data = dict(zip(keys, values))
        header_data[time[0]] = "".join(time[1:])

        self.run.append(header_data)

    def read_data(self, lines):
        timeslice = self.run[-1]
        keys = lines[0].split()[1:]

        for line in lines[1:]:
            data = line.split()
            timeslice[data[0]] = dict(zip(keys, data[1:]))

    def print_data(self):
        print self.system
        for run in self.run:
            pprint(run)
            print


class MPStatReport(object):
    def __init__(self, filename):
        self.fd = open(filename, 'r')
        self.read_system_info()
        self.run = []

        data_buffer = []

        line = self.fd.readline()
        while line:
            if line == '\n':
                self.read_data(data_buffer)
                data_buffer = []
            else:
                data_buffer.append(line)

            line = self.fd.readline()

    def read_system_info(self):
        line = self.fd.readline()[:-1]
        data = line.split()

        system = {}
        system['kernel'] = data[0]
        system['version'] = data[1]
        system['hostname'] = data[2][1:-1]
        system['date'] = data[3]

        self.system = system
        self.fd.readline()

    def read_data(self, lines):
        timeslice = {}
        line = lines[0].split()

        time = line[:1]
        keys = line[3:]

        for lin in lines[1:]:
            data = lin.split()
            timeslice[data[2]] = dict(zip(keys, data[3:]))

        timeslice["Time"] = "".join(time)

        self.run.append(timeslice)

    def print_data(self):
        print self.system
        for run in self.run:
            pprint(run)
            print


class VMStatReport(object):
    def __init__(self, filename):
        self.fd = open(filename, 'r')
        self.run = []

        self.read_data(self.fd.readlines())

    def read_data(self, lines):
        topkeys = lines[0][:-1].split()
        subkeys = lines[1][:-1].split()

        for line in lines[2:]:
            ts = {}
            data = line[:-1].split()

            ts[topkeys[0].strip('-')] = dict(zip(subkeys[  :2 ], data[:2]))
            ts[topkeys[1].strip('-')] = dict(zip(subkeys[2 :6 ], data[2 :6]))
            ts[topkeys[2].strip('-')] = dict(zip(subkeys[6 :8 ], data[6 :8]))
            ts[topkeys[3].strip('-')] = dict(zip(subkeys[8 :10], data[8 :10]))
            ts[topkeys[4].strip('-')] = dict(zip(subkeys[10:12], data[10:12]))
            ts[topkeys[5].strip('-')] = dict(zip(subkeys[12:  ], data[12:]))
            self.run.append(ts)

    def print_data(self):
        print self.system
        for run in self.run:
            pprint(run)
            print

