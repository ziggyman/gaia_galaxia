#! /usr/bin/env python

from multiprocessing import Pool
import os
import sys
import time
import numpy as np
import random
import subprocess

import csvData# for CSVData as a return type
import csvFree
import hammer
import moveStarsToXY

#globallock = Lock()


class GaiaDR2(object):
    ham = hammer.Hammer()
    inFileNames = []
    keys = []
    keyStr = ''
    combinations = []
    fileWorkingName = '/Volumes/obiwan/azuri/data/gaia/dr2/workinOnFiles.txt'
    fileWorking = None
    fileFinishedName = '/Volumes/obiwan/azuri/data/gaia/dr2/finishedFiles.txt'
    fileFinished = None
    filesFinished = []
    filesWorking = []
    ids = ['source_id']
    headerFile = ''
    logContent = []
    logFileName = '/Volumes/obiwan/azuri/data/gaia/dr2/gaiaDR2MoveToXY.log'

    def __init__(self):
        dir = '/Volumes/obiwan/azuri/data/gaia/dr2/cdn.gea.esac.esa.int/Gaia/gdr2/gaia_source/csv'
        self.fileNameIn = os.path.join(dir, 'GaiaSource_%s_%s.csv')

    def openFileWorking(self, flag='a'):
        GaiaDR2.fileWorking = open(GaiaDR2.fileWorkingName, flag)

    def openFileFinished(self, flag='a'):
        GaiaDR2.fileFinished = open(GaiaDR2.fileFinishedName, flag)

    def closeFileWorking(self):
        GaiaDR2.fileWorking.close()

    def closeFileFinished(self):
        GaiaDR2.fileFinished.close()

    def writeToFileWorking(self, text):
        self.openFileWorking()
        GaiaDR2.fileWorking.write(text+'\n')
        self.closeFileWorking()

    def writeToFileFinished(self, text):
        self.openFileFinished()
        GaiaDR2.fileFinished.write(text+'\n')
        self.closeFileFinished()

    def readFinishedFiles(self):
        if os.path.isfile(GaiaDR2.fileFinishedName):
            self.openFileFinished(flag = 'r')
            lines = GaiaDR2.fileFinished.readlines()
            self.closeFileFinished()
            for line in lines:
                GaiaDR2.filesFinished.append(line[0:line.find(' ')])
            return True
        return False

    def readWorkingFiles(self):
        if os.path.isfile(GaiaDR2.fileWorkingName):
            self.openFileWorking(flag = 'r')
            lines = GaiaDR2.fileWorking.readlines()
            self.closeFileWorking()
            for line in lines:
                GaiaDR2.filesWorking.append(line[0:line.find('\n')])
            return True
        return False

    def readLogFile(self):
        if os.path.isfile(GaiaDR2.logFileName):
            logFile = open(GaiaDR2.logFileName, 'r')
            lines = logFile.readlines()
            logFile.close()
            for line in lines:
                lineSplit = line.split(' ')
                if lineSplit[0] == 'ran':
                    iIt = lineSplit[4]
                    fName = lineSplit[9]
                    if (fName in GaiaDR2.filesWorking) and (fName not in GaiaDR2.filesFinished):
                        fPos = -1
                        if len(GaiaDR2.logContent) > 0:
                            fNames = [GaiaDR2.logContent[i][0] for i in range(len(GaiaDR2.logContent))]
                            try:
                                fPos = fNames.index(fName)
                            except:
                                """do nothing"""
                        if fPos < 0:
                            GaiaDR2.logContent.append([fName, iIt])
                            fPos = len(GaiaDR2.logContent)-1
                        else:
                            GaiaDR2.logContent[fPos][1] = iIt
        else:
            GaiaDR2.logContent = [['a',-1]]

    def getCombinations(self):
        if len(GaiaDR2.combinations) == 0:
            inFile = '/Volumes/obiwan/azuri/data/gaia/dr2/cdn.gea.esac.esa.int/Gaia/gdr2/gaia_source/csv/csvFiles.list'
            with open(inFile) as f:
                content = f.readlines()
            # remove whitespace characters like `\n` at the end of each line
            content = [x.strip() for x in content]
            for x in content:
                comA = x[x.rfind('e_')+2:x.rfind('_')]
                comB = x[x.rfind('_')+1:x.rfind('.csv')]
                GaiaDR2.combinations.append([comA, comB])

    def getInFileNames(self):
        if len(GaiaDR2.combinations) == 0:
            print 'ERROR: run GaiaDR2.getCombinations() first'
            STOP
        for combo in GaiaDR2.combinations:
            GaiaDR2.inFileNames.append(self.fileNameIn % (combo[0], combo[1]))

    def addXY(self, data):
        long = csvFree.convertStringVectorToDoubleVector(data.getData('l'))
        ind=np.where(long < 0.0)[0]
        if len(ind) > 0:
            print 'gaiaDR2MoveToXY.addXY: ind(where long < 0) = ',ind
            STOP
            long[ind]=long[ind] + 360.0

        lati = csvFree.convertStringVectorToDoubleVector(data.getData('b'))
        xys = GaiaDR2.ham.lonLatToXY(long, lati)

        data.addColumn(GaiaDR2.ham.getKeyWordHammerX(), xys[0])
        data.addColumn(GaiaDR2.ham.getKeyWordHammerY(), xys[1])

    def getHeader(self):

        GaiaDR2.keys = csvFree.readHeader(self.headerFile)
        GaiaDR2.keys.append(GaiaDR2.ham.getKeyWordHammerX())
        GaiaDR2.keys.append(GaiaDR2.ham.getKeyWordHammerY())

        GaiaDR2.keyStr = GaiaDR2.keys[0]
        for key in GaiaDR2.keys[1:]:
            GaiaDR2.keyStr += ','+key
        GaiaDR2.keyStr += '\n'
        return GaiaDR2.keys

    def writeHeaders(self):

        if len(GaiaDR2.keys) == 0:
            self.getHeader()

        pixels = GaiaDR2.ham.getPixels()
        moveStarsToXY.writeHeaderToOutFiles(GaiaDR2.keys,
                                            pixels,
                                            'gaiaDR2',
                                            False,
                                            '')

    def processGaiaDR2(self, iCombo):
        doIt = True
        inputFile = ''

        pixels = GaiaDR2.ham.getPixels()

        if doIt:
            timeStart = time.time()

            inputFile = self.fileNameIn % (GaiaDR2.combinations[iCombo][0], GaiaDR2.combinations[iCombo][1])
            subprocessResult = subprocess.check_output(['gunzip', inputFile+'.gz'])
            print('subprocessResult = ',subprocessResult)
            if not os.path.isfile(inputFile):
                print "gaiaDR2MoveToXY.processGaiaDR2: ERROR: gaiaDR2 input file ",inputFile," not found"
                STOP

            data = csvFree.readCSVFile(inputFile)

            # add Hammer x and y
            self.addXY(data)

            moveStarsToXY.appendCSVDataToXYFiles(data,
                                                 pixels,
                                                 'gaiaDR2',
                                                 GaiaDR2.ids,
                                                 False,
                                                 '',
                                                 '')

            subprocessResult = subprocess.check_output(['gzip', inputFile])

            timeEnd = time.time()
            duration = timeEnd-timeStart
            print 'gaiaDR2MoveToXY.processGaiaDR2: ran file <', inputFile,'> in ',duration,' seconds'

            self.writeToFileFinished(inputFile+' done in '+str(duration)+'s')

    #        globallock.release()
def processGaiaDR2(iCombo):
    gal = GaiaDR2()
    gal.processGaiaDR2(iCombo)

def main(argv):
    """Main program.

    Arguments:
    argv -- command line arguments
    """
    gal = GaiaDR2()
    gal.getCombinations()
    gal.getInFileNames()
    gal.headerFile = gal.fileNameIn % (gal.combinations[0][0], gal.combinations[0][1])
    print('gal.combinations[0][0] = <'+gal.combinations[0][0]+'>, gal.combinations[0][1] = <'+gal.combinations[0][1]+'> => gal.headerFile = <'+gal.headerFile+'>')
    subprocessResult = subprocess.check_output(['gunzip', gal.headerFile+'.gz'])
    gal.getHeader()
    subprocessResult = subprocess.check_output(['gzip', gal.headerFile])
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
        iCombo = np.arange(len(GaiaDR2.combinations))
        random.shuffle(iCombo)
        p.map(processGaiaDR2, iCombo)
        p.close()

if __name__ == '__main__':
    main(sys.argv)
