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


class GaiaXSDSS(object):
    ham = hammer.Hammer()
    inFileNames = []
    keys = []
    keyStr = ''
    releaseTractPatchCombinations = []
    fileWorkingName = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2distXSDSS12/workinOnFiles.txt'
    fileWorking = None
    fileFinishedName = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2distXSDSS12/finishedFiles.txt'
    fileFinished = None
    filesFinished = []
    filesWorking = []
    ids = ['source_id']
    logContent = []
    logFileName = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2distXSDSS12/gaiaXSDSSMoveToXY.log'
    dir = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2distXSDSS12/'

    def __init__(self):
#        dir = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2distXSDSS12/'
        self.fileNameIn = os.path.join(self.dir, 'GaiaXSDSS_mean_lb.csv')
        self.headerFile = self.fileNameIn
        self.inFileNames = [self.fileNameIn]

    def openFileWorking(self, flag='a'):
        GaiaXSDSS.fileWorking = open(GaiaXSDSS.fileWorkingName, flag)

    def openFileFinished(self, flag='a'):
        GaiaXSDSS.fileFinished = open(GaiaXSDSS.fileFinishedName, flag)

    def closeFileWorking(self):
        GaiaXSDSS.fileWorking.close()

    def closeFileFinished(self):
        GaiaXSDSS.fileFinished.close()

    def writeToFileWorking(self, text):
        self.openFileWorking()
        GaiaXSDSS.fileWorking.write(text+'\n')
        self.closeFileWorking()

    def writeToFileFinished(self, text):
        self.openFileFinished()
        GaiaXSDSS.fileFinished.write(text+'\n')
        self.closeFileFinished()

    def readFinishedFiles(self):
        if os.path.isfile(GaiaXSDSS.fileFinishedName):
            self.openFileFinished(flag = 'r')
            lines = GaiaXSDSS.fileFinished.readlines()
            self.closeFileFinished()
            for line in lines:
                GaiaXSDSS.filesFinished.append(line[0:line.find(' ')])
            return True
        return False

    def readWorkingFiles(self):
        if os.path.isfile(GaiaXSDSS.fileWorkingName):
            self.openFileWorking(flag = 'r')
            lines = GaiaXSDSS.fileWorking.readlines()
            self.closeFileWorking()
            for line in lines:
                GaiaXSDSS.filesWorking.append(line[0:line.find('\n')])
            return True
        return False

    def readLogFile(self):
        if os.path.isfile(GaiaXSDSS.logFileName):
            logFile = open(GaiaXSDSS.logFileName, 'r')
            lines = logFile.readlines()
            logFile.close()
            for line in lines:
                lineSplit = line.split(' ')
                if lineSplit[0] == 'ran':
                    iIt = lineSplit[4]
                    fName = lineSplit[9]
                    if (fName in GaiaXSDSS.filesWorking) and (fName not in GaiaXSDSS.filesFinished):
                        fPos = -1
                        if len(GaiaXSDSS.logContent) > 0:
                            fNames = [GaiaXSDSS.logContent[i][0] for i in range(len(GaiaXSDSS.logContent))]
                            try:
                                fPos = fNames.index(fName)
                            except:
                                """do nothing"""
                        if fPos < 0:
                            GaiaXSDSS.logContent.append([fName, iIt])
                            fPos = len(GaiaXSDSS.logContent)-1
                        else:
                            GaiaXSDSS.logContent[fPos][1] = iIt
        else:
            GaiaXSDSS.logContent = [['a',-1]]

#    def getReleaseTractPatchCombinations(self):
#        if len(GaiaXSDSS.releaseTractPatchCombinations) == 0:
#            for release in np.arange(0, 1, 1):
#                for tract in np.arange(0, 1, 1):
#                    for patch in np.arange(0, 16, 1):
#                        GaiaXSDSS.releaseTractPatchCombinations.append([release, tract, patch])

    def getInFileNames(self):
        return GaiaXSDSS.inFileNames

    def addXY(self, data):
        long = np.array(csvFree.convertStringVectorToDoubleVector(data.getData('l')))
        ind=np.where(long < 0.0)[0]
        if len(ind) > 0:
            print('gaiaXSDSSMoveToXY.addXY: ind(where long < 0) = ',ind)
            STOP
            long[ind]=long[ind] + 360.0

        lati = csvFree.convertStringVectorToDoubleVector(data.getData('b'))
        xys = GaiaXSDSS.ham.lonLatToXY(long, lati)

        data.addColumn(GaiaXSDSS.ham.getKeyWordHammerX(), xys[0])
        data.addColumn(GaiaXSDSS.ham.getKeyWordHammerY(), xys[1])

    def getHeader(self):

        GaiaXSDSS.keys = csvFree.readHeader(self.headerFile)
        GaiaXSDSS.keys.append(GaiaXSDSS.ham.getKeyWordHammerX())
        GaiaXSDSS.keys.append(GaiaXSDSS.ham.getKeyWordHammerY())

        GaiaXSDSS.keyStr = GaiaXSDSS.keys[0]
        for key in GaiaXSDSS.keys[1:]:
            GaiaXSDSS.keyStr += ','+key
        GaiaXSDSS.keyStr += '\n'
        return GaiaXSDSS.keys

    def writeHeaders(self):

        if len(GaiaXSDSS.keys) == 0:
            self.getHeader()

        pixels = GaiaXSDSS.ham.getPixels()
        print('GaiaXSDSS.keys = ',GaiaXSDSS.keys)
        moveStarsToXY.writeHeaderToOutFiles(GaiaXSDSS.keys,
                                            pixels,
                                            'gaiaXSDSS',
                                            False,
                                            os.path.join(GaiaXSDSS.dir,'xy/'))

    def processGaiaXSDSS(self, iCombo):
        doIt = True
        inputFile = ''

        pixels = GaiaXSDSS.ham.getPixels()

        if doIt:
            timeStart = time.time()
            inputFile = self.fileNameIn
            print('working on <'+inputFile+'>')
            if not os.path.isfile(inputFile):
                print("gaiaXSDSSMoveToXY.processGaiaXSDSS: ERROR: gaiaXSDSS input file ",inputFile," not found")
                STOP

            data = csvFree.readCSVFile(inputFile)

            # add Hammer x and y
            self.addXY(data)

            moveStarsToXY.appendCSVDataToXYFiles(data,
                                                 pixels,
                                                 'gaiaXSDSS',
                                                 GaiaXSDSS.ids,
                                                 False,
                                                 'gaiaXSDSS',
                                                 os.path.join(GaiaXSDSS.dir,'xy/'))
            timeEnd = time.time()
            duration = timeEnd-timeStart
            print('gaiaXSDSSMoveToXY.processGaiaXSDSS: ran file <', inputFile,'> in ',duration,' seconds')

            self.writeToFileFinished(inputFile+' done in '+str(duration)+'s')

    #        globallock.release()
def processGaiaXSDSS(iCombo):
    gal = GaiaXSDSS()
    gal.processGaiaXSDSS(iCombo)

def main(argv):
    """Main program.

    Arguments:
    argv -- command line arguments
    """
    gal = GaiaXSDSS()
#    gal.getReleaseTractPatchCombinations()
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
#        p = Pool(processes=1)
#        p.map(processGaiaXSDSS, [0])
#        p.close()
        processGaiaXSDSS(0)

if __name__ == '__main__':
    main(sys.argv)
