#!/usr/bin/env python

from os import listdir
import os.path
import sys

import pyPdf

basedir = sys.argv[1]
all = pyPdf.PdfFileWriter()
for subdir in sorted(listdir(basedir)):
    subdir = os.path.join(basedir, subdir)
    if os.path.isdir(subdir):
#        output = pyPdf.PdfFileWriter()

        pdf_graph = pyPdf.PdfFileReader(open(os.path.join(subdir, "grafico.pdf")))
        for page in pdf_graph.pages:
#            output.addPage(page)
            all.addPage(page)

        pdf_histo = pyPdf.PdfFileReader(open(os.path.join(subdir, "histogramas.pdf")))
        for page in pdf_histo.pages:
#            output.addPage(page)
            all.addPage(page)

#        outputStream = file(os.path.join(subdir, "both.pdf"), "wb")
#        output.write(outputStream)
#        outputStream.close()

outputStream = file(os.path.join(basedir, "all.pdf"), "wb")
all.write(outputStream)
outputStream.close()

