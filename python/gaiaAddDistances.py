#! /usr/bin/env python

import ebf
import gxutil
from multiprocessing import Pool
import os
import sys
import time
import numpy as np
import random

import galcomp
import hammer
import moveStarsToXY

from myUtils import lockAndWriteToFile#(filename,flag,lockName,textToWrite)
from astroutils import addGaiaDistances

class Gaia(object):
    ham = hammer.Hammer()
    inFileNames = []
    keys = []
    keyStr = ''
    lonLatCombinations = []
    fileWorkingName = '/Volumes/discovery/azuri/data/gaia/workinOnFilesGaiaAddDistances.txt'
    fileFinishedName = '/Volumes/discovery/azuri/data/gaia/finishedFilesGaiaAddDistances.txt'
    filesFinished = []
    filesWorking = []
    ids = ['rad', 'hammerX', 'hammerY', 'exbv_solar']
    logContent = []
    logFileName = '/Volumes/discovery/azuri/data/gaia/gaiaAddDistances.log'
    pixels = ham.getPixelsSmallTowardsCenter()

    def __init__(self):
        inputDir = '/Volumes/discovery/azuri/data/gaia/dr2/xy/'
        outputDir = '/Volumes/discovery/azuri/data/gaia/dr2_distances/xy/'
        self.fileNameIn = os.path.join(inputDir, 'GaiaSource_%.6d-%.6d_%.6d-%.6d_xyz.csv')
        self.fileNameOut = os.path.join(outputDir, 'GaiaSource_%.6d-%.6d_%.6d-%.6d_xyz_dist.csv')

    def readFinishedFiles(self):
        if os.path.isfile(Gaia.fileFinishedName):
            self.openFileFinished(flag = 'r')
            lines = Gaia.fileFinished.readlines()
            self.closeFileFinished()
            for line in lines:
                Gaia.filesFinished.append(line[0:line.find(' ')])
            return True
        return False

    def readWorkingFiles(self):
        if os.path.isfile(Gaia.fileWorkingName):
            self.openFileWorking(flag = 'r')
            lines = Gaia.fileWorking.readlines()
            self.closeFileWorking()
            for line in lines:
                Gaia.filesWorking.append(line[0:line.find('\n')])
            return True
        return False

    def readLogFile(self):
        if os.path.isfile(Gaia.logFileName):
            logFile = open(Gaia.logFileName, 'r')
            lines = logFile.readlines()
            logFile.close()
            for line in lines:
                lineSplit = line.split(' ')
                if lineSplit[0] == 'ran':
                    iIt = lineSplit[4]
                    fName = lineSplit[9]
#                    if fName == '/Volumes/discovery/azuri/data/gaia/sdss/gaia_-25_-5.ebf':
#                        print 'fName = <',fName,'>: iIt read = ',iIt
                    if (fName in Gaia.filesWorking) and (fName not in Gaia.filesFinished):
#                        if fName == '/Volumes/discovery/azuri/data/gaia/sdss/gaia_-25_-5.ebf':
#                            print 'file <',fName,'> found in filesWorking but not in filesFinished'
                        fPos = -1
                        if len(Gaia.logContent) > 0:
                            fNames = [Gaia.logContent[i][0] for i in range(len(Gaia.logContent))]
                            try:
                                fPos = fNames.index(fName)
#                                if fName == '/Volumes/discovery/azuri/data/gaia/sdss/gaia_-25_-5.ebf':
#                                    print 'file <',fName,'> found in logContent: fPos = ',fPos
                            except:
                                """do nothing"""
#                                if fName == '/Volumes/discovery/azuri/data/gaia/sdss/gaia_-25_-5.ebf':
#                                    print 'file <',fName,'> NOT found in logContent'
                        if fPos < 0:
                            Gaia.logContent.append([fName, iIt])
                            fPos = len(Gaia.logContent)-1
                        else:
                            Gaia.logContent[fPos][1] = iIt
 #                       if fName == '/Volumes/discovery/azuri/data/gaia/sdss/gaia_-25_-5.ebf':
 #                           print 'Gaia.logContent[',fPos,'][:] = ',Gaia.logContent[fPos]
 #           print 'Gaia.logContent = ',len(Gaia.logContent),': ',Gaia.logContent
        else:
            Gaia.logContent = [['a',-1]]

    def processGaia(self, iCombo):
#        print 'processGaia started'
#        print 'Gaia.keys = ',Gaia.keys
#        print 'Gaia.keyStr = ',Gaia.keyStr
#        print 'self.fileNameIn = ',self.fileNameIn
        doIt = True
        px = pixels(iCombo)
        inputFile = self.fileNameIn % (px.xLow,px.xHigh,px.yLow,px.yLow)
        outputFile = self.fileNameOut % (px.xLow,px.xHigh,px.yLow,px.yLow)

        if doIt:
            if inputFile not in self.filesFinished:
                if not os.path.isfile(inputFile):
                    print "ERROR: gaia input file ",inputFile," not found"
                    lockAndWriteToFile(logFileName,'a',os.path.join('/Users/azuri/var/log/',logFileName),inputFile+' not found')
                else:
                    timeStart = time.time()
                    print('starting ',inputFileName)
                    lockAndWriteToFile(filesWorkingName,'a',os.path.join('/Users/azuri/var/log/',logFileName),inputFile)
                    self.filesWorking.append(inputFile)
                    addGaiaDistances(inputFile,outputFile)
                    timeEnd = time.time()
                    duration = timeEnd-timeStart
                    print('ran file <',inputFile,'> in ',duration,' s')
                    lockAndWriteToFile(logFileName,'a',os.path.join('/Users/azuri/var/log/',logFileName),inputFile+' done in '+str(duration)+'s')
                    lockAndWriteToFile(fileFinishedName,'a',os.path.join('/Users/azuri/var/log/',fileFinishedName[fileFinishedName.rfind('/')+1:]),inputFile)
                    self.filesFinished.append(inputFile)
            else:
                print 'file <',inputFile,'> already finished'

def processGaia(iCombo):
    gal = Gaia()
    gal.processGaia(iCombo)

def main(argv):
    """Main program.

    Arguments:
    argv -- command line arguments
    """
    gal = Gaia()
    if not gal.readWorkingFiles():
        gal.openFileWorking('w')
        gal.closeFileWorking()
    if not gal.readFinishedFiles():
        gal.openFileFinished('w')
        gal.closeFileFinished()
    gal.readLogFile()

    if True:
        p = Pool(processes=12)
        iCombo = np.arange(len(Gaia.pixels))
        random.shuffle(iCombo)
        p.map(processGaia, iCombo)
        p.close()
    else:

if __name__ == '__main__':
    main(sys.argv)
