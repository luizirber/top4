#!/bin/sh

#./install
#./run.sh $1
./plot.py $1
./plot.py $2
./pdfgen.sh $1
./pdfmerger.py $1
./pdffinal.sh desempenho.pdf $1 $2
