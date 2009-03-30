#!/usr/bin/env python

import sys

import Gnuplot
from numpy import array, arange
from systat import IOStatReport, MPStatReport, VMStatReport

if __name__ == "__main__":
    iostats = IOStatReport(sys.argv[1] + "ioreport")
    mpstats = MPStatReport(sys.argv[1] + "mpreport")
    vmstats = VMStatReport(sys.argv[1] + "vmreport")

    time = arange(0, 70, 5, dtype="float_")

    g = Gnuplot.Gnuplot()
    g('set multiplot')

    # CPU Utilization
    g.title = "CPU Utilization"
    g.xlabel('time (s)')
    g.ylabel('% of CPU time')
    g('set data style lines')
    g('set size 0.5,0.5')
    g('set origin 0.0,0.5')

    data = array([float(i['all']['%user']) for i in mpstats.run[1:]],
                 dtype="float_")
    userdata = Gnuplot.Data(data,
                            title="non-kernel code",
                            using="($0*5):1",
                            smooth=1)

    data = array([float(i['all']['%sys']) for i in mpstats.run[1:]],
                 dtype="float_")
    sysdata = Gnuplot.Data(data,
                           title="kernel code",
                           using="($0*5):1")

    data = array([float(i['all']['%idle']) for i in mpstats.run[1:]],
                 dtype="float_")
    idledata = Gnuplot.Data(data,
                            title="idle",
                            using="($0*5):1",
                            smooth=1)

    data = array([float(i['all']['%iowait']) for i in mpstats.run[1:]],
                 dtype="float_")
    iodata = Gnuplot.Data(data,
                          title="waiting IO",
                          using="($0*5):1",
                          smooth=1)

    g.plot(userdata, sysdata, idledata, iodata)

    # IO utilization
    g.title = "IO Utilization"
    g.xlabel('time (s)')
    g.ylabel('Memory Fluctuation (kbytes/sec)')
    g('set data style lines')
    g('set origin 0.5,0.5')

    data = array([float(i['swap']['si']) for i in vmstats.run[1:]],
                 dtype="float_")
    memindata = Gnuplot.Data(data,
                            title="memory swapped in from disk",
                            using="($0*5):1",
                            smooth=1)

    data = array([float(i['swap']['so']) for i in vmstats.run[1:]],
                 dtype="float_")
    memoutdata = Gnuplot.Data(data,
                              title="memory swapped to disk",
                              using="($0*5):1")

    data = array([float(i['io']['bi']) for i in vmstats.run[1:]],
                 dtype="float_")
    bindata = Gnuplot.Data(data,
                           title="blocks received from a block device",
                           using="($0*5):1",
                           smooth=1)

    data = array([float(i['io']['bo']) for i in vmstats.run[1:]],
                 dtype="float_")
    boutdata = Gnuplot.Data(data,
                            title="blocks sent to a block device",
                            using="($0*5):1",
                            smooth=1)

    g.plot(memindata, memoutdata, bindata, boutdata)

    # Mem utilization
    g.title = "Mem Utilization"
    g.xlabel('time (s)')
    g.ylabel('Memory Used (bytes)')
    g('set data style lines')
    g('set logscale y')
    g('set origin 0.0,0.0')

    data = array([float(i['memory']['swpd']) for i in vmstats.run[1:]],
                 dtype="float_")
    userdata = Gnuplot.Data(data,
                            title="virtual memory",
                            using="($0*5):1",
                            smooth=1)

    data = array([float(i['memory']['free']) for i in vmstats.run[1:]],
                 dtype="float_")
    sysdata = Gnuplot.Data(data,
                           title="idle memory",
                           using="($0*5):1")

    data = array([float(i['memory']['inact']) for i in vmstats.run[1:]],
                 dtype="float_")
    idledata = Gnuplot.Data(data,
                            title="inactive memory",
                            using="($0*5):1",
                            smooth=1)

    data = array([float(i['memory']['active']) for i in vmstats.run[1:]],
                 dtype="float_")
    iodata = Gnuplot.Data(data,
                          title="active memory",
                          using="($0*5):1",
                          smooth=1)

    g.plot(userdata, sysdata, idledata, iodata)

    # Contexts switched and interrupts
    g.title = "Contexts switched and interrupts"
    g.xlabel('time (s)')
    g.ylabel('Interrupts (#/sec)')
    g('unset logscale y')
    g('set data style lines')
    g('set origin 0.5,0.0')

    data = array([float(i['all']['intr/s']) for i in mpstats.run[1:]],
                 dtype="float_")
    interruptsdata = Gnuplot.Data(data,
                            title="Interrupts (including clock)",
                            using="($0*5):1",
                            smooth=1)

    # TODO: fix this!
    data = array([float(i['all']['%steal']) for i in mpstats.run[1:]],
                 dtype="float_")
    contextdata = Gnuplot.Data(data,
                           title="Context switched",
                           using="($0*5):1")

    g.plot(interruptsdata, contextdata)

    g('set nomultiplot')
    g.hardcopy('cpu.ps', terminal='postscript', enhanced=1, color=1)
    raw_input()

