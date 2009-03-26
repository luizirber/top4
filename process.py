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

        data = {}
        data['data'] = header_data
        self.run.append(data)

    def read_data(self, lines):
        timeslice = self.run[-1]['data']
        keys = lines[0].split()[1:]

        for line in lines[1:]:
            data = line.split()
            timeslice[data[0]] = dict(zip(keys, data[1:]))

    def print_data(self):
        print self.system
        for run in self.run:
            pprint(run)
            print

if __name__ == "__main__":
    stats = IOStatReport(sys.argv[1])
    stats.print_data()
