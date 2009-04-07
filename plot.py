#!/usr/bin/env python

import sys
from os import listdir
import os.path
from math import ceil, floor

import Gnuplot
from numpy import array, arange, histogram
from systat import IOStatReport, MPStatReport, VMStatReport, PIDStatReport

def plot_data(basedir):

    for subdir in sorted(listdir(basedir)):
        subdir = os.path.join(basedir, subdir)
        if os.path.isdir(subdir):
            iostats = IOStatReport(os.path.join(subdir, "ioreport"))
            mpstats = MPStatReport(os.path.join(subdir, "mpreport"))
            vmstats = VMStatReport(os.path.join(subdir, "vmreport"))
            pidstats = PIDStatReport(os.path.join(subdir, "pidreport"))

            data_stats = []

            time = arange(0, 70, 5, dtype="float_")

            g = Gnuplot.Gnuplot()
            g('set terminal postscript enhanced "Helvetica" 12 color')
            g("set output '" + os.path.join(subdir, 'grafico.ps') + "'")
            g('set size 1,1')
            g('set origin 0,0')
            g('set multiplot layout 2,2 scale 1,0.95 title "%s"' % subdir.split('/')[-1])

            # CPU Utilization
            g.title("CPU Utilization")
            g.xlabel('time (s)')
            g.ylabel('% of CPU time')
            g('set data style linespoints')

            data = array([float(i['all']['%user']) for i in mpstats.run[1:]],
                         dtype="float_")
            userdata = Gnuplot.Data(data,
                                    title="non-kernel code",
                                    using="($0*5):1",
                                    smooth=1)
            data_stats.append({'title':"non-kernel code",
                              'data':data})

            data = array([float(i['all']['%sys']) for i in mpstats.run[1:]],
                         dtype="float_")
            sysdata = Gnuplot.Data(data,
                                   title="kernel code",
                                   using="($0*5):1")
            data_stats.append({'title':"kernel code",
                              'data':data})

            data = array([float(i['all']['%idle']) for i in mpstats.run[1:]],
                         dtype="float_")
            idledata = Gnuplot.Data(data,
                                    title="idle",
                                    using="($0*5):1",
                                    smooth=1)
            data_stats.append({'title':"idle",
                              'data':data})

            data = array([float(i['all']['%iowait']) for i in mpstats.run[1:]],
                         dtype="float_")
            iodata = Gnuplot.Data(data,
                                  title="waiting IO",
                                  using="($0*5):1",
                                  smooth=1)
            data_stats.append({'title':"waiting IO",
                              'data':data})

            g.plot(userdata, sysdata, idledata, iodata)

            # IO utilization
            g.title("IO Utilization")
            g.xlabel('time (s)')
            g.ylabel('Memory Fluctuation (kbytes/sec)')

            data = array([float(i['swap']['si']) for i in vmstats.run[1:]],
                         dtype="float_")
            memindata = Gnuplot.Data(data,
                                    title="memory swapped in from disk",
                                    using="($0*5):1",
                                    smooth=1)
            data_stats.append({'title':"memory swapped in from disk",
                              'data':data})

            data = array([float(i['swap']['so']) for i in vmstats.run[1:]],
                         dtype="float_")
            memoutdata = Gnuplot.Data(data,
                                      title="memory swapped to disk",
                                      using="($0*5):1")
            data_stats.append({'title':"memory swapped to disk",
                              'data':data})

            data = array([float(i['io']['bi']) for i in vmstats.run[1:]],
                         dtype="float_")
            bindata = Gnuplot.Data(data,
                                   title="blocks received from a block device",
                                   using="($0*5):1",
                                   smooth=1)
            data_stats.append({'title':"blocks received from a block device",
                              'data':data})

            data = array([float(i['io']['bo']) for i in vmstats.run[1:]],
                         dtype="float_")
            boutdata = Gnuplot.Data(data,
                                    title="blocks sent to a block device",
                                    using="($0*5):1",
                                    smooth=1)
            data_stats.append({'title':"blocks sent to a block device",
                              'data':data})

            g.plot(memindata, memoutdata, bindata, boutdata)

            # Mem utilization
            g.title("Mem Utilization")
            g.xlabel('time (s)')
            g.ylabel('Memory Used (bytes)')
            g('set logscale y')

            data = array([float(i['memory']['swpd']) for i in vmstats.run[1:]],
                         dtype="float_")
            userdata = Gnuplot.Data(data,
                                    title="virtual memory",
                                    using="($0*5):1",
                                    smooth=1)
            data_stats.append({'title':"virtual memory",
                              'data':data})

            data = array([float(i['memory']['free']) for i in vmstats.run[1:]],
                         dtype="float_")
            sysdata = Gnuplot.Data(data,
                                   title="idle memory",
                                   using="($0*5):1")
            data_stats.append({'title':"idle memory",
                              'data':data})

            data = array([float(i['memory']['inact']) for i in vmstats.run[1:]],
                         dtype="float_")
            idledata = Gnuplot.Data(data,
                                    title="inactive memory",
                                    using="($0*5):1",
                                    smooth=1)
            data_stats.append({'title':"inactive memory",
                              'data':data})

            data = array([float(i['memory']['active']) for i in vmstats.run[1:]],
                         dtype="float_")
            iodata = Gnuplot.Data(data,
                                  title="active memory",
                                  using="($0*5):1",
                                  smooth=1)
            data_stats.append({'title':"active",
                              'data':data})

            g.plot(userdata, sysdata, idledata, iodata)

            # Contexts switched and interrupts
            g.title("Contexts switched and interrupts")
            g.xlabel('time (s)')
            g.ylabel('Interrupts (#/sec)')
            g('unset logscale y')

            data = array([float(i['all']['intr/s']) for i in mpstats.run[1:]],
                         dtype="float_")
            interruptsdata = Gnuplot.Data(data,
                                    title="Interrupts (including clock)",
                                    using="($0*5):1",
                                    smooth=1)
            data_stats.append({'title':"Interrupts (including clock)",
                              'data':data})

            data = array([float(i['nvcswch/s']) for i in pidstats.run[1:]],
                         dtype="float_")
            contextdata = Gnuplot.Data(data,
                                   title="Context switched",
                                   using="($0*5):1")
            data_stats.append({'title':"Context switched",
                              'data':data})

            g.plot(interruptsdata, contextdata)

            g('set nomultiplot')
            g('set output')
            g('reset')

            # plot histograms
            g('set terminal postscript enhanced "Helvetica" 8 color')
            g("set output '" + os.path.join(subdir, 'histogramas.ps') + "'")
            g('set size 1,1')
            g('set origin 0,0')
            g('set style data histogram')
            g('set style fill solid border -1')
            g('set xtic rotate by -45')
            g.xlabel('Faixas')
            g.ylabel('Frequencias')
            g('set key off')
            g('set multiplot layout 4,4 scale 1,0.95 title "%s"' %
               subdir.split('/')[-1])

            for data in data_stats:
                g.title(data['title'])
                hdata = histogram(data['data'])

                g('set yrange [0:30]')

                low = int(floor(hdata[1][0]))
                high = int(floor(hdata[1][-1])) + 1
                fill = int(ceil(hdata[1][1] - low))
                g('set xrange [%d:%d]' % (low, high))
                g('set xtics %d,%d' % (low, fill))
                g('set boxwidth %f' % fill)

                gdata = Gnuplot.Data(hdata[0],
                                     using="($0*%f+%f):1" % (float(fill), float(low)),
                                     with_="boxes",
                                     smooth=1)
                g.plot(gdata)
            g('set nomultiplot')
            g('set output')
            g('reset')

#            data_stats.write("non-kernel code media: %.2f\n" % data.mean())
#            data_stats.write("non-kernel code desvio: %.2f\n" % data.std())
#            data_stats.write("non-kernel code variancia: %.2f\n" % pow(data.std(), 2))
#            data_stats.write("non-kernel code histograma: %s\n\n" % [histogram(data)])


            #data_stats.close()


if __name__ == "__main__":
    plot_data(sys.argv[1])

