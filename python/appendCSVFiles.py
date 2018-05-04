import os
import numpy as np
import subprocess

import hammer

inputDirRoot = "/Volumes/yoda/azuri/data/galaxia/ubv_Vlt21.5_1.0/%d_%d/xy"# % (lon, lat)
csvFileNameRoot = "galaxia_%.6f-%.6f_%.6f-%.6f.csv"# % (xMin, xMax, yMin, yMax)
outputDir = "/Volumes/yoda/azuri/data/galaxia/ubv_Vlt21.5_1.0/xy"

ham = hammer.Hammer()
pixels = ham.getPixels()

nFilesProcessed = 0

for lon in np.arange(-175, 180, 10):
    for lat in np.arange(-85, 90, 10):
        inputDir = inputDirRoot % (lon, lat)
        print 'inputDir = <'+inputDir+'>'
        for pix in pixels:
            csvFileName = csvFileNameRoot % (pix.xLow, pix.xHigh, pix.yLow, pix.yHigh)
            csvFileIn = os.path.join(inputDir, csvFileName)
            csvFileOut = os.path.join(outputDir, csvFileName)
            if not os.path.isfile(csvFileOut):
                raise RuntimeError('ERROR: csvFileOut does not exist')

            if os.path.isfile(csvFileIn):
                print 'processing '+csvFileIn
                args = ['cat '+csvFileIn+" >> "+csvFileOut]
                rv = subprocess.call(args, shell=True)
                print 'rv = ',rv
                if rv == 0:
                    nFilesProcessed += 1
                    print "longitude=", lon,", latitude=", lat,", pix=", pix," processed."
                    os.remove(csvFileIn)
                else:
                    print "Error when processing longitude=", lon,", latitude=", lat,", pix=", pix
                    raise RuntimeError("ERROR")

print 'processed ',nFilesProcessed,' files'