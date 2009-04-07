#!/usr/bin/env python

from os import listdir
import os.path
import sys

import pyPdf

text = sys.argv[1]
basedata = sys.argv[2]
bonusdata = sys.argv[3]

all = pyPdf.PdfFileWriter()

pdf_graph = pyPdf.PdfFileReader(open(text))
for page in pdf_graph.pages:
    all.addPage(page)

pdf_graph = pyPdf.PdfFileReader(open(os.path.join(basedata, "all.pdf")))
for page in pdf_graph.pages:
    all.addPage(page)

pdf_graph = pyPdf.PdfFileReader(open(os.path.join(bonusdata, "all.pdf")))
for page in pdf_graph.pages:
    all.addPage(page)

outputStream = file("final.pdf", "wb")
all.write(outputStream)
outputStream.close()

