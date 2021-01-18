#! /usr/bin/env python
import glob
from multiprocessing import Pool
import os
import sys
import time
import numpy as np
import random

#import galcomp
import hammer
import moveStarsToXY

from myUtils import lockAndWriteToFile#(filename,flag,lockName,textToWrite)
from astroutils import addGaiaDistances

class Gaia(object):
    ham = hammer.Hammer()
    inFileNames = []
    fileWorkingName = '/Volumes/discovery/azuri/data/gaia/workinOnFilesGaiaAddDistances.txt'
    fileFinishedName = '/Volumes/discovery/azuri/data/gaia/finishedFilesGaiaAddDistances.txt'
    filesFinished = []
    filesWorking = []
    logContent = []
    logFileName = '/Volumes/discovery/azuri/data/gaia/gaiaAddDistances.log'
    pixels = ham.getPixelsSmallTowardsCenter()
    fileNameIn = ''
    fileNameOut = ''

    def __init__(self):
        inputDir = '/Volumes/discovery/azuri/data/gaia/dr2/xy/'
        outputDir = '/Volumes/discovery/azuri/data/gaia/dr2_distances/xy/'
        self.fileNameIn = os.path.join(inputDir, 'GaiaSource_%.6f-%.6f_%.6f-%.6f_xyz.csv')
        self.fileNameOut = os.path.join(outputDir, 'GaiaSource_%.6f-%.6f_%.6f-%.6f_xyz_dist.csv')

    def readFinishedFiles(self):
        if os.path.isfile(Gaia.fileFinishedName):
            with open(self.fileFinishedName,'r') as f:
                lines = f.readlines()
            for line in lines:
                Gaia.filesFinished.append(line[0:line.find('\n')])
            print('filesFinished = ',Gaia.filesFinished)
            #STOP
            return True
        return False

    def readWorkingFiles(self):
        if os.path.isfile(Gaia.fileWorkingName):
            with open(self.fileWorkingName,'r') as f:
                lines = f.readlines()
            for line in lines:
                Gaia.filesWorking.append(line[0:line.find('\n')])
            return True
        return False

    def readLogFile(self):
        if os.path.isfile(Gaia.logFileName):
            logFile = open(Gaia.logFileName, 'r')
            lines = logFile.readlines()
            logFile.close()
            iIt = 0
            for line in lines:
                lineSplit = line.split(' ')
                if lineSplit[1] == 'done':
                    fName = lineSplit[0]
#                    if fName == '/Volumes/discovery/azuri/data/gaia/sdss/gaia_-25_-5.ebf':
#                        print('fName = <',fName,'>: iIt read = ',iIt)
                    if (fName in Gaia.filesWorking) and (fName not in Gaia.filesFinished):
#                        if fName == '/Volumes/discovery/azuri/data/gaia/sdss/gaia_-25_-5.ebf':
#                            print('file <',fName,'> found in filesWorking but not in filesFinished')
                        fPos = -1
                        if len(Gaia.logContent) > 0:
                            fNames = [Gaia.logContent[i][0] for i in range(len(Gaia.logContent))]
                            try:
                                fPos = fNames.index(fName)
#                                if fName == '/Volumes/discovery/azuri/data/gaia/sdss/gaia_-25_-5.ebf':
#                                    print('file <',fName,'> found in logContent: fPos = ',fPos)
                            except:
                                """do nothing"""
#                                if fName == '/Volumes/discovery/azuri/data/gaia/sdss/gaia_-25_-5.ebf':
#                                    print('file <',fName,'> NOT found in logContent')
                        if fPos < 0:
                            Gaia.logContent.append([fName, iIt])
                            fPos = len(Gaia.logContent)-1
                        else:
                            Gaia.logContent[fPos][1] = iIt
 #                       if fName == '/Volumes/discovery/azuri/data/gaia/sdss/gaia_-25_-5.ebf':
 #                           print('Gaia.logContent[',fPos,'][:] = ',Gaia.logContent[fPos])
 #           print('Gaia.logContent = ',len(Gaia.logContent),': ',Gaia.logContent)
                    iIt += 1
        else:
            Gaia.logContent = [['a',-1]]
        print('Gaia.logContent = ',Gaia.logContent)
        STOP

    def processGaia(self, iCombo):
#        print('processGaia started')
#        print('self.fileNameIn = ',self.fileNameIn)
        doIt = True
        px = self.pixels[iCombo]
        print('px = ',px)
        inputFile = self.fileNameIn % (px.xLow,px.xHigh,px.yLow,px.yHigh)
        outputFile = self.fileNameOut % (px.xLow,px.xHigh,px.yLow,px.yHigh)

        if doIt:
            if inputFile not in self.filesFinished:
                if not os.path.isfile(inputFile):
                    print("ERROR: gaia input file ",inputFile," not found")
                    lockAndWriteToFile(self.logFileName,'a',os.path.join('/Users/azuri/var/log/',self.logFileName[self.logFileName.rfind('/')+1:]),inputFile+' not found\n')
                else:
                    timeStart = time.time()
                    print('starting ',inputFile)
                    lockAndWriteToFile(self.logFileName,'a',os.path.join('/Users/azuri/var/log/',self.logFileName[self.logFileName.rfind('/')+1:]),inputFile+' started\n')
                    lockAndWriteToFile(self.fileWorkingName,'a',os.path.join('/Users/azuri/var/log/',self.fileWorkingName[self.fileWorkingName.rfind('/')+1:]),inputFile+'\n')
                    self.filesWorking.append(inputFile)
                    addGaiaDistances(inputFile,outputFile)
                    timeEnd = time.time()
                    duration = timeEnd-timeStart
                    print('ran file <',inputFile,'> in ',duration,' s')
                    lockAndWriteToFile(self.logFileName,'a',os.path.join('/Users/azuri/var/log/',self.logFileName[self.logFileName.rfind('/')+1:]),inputFile+' done in '+str(duration)+'s\n')
                    lockAndWriteToFile(self.fileFinishedName,'a',os.path.join('/Users/azuri/var/log/',self.fileFinishedName[self.fileFinishedName.rfind('/')+1:]),inputFile+'\n')
                    self.filesFinished.append(inputFile)
            else:
                print('file <',inputFile,'> already finished')

def processGaia(iCombo):
    gal = Gaia()
    gal.processGaia(iCombo)

def main(argv):
    """Main program.

    Arguments:
    argv -- command line arguments
    """
    gal = Gaia()
    files = glob.glob('/Users/azuri/var/log/*')
    for f in files:
        os.remove(f)
#    if not gal.readWorkingFiles():
#        open(gal.fileWorkingName,'a').close()

    if not gal.readFinishedFiles():
        open(gal.fileFinishedName,'a').close()
#    gal.readLogFile()

    if True:
        p = Pool(processes=12)
        iCombo = np.arange(len(Gaia.pixels))
        random.shuffle(iCombo)
        p.map(processGaia, iCombo)
        p.close()

if __name__ == '__main__':
    main(sys.argv)
