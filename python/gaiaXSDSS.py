#! /usr/bin/env python
#
from multiprocessing import Pool
import os
import sys
import time
import numpy as np
import random

import csvData# for CSVData as a return type
import csvFree
import hammer
import moveStarsToXY


def getGaiaIndex(csvGaia, source_id):
    source_ids = csvGaia.getData('source_id')
    for i in range(csvGaia.size()):
        if source_ids[i] == source_id:
            return i
    return -1

headerGaia = csvFree.readCSVFile('/Volumes/obiwan/azuri/data/gaia/dr2/xy/GaiaSource_2.810749-2.828427_0.159099-0.176777.csv', ',', True).header
headerXMatch = csvFree.readCSVFile('/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2distXSDSS12/xy/GaiaXSDSS_2.810749-2.828427_0.053033-0.070711.csv', ',', True).header

headerOut = []
for key in headerGaia:
    headerOut.append(key)
for key in headerXMatch:
    if key not in headerOut:
        headerOut.append(key)

inFilesGaiaRoot = '/Volumes/obiwan/azuri/data/gaia/dr2/xy/GaiaSource_%.6f-%.6f_%.6f-%.6f.csv'
inFilesXMatchRoot = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2distXSDSS12/xy/GaiaXSDSS_%.6f-%.6f_%.6f-%.6f.csv'
outFilesXMatchRoot = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2distXSDSS12/xy/Gaia+SDSS_%.6f-%.6f_%.6f-%.6f.csv'
ham = hammer.Hammer()
pixels = ham.getPixels()

def process(iFile):
    outFile = outFilesXMatchRoot % (pixels[iFile].xLow, pixels[iFile].xHigh, pixels[iFile].yLow, pixels[iFile].yHigh)
    if True:#not os.path.isfile(outFile):
        nFound = 0

        inFileXMatch = inFilesXMatchRoot % (pixels[iFile].xLow, pixels[iFile].xHigh, pixels[iFile].yLow, pixels[iFile].yHigh)
        print('reading inFileXMatch = <'+inFileXMatch+'>)')
        csvXMatch = csvFree.readCSVFile(inFileXMatch, ',', True)

        csvOut = csvData.CSVData()
        csvOut.header = headerOut

        if csvXMatch.size() > 0:
            inFileGaia = inFilesGaiaRoot % (pixels[iFile].xLow, pixels[iFile].xHigh, pixels[iFile].yLow, pixels[iFile].yHigh)
            csvGaia = csvFree.readCSVFile(inFileGaia, ',', True)
            nStarsGaia = csvGaia.size()

            sourceIds = csvGaia.getData('source_id')
            for iStarXMatch in range(csvXMatch.size()):
                id = csvXMatch.getData('id', iStarXMatch)

                found = False
                iStarGaia = 0
                while (not found) and (iStarGaia < nStarsGaia):
                    if sourceIds[iStarGaia] == id:
                        found = True
                    else:
                        iStarGaia += 1
                if found:
#                    print('id '+id+' found in csvGaia at position ',iStarGaia)
                    rowOut = csvGaia.getData(iStarGaia)
    #                print('csvGaia[',iStarGaia,'] = ',len(rowOut),': ',rowOut)

    #                print('len(headerGaia) = ',len(headerGaia),', len(headerOut) = ',len(headerOut))
                    for iHeader in np.arange(len(headerGaia), len(headerOut)):
                        rowOut.append(csvXMatch.getData(headerOut[iHeader], iStarXMatch))
    #                    print('iHeader = ',iHeader,': rowOut = ',len(rowOut),': ',rowOut)
    #                print('rowOut = ',len(rowOut),': ',rowOut)
                    csvOut.append(rowOut)
                    nFound += 1
                else:
                    print('id '+id+' NOT found in csvGaia')

        print('writing ',nFound,' stars to '+outFile)
        csvFree.writeCSVFile(csvOut, outFile)
#        return csvOut

starsFound = False
pixRange = range(len(pixels))

p = Pool(processes=16)
p.map(process, pixRange)
p.close()
