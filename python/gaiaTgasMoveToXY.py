#! /usr/bin/env python

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

#globallock = Lock()


class GaiaTgas(object):
    ham = hammer.Hammer()
    inFileNames = []
    keys = []
    keyStr = ''
    releaseTractPatchCombinations = []
    fileWorkingName = '/Volumes/yoda/azuri/data/gaia-tgas/workinOnFiles.txt'
    fileWorking = None
    fileFinishedName = '/Volumes/yoda/azuri/data/gaia-tgas/finishedFiles.txt'
    fileFinished = None
    filesFinished = []
    filesWorking = []
    ids = ['source_id']
    logContent = []
    logFileName = '/Volumes/yoda/azuri/data/gaia-tgas/gaiaTgasMoveToXY.log'

    def __init__(self):
        dir = '/Volumes/yoda/azuri/data/gaia-tgas/'
        self.fileNameIn = os.path.join(dir, 'TgasSource_%03d-%03d-%03d.csv')
        self.headerFile = self.fileNameIn % (0, 0, 0)

    def openFileWorking(self, flag='a'):
        GaiaTgas.fileWorking = open(GaiaTgas.fileWorkingName, flag)

    def openFileFinished(self, flag='a'):
        GaiaTgas.fileFinished = open(GaiaTgas.fileFinishedName, flag)

    def closeFileWorking(self):
        GaiaTgas.fileWorking.close()

    def closeFileFinished(self):
        GaiaTgas.fileFinished.close()

    def writeToFileWorking(self, text):
        self.openFileWorking()
        GaiaTgas.fileWorking.write(text+'\n')
        self.closeFileWorking()

    def writeToFileFinished(self, text):
        self.openFileFinished()
        GaiaTgas.fileFinished.write(text+'\n')
        self.closeFileFinished()

    def readFinishedFiles(self):
        if os.path.isfile(GaiaTgas.fileFinishedName):
            self.openFileFinished(flag = 'r')
            lines = GaiaTgas.fileFinished.readlines()
            self.closeFileFinished()
            for line in lines:
                GaiaTgas.filesFinished.append(line[0:line.find(' ')])
            return True
        return False

    def readWorkingFiles(self):
        if os.path.isfile(GaiaTgas.fileWorkingName):
            self.openFileWorking(flag = 'r')
            lines = GaiaTgas.fileWorking.readlines()
            self.closeFileWorking()
            for line in lines:
                GaiaTgas.filesWorking.append(line[0:line.find('\n')])
            return True
        return False

    def readLogFile(self):
        if os.path.isfile(GaiaTgas.logFileName):
            logFile = open(GaiaTgas.logFileName, 'r')
            lines = logFile.readlines()
            logFile.close()
            for line in lines:
                lineSplit = line.split(' ')
                if lineSplit[0] == 'ran':
                    iIt = lineSplit[4]
                    fName = lineSplit[9]
                    if (fName in GaiaTgas.filesWorking) and (fName not in GaiaTgas.filesFinished):
                        fPos = -1
                        if len(GaiaTgas.logContent) > 0:
                            fNames = [GaiaTgas.logContent[i][0] for i in range(len(GaiaTgas.logContent))]
                            try:
                                fPos = fNames.index(fName)
                            except:
                                """do nothing"""
                        if fPos < 0:
                            GaiaTgas.logContent.append([fName, iIt])
                            fPos = len(GaiaTgas.logContent)-1
                        else:
                            GaiaTgas.logContent[fPos][1] = iIt
        else:
            GaiaTgas.logContent = [['a',-1]]

    def getReleaseTractPatchCombinations(self):
        if len(GaiaTgas.releaseTractPatchCombinations) == 0:
            for release in np.arange(0, 1, 1):
                for tract in np.arange(0, 1, 1):
                    for patch in np.arange(0, 16, 1):
                        GaiaTgas.releaseTractPatchCombinations.append([release, tract, patch])

    def getInFileNames(self):
        if len(GaiaTgas.releaseTractPatchCombinations) == 0:
            print 'ERROR: run GaiaTgas.getReleaseTractPatchCombinations() first'
            STOP
        for combo in GaiaTgas.releaseTractPatchCombinations:
            GaiaTgas.inFileNames.append(self.fileNameIn % (combo[0], combo[1], combo[2]))

    def addXY(self, data):
        long = csvFree.convertStringVectorToDoubleVector(data.getData('l'))
        ind=np.where(long < 0.0)[0]
        if len(ind) > 0:
            print 'gaiaTgasMoveToXY.addXY: ind(where long < 0) = ',ind
            STOP
            long[ind]=long[ind] + 360.0

        lati = csvFree.convertStringVectorToDoubleVector(data.getData('b'))
        xys = GaiaTgas.ham.lonLatToXY(long, lati)

        data.addColumn(GaiaTgas.ham.getKeyWordHammerX(), xys[0])
        data.addColumn(GaiaTgas.ham.getKeyWordHammerY(), xys[1])

    def getHeader(self):

        GaiaTgas.keys = csvFree.readHeader(self.headerFile)
        GaiaTgas.keys.append(GaiaTgas.ham.getKeyWordHammerX())
        GaiaTgas.keys.append(GaiaTgas.ham.getKeyWordHammerY())

        GaiaTgas.keyStr = GaiaTgas.keys[0]
        for key in GaiaTgas.keys[1:]:
            GaiaTgas.keyStr += ','+key
        GaiaTgas.keyStr += '\n'
        return GaiaTgas.keys

    def writeHeaders(self):

        if len(GaiaTgas.keys) == 0:
            self.getHeader()

        pixels = GaiaTgas.ham.getPixels()
        moveStarsToXY.writeHeaderToOutFiles(GaiaTgas.keys,
                                            pixels,
                                            'gaiaTgas',
                                            False)

    def processGaiaTgas(self, iCombo):
        doIt = True
        inputFile = ''

        pixels = GaiaTgas.ham.getPixels()

        if doIt:
            release = GaiaTgas.releaseTractPatchCombinations[iCombo][0]
            tract = GaiaTgas.releaseTractPatchCombinations[iCombo][1]
            patch = GaiaTgas.releaseTractPatchCombinations[iCombo][2]
            timeStart = time.time()
            inputFile = self.fileNameIn % (release, tract, patch)
            if not os.path.isfile(inputFile):
                print "gaiaTgasMoveToXY.processGaiaTgas: ERROR: gaiaTgas input file ",inputFile," not found"
                STOP

            data = csvFree.readCSVFile(inputFile)

            # add Hammer x and y
            self.addXY(data)

            moveStarsToXY.appendCSVDataToXYFiles(data,
                                                 pixels,
                                                 'gaiaTgas',
                                                 GaiaTgas.ids,
                                                 False)
            timeEnd = time.time()
            duration = timeEnd-timeStart
            print 'gaiaTgasMoveToXY.processGaiaTgas: ran file <', inputFile,'> in ',duration,' seconds'

            self.writeToFileFinished(inputFile+' done in '+str(duration)+'s')

    #        globallock.release()
def processGaiaTgas(iCombo):
    gal = GaiaTgas()
    gal.processGaiaTgas(iCombo)

def main(argv):
    """Main program.

    Arguments:
    argv -- command line arguments
    """
    gal = GaiaTgas()
    gal.getReleaseTractPatchCombinations()
    gal.getInFileNames()
    gal.getHeader()
    gal.writeHeaders()
    if not gal.readWorkingFiles():
        gal.openFileWorking('w')
        gal.closeFileWorking()
    if not gal.readFinishedFiles():
        gal.openFileFinished('w')
        gal.closeFileFinished()
    gal.readLogFile()

    folder = '/var/lock'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

    if True:
        p = Pool(processes=16)
        iCombo = np.arange(len(GaiaTgas.releaseTractPatchCombinations))
        random.shuffle(iCombo)
        p.map(processGaiaTgas, iCombo)
        p.close()

if __name__ == '__main__':
    main(sys.argv)
