#!/bin/sh

wget -c http://weather.ou.edu/~apw/projects/stress/stress-1.0.0.tar.gz
tar zxvf stress-1.0.0.tar.gz
cd stress-1.0.0 && ./configure && make
cp src/stress ../
cd ..
rm -rf stress-1.0.0*
