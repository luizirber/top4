#!/usr/bin/env python

import sys
from os import listdir
import os.path

import Gnuplot
from numpy import array, arange, histogram
from systat import IOStatReport, MPStatReport, VMStatReport, PIDStatReport

def plot_data(basedir):

    for subdir in listdir(basedir):
        subdir = os.path.join(basedir, subdir)
        if os.path.isdir(subdir):
            iostats = IOStatReport(os.path.join(subdir, "ioreport"))
            mpstats = MPStatReport(os.path.join(subdir, "mpreport"))
            vmstats = VMStatReport(os.path.join(subdir, "vmreport"))
            pidstats = PIDStatReport(os.path.join(subdir, "pidreport"))

            data_stats = open(os.path.join(subdir, 'estatistica'), 'w')

            time = arange(0, 70, 5, dtype="float_")

            g = Gnuplot.Gnuplot()
            g('set terminal postscript enhanced color')
            g("set output '" + os.path.join(subdir, 'grafico.ps') + "'")
            g('set multiplot')

            # CPU Utilization
            data_stats.write("CPU Utilization\n" + "*"*60 + "\n")
            g.title = "CPU Utilization"
            g.xlabel('time (s)')
            g.ylabel('% of CPU time')
            g('set data style linespoints')
            g('set size 0.5,0.5')
            g('set origin 0.0,0.5')

            data = array([float(i['all']['%user']) for i in mpstats.run[1:]],
                         dtype="float_")
            userdata = Gnuplot.Data(data,
                                    title="non-kernel code",
                                    using="($0*5):1",
                                    smooth=1)
            data_stats.write("non-kernel code media: %.2f\n" % data.mean())
            data_stats.write("non-kernel code desvio: %.2f\n" % data.std())
            data_stats.write("non-kernel code histograma: %s\n\n" % [histogram(data)])

            data = array([float(i['all']['%sys']) for i in mpstats.run[1:]],
                         dtype="float_")
            sysdata = Gnuplot.Data(data,
                                   title="kernel code",
                                   using="($0*5):1")
            data_stats.write("kernel code media: %.2f\n" % data.mean())
            data_stats.write("kernel code desvio: %.2f\n" % data.std())
            data_stats.write("kernel code histograma: %s\n\n" % [histogram(data)])

            data = array([float(i['all']['%idle']) for i in mpstats.run[1:]],
                         dtype="float_")
            idledata = Gnuplot.Data(data,
                                    title="idle",
                                    using="($0*5):1",
                                    smooth=1)
            data_stats.write("idle media: %.2f\n" % data.mean())
            data_stats.write("idle desvio: %.2f\n" % data.std())
            data_stats.write("idle histograma: %s\n\n" % [histogram(data)])

            data = array([float(i['all']['%iowait']) for i in mpstats.run[1:]],
                         dtype="float_")
            iodata = Gnuplot.Data(data,
                                  title="waiting IO",
                                  using="($0*5):1",
                                  smooth=1)
            data_stats.write("waiting IO media: %.2f\n" % data.mean())
            data_stats.write("waiting IO desvio: %.2f\n" % data.std())
            data_stats.write("waiting IO histograma: %s\n\n" % [histogram(data)])

            g.plot(userdata, sysdata, idledata, iodata)

            # IO utilization
            data_stats.write("IO Utilization\n" + "*"*60 + "\n")
            g.title = "IO Utilization"
            g.xlabel('time (s)')
            g.ylabel('Memory Fluctuation (kbytes/sec)')
            g('set origin 0.5,0.5')

            data = array([float(i['swap']['si']) for i in vmstats.run[1:]],
                         dtype="float_")
            memindata = Gnuplot.Data(data,
                                    title="memory swapped in from disk",
                                    using="($0*5):1",
                                    smooth=1)
            data_stats.write("memory swapped in from disk media: %.2f\n" % data.mean())
            data_stats.write("memory swapped in from disk desvio: %.2f\n" % data.std())
            data_stats.write("memory swapped in from disk histograma: %s\n\n" % [histogram(data)])

            data = array([float(i['swap']['so']) for i in vmstats.run[1:]],
                         dtype="float_")
            memoutdata = Gnuplot.Data(data,
                                      title="memory swapped to disk",
                                      using="($0*5):1")
            data_stats.write("memory swapped to disk media: %.2f\n" % data.mean())
            data_stats.write("memory swapped to disk desvio: %.2f\n" % data.std())
            data_stats.write("memory swapped to disk histograma: %s\n\n" % [histogram(data)])

            data = array([float(i['io']['bi']) for i in vmstats.run[1:]],
                         dtype="float_")
            bindata = Gnuplot.Data(data,
                                   title="blocks received from a block device",
                                   using="($0*5):1",
                                   smooth=1)
            data_stats.write("blocks received from a block device media: %.2f\n" % data.mean())
            data_stats.write("blocks received from a block device desvio: %.2f\n" % data.std())
            data_stats.write("blocks received from a block device histograma: %s\n\n" % [histogram(data)])

            data = array([float(i['io']['bo']) for i in vmstats.run[1:]],
                         dtype="float_")
            boutdata = Gnuplot.Data(data,
                                    title="blocks sent to a block device",
                                    using="($0*5):1",
                                    smooth=1)
            data_stats.write("blocks sent to a block device media: %.2f\n" % data.mean())
            data_stats.write("blocks sent to a block device desvio: %.2f\n" % data.std())
            data_stats.write("blocks sent to a block device histograma: %s\n\n" % [histogram(data)])

            g.plot(memindata, memoutdata, bindata, boutdata)

            # Mem utilization
            data_stats.write("Mem Utilization\n" + "*"*60 + "\n")
            g.title = "Mem Utilization"
            g.xlabel('time (s)')
            g.ylabel('Memory Used (bytes)')
            g('set logscale y')
            g('set origin 0.0,0.0')

            data = array([float(i['memory']['swpd']) for i in vmstats.run[1:]],
                         dtype="float_")
            userdata = Gnuplot.Data(data,
                                    title="virtual memory",
                                    using="($0*5):1",
                                    smooth=1)
            data_stats.write("virtual memory media: %.2f\n" % data.mean())
            data_stats.write("virtual memory desvio: %.2f\n" % data.std())
            data_stats.write("virtual memory histograma: %s\n\n" % [histogram(data)])

            data = array([float(i['memory']['free']) for i in vmstats.run[1:]],
                         dtype="float_")
            sysdata = Gnuplot.Data(data,
                                   title="idle memory",
                                   using="($0*5):1")
            data_stats.write("idle memory media: %.2f\n" % data.mean())
            data_stats.write("idle memory desvio: %.2f\n" % data.std())
            data_stats.write("idle memory histograma: %s\n\n" % [histogram(data)])

            data = array([float(i['memory']['inact']) for i in vmstats.run[1:]],
                         dtype="float_")
            idledata = Gnuplot.Data(data,
                                    title="inactive memory",
                                    using="($0*5):1",
                                    smooth=1)
            data_stats.write("inactive memory media: %.2f\n" % data.mean())
            data_stats.write("inactive memory desvio: %.2f\n" % data.std())
            data_stats.write("inactive memory histograma: %s\n\n" % [histogram(data)])

            data = array([float(i['memory']['active']) for i in vmstats.run[1:]],
                         dtype="float_")
            iodata = Gnuplot.Data(data,
                                  title="active memory",
                                  using="($0*5):1",
                                  smooth=1)
            data_stats.write("active memory media: %.2f\n" % data.mean())
            data_stats.write("active memory desvio: %.2f\n" % data.std())
            data_stats.write("active memory histograma: %s\n\n" % [histogram(data)])

            g.plot(userdata, sysdata, idledata, iodata)

            # Contexts switched and interrupts
            data_stats.write("Contexts switched and interrupts\n" + "*"*60 + "\n")
            g.title = "Contexts switched and interrupts"
            g.xlabel('time (s)')
            g.ylabel('Interrupts (#/sec)')
            g('unset logscale y')
            g('set origin 0.5,0.0')

            data = array([float(i['all']['intr/s']) for i in mpstats.run[1:]],
                         dtype="float_")
            interruptsdata = Gnuplot.Data(data,
                                    title="Interrupts (including clock)",
                                    using="($0*5):1",
                                    smooth=1)
            data_stats.write("Interrupts media: %.2f\n" % data.mean())
            data_stats.write("Interrupts desvio: %.2f\n" % data.std())
            data_stats.write("Interrupts histograma: %s\n\n" % [histogram(data)])

            data = array([float(i['nvcswch/s']) for i in pidstats.run[1:]],
                         dtype="float_")
            contextdata = Gnuplot.Data(data,
                                   title="Context switched",
                                   using="($0*5):1")
            data_stats.write("Context switched media: %.2f\n" % data.mean())
            data_stats.write("Context switched desvio: %.2f\n" % data.std())
            data_stats.write("Context switched histograma: %s\n\n" % [histogram(data)])

            g.plot(interruptsdata, contextdata)

            g('set nomultiplot')
            g('set output')
            g('reset')

            data_stats.close()


if __name__ == "__main__":
    plot_data(sys.argv[1])

