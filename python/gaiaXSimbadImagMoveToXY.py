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


class GaiaXSimbad(object):
    ham = hammer.Hammer()
    inFileNames = []
    keys = []
    keyStr = ''
    releaseTractPatchCombinations = []
    fileWorkingName = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2xSimbad/workinOnFiles.txt'
    fileWorking = None
    fileFinishedName = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2xSimbad/finishedFiles.txt'
    fileFinished = None
    filesFinished = []
    filesWorking = []
    ids = ['source_id']
    logContent = []
    logFileName = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2xSimbad/gaiaXSimbadIMoveToXY.log'

    def __init__(self):
        self.dir = '/Volumes/obiwan/azuri/data/simbad/'
        self.headerFile = os.path.join(self.dir, 'simbad_Imag_logg.csv')

    def openFileWorking(self, flag='a'):
        GaiaXSimbad.fileWorking = open(GaiaXSimbad.fileWorkingName, flag)

    def openFileFinished(self, flag='a'):
        GaiaXSimbad.fileFinished = open(GaiaXSimbad.fileFinishedName, flag)

    def closeFileWorking(self):
        GaiaXSimbad.fileWorking.close()

    def closeFileFinished(self):
        GaiaXSimbad.fileFinished.close()

    def writeToFileWorking(self, text):
        self.openFileWorking()
        GaiaXSimbad.fileWorking.write(text+'\n')
        self.closeFileWorking()

    def writeToFileFinished(self, text):
        self.openFileFinished()
        GaiaXSimbad.fileFinished.write(text+'\n')
        self.closeFileFinished()

    def readFinishedFiles(self):
        if os.path.isfile(GaiaXSimbad.fileFinishedName):
            self.openFileFinished(flag = 'r')
            lines = GaiaXSimbad.fileFinished.readlines()
            self.closeFileFinished()
            for line in lines:
                GaiaXSimbad.filesFinished.append(line[0:line.find(' ')])
            return True
        return False

    def readWorkingFiles(self):
        if os.path.isfile(GaiaXSimbad.fileWorkingName):
            self.openFileWorking(flag = 'r')
            lines = GaiaXSimbad.fileWorking.readlines()
            self.closeFileWorking()
            for line in lines:
                GaiaXSimbad.filesWorking.append(line[0:line.find('\n')])
            return True
        return False

    def readLogFile(self):
        if os.path.isfile(GaiaXSimbad.logFileName):
            logFile = open(GaiaXSimbad.logFileName, 'r')
            lines = logFile.readlines()
            logFile.close()
            for line in lines:
                lineSplit = line.split(' ')
                if lineSplit[0] == 'ran':
                    iIt = lineSplit[4]
                    fName = lineSplit[9]
                    if (fName in GaiaXSimbad.filesWorking) and (fName not in GaiaXSimbad.filesFinished):
                        fPos = -1
                        if len(GaiaXSimbad.logContent) > 0:
                            fNames = [GaiaXSimbad.logContent[i][0] for i in range(len(GaiaXSimbad.logContent))]
                            try:
                                fPos = fNames.index(fName)
                            except:
                                """do nothing"""
                        if fPos < 0:
                            GaiaXSimbad.logContent.append([fName, iIt])
                            fPos = len(GaiaXSimbad.logContent)-1
                        else:
                            GaiaXSimbad.logContent[fPos][1] = iIt
        else:
            GaiaXSimbad.logContent = [['a',-1]]

    def getInFileNames(self):
        if len(GaiaXSimbad.inFileNames) == 0:
            GaiaXSimbad.inFileNames.append(self.dir + ("simbad_Imag_logg.csv"))

    def addXY(self, data):
        long = csvFree.convertStringVectorToDoubleVector(data.getData('l'))
        ind=np.where(np.array(long) < 0.0)[0]
        if len(ind) > 0:
            print('gaiaXSimbadIMoveToXY.addXY: ind(where long < 0) = ',ind)
            STOP
            long[ind]=long[ind] + 360.0

        lati = csvFree.convertStringVectorToDoubleVector(data.getData('b'))
        xys = GaiaXSimbad.ham.lonLatToXY(long, lati)

#        data.addColumn(GaiaXSimbad.ham.getKeyWordHammerX(), xys[0])
#        data.addColumn(GaiaXSimbad.ham.getKeyWordHammerY(), xys[1])

    def getHeader(self):

        GaiaXSimbad.keys = csvFree.readHeader(self.headerFile,',')
#        GaiaXSimbad.keys.append(GaiaXSimbad.ham.getKeyWordHammerX())
#        GaiaXSimbad.keys.append(GaiaXSimbad.ham.getKeyWordHammerY())

        GaiaXSimbad.keyStr = GaiaXSimbad.keys[0]
        for key in GaiaXSimbad.keys[1:]:
            GaiaXSimbad.keyStr += ','+key
        GaiaXSimbad.keyStr += '\n'
        return GaiaXSimbad.keys

    def writeHeaders(self):

        if len(GaiaXSimbad.keys) == 0:
            self.getHeader()

        pixels = GaiaXSimbad.ham.getPixels()
        print('type(GaiaXSimbad.keys) = ',type(GaiaXSimbad.keys),': ',type(GaiaXSimbad.keys[0]))
        print('type(pixels) = ',type(pixels),': ',type(pixels[0]))
        whichone = 'gaiaXSimbadI'
#        whichone = whichone.decode('utf-8')
        print('type(whichone) = ',type(whichone))
        print('type("gaiaXSimbadI") = ',type('gaiaXSimbadI'))
        print('type(False) = ',type(False))
        tempdir = ''
#        tempdir = tempdir.decode('utf-8')
        moveStarsToXY.writeHeaderToOutFiles(GaiaXSimbad.keys,
                                            pixels,
                                            whichone,
                                            False,
                                            tempdir)

    def processGaiaXSimbad(self, iCombo):
        doIt = True
        inputFile = ''

        pixels = GaiaXSimbad.ham.getPixels()

        if doIt:
            timeStart = time.time()
            inputFile = GaiaXSimbad.inFileNames[iCombo]
            if not os.path.isfile(inputFile):
                print("gaiaXSimbadIMoveToXY.processGaiaXSimbad: ERROR: gaiaXSimbadI input file ",inputFile," not found")
                STOP

            data = csvFree.readCSVFile(inputFile)

            # add Hammer x and y
#            self.addXY(data)

            moveStarsToXY.appendCSVDataToXYFiles(data,
                                                 pixels,
                                                 'gaiaXSimbadI',
                                                 GaiaXSimbad.ids,
                                                 False,
                                                 '',
                                                 '')
            timeEnd = time.time()
            duration = timeEnd-timeStart
            print('gaiaXSimbadIMoveToXY.processGaiaXSimbad: ran file <', inputFile,'> in ',duration,' seconds')

            self.writeToFileFinished(inputFile+' done in '+str(duration)+'s')

    #        globallock.release()
def processGaiaXSimbad(iCombo):
    gal = GaiaXSimbad()
    gal.processGaiaXSimbad(iCombo)

def main(argv):
    """Main program.

    Arguments:
    argv -- command line arguments
    """
    gal = GaiaXSimbad()
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
        iCombo = np.arange(len(GaiaXSimbad.inFileNames))
        #gal.processGaiaXSimbad(iCombo[0])
        random.shuffle(iCombo)
        p.map(processGaiaXSimbad, iCombo)
        p.close()

if __name__ == '__main__':
    main(sys.argv)
