#!/bin/sh

wget -c http://weather.ou.edu/~apw/projects/stress/stress-1.0.0.tar.gz
tar zxvf stress-1.0.0.tar.gz
cd stress-1.0.0 && ./configure && make
cp src/stress ../
cd ..
rm -rf stress-1.0.0*

wget -c http://downloads.sourceforge.net/gnuplot-py/gnuplot-py-1.8.tar.gz?use_mirror=ufpr
tar zxvf gnuplot-py-1.8.tar.gz
mv gnuplot-py-1.8 Gnuplot
rm gnuplot-py-1.8.tar.gz
