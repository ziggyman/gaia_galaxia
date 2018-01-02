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

#globallock = Lock()


class Galaxia(object):
    ham = hammer.Hammer()
    inFileNames = []
    keys = []
    keyStr = ''
    lonLatCombinations = []
    fileWorkingName = '/Volumes/yoda/azuri/data/galaxia/workinOnFiles.txt'
    fileWorking = None
    fileFinishedName = '/Volumes/yoda/azuri/data/galaxia/finishedFiles.txt'
    fileFinished = None
    filesFinished = []
    filesWorking = []
    ids = ['rad', 'hammerX', 'hammerY', 'exbv_solar']
    logContent = []
    logFileName = '/Volumes/yoda/azuri/data/galaxia/galaxiaMoveToXY.log'

    def __init__(self):
        dir = '/Volumes/yoda/azuri/data/galaxia/sdss/'
        self.fileNameIn = os.path.join(dir, 'galaxia_%d_%d.ebf')
        self.headerFile = self.fileNameIn % (-85, -85)

    def openFileWorking(self, flag='a'):
        Galaxia.fileWorking = open(Galaxia.fileWorkingName, flag)

    def openFileFinished(self, flag='a'):
        Galaxia.fileFinished = open(Galaxia.fileFinishedName, flag)

    def closeFileWorking(self):
        Galaxia.fileWorking.close()

    def closeFileFinished(self):
        Galaxia.fileFinished.close()

    def writeToFileWorking(self, text):
        self.openFileWorking()
        Galaxia.fileWorking.write(text+'\n')
        self.closeFileWorking()

    def writeToFileFinished(self, text):
        self.openFileFinished()
        Galaxia.fileFinished.write(text+'\n')
        self.closeFileFinished()

    def readFinishedFiles(self):
        if os.path.isfile(Galaxia.fileFinishedName):
            self.openFileFinished(flag = 'r')
            lines = Galaxia.fileFinished.readlines()
            self.closeFileFinished()
            for line in lines:
                Galaxia.filesFinished.append(line[0:line.find(' ')])
            return True
        return False

    def readWorkingFiles(self):
        if os.path.isfile(Galaxia.fileWorkingName):
            self.openFileWorking(flag = 'r')
            lines = Galaxia.fileWorking.readlines()
            self.closeFileWorking()
            for line in lines:
                Galaxia.filesWorking.append(line[0:line.find('\n')])
            return True
        return False

    def readLogFile(self):
        if os.path.isfile(Galaxia.logFileName):
            logFile = open(Galaxia.logFileName, 'r')
            lines = logFile.readlines()
            logFile.close()
            for line in lines:
                lineSplit = line.split(' ')
                if lineSplit[0] == 'ran':
                    iIt = lineSplit[4]
                    fName = lineSplit[9]
#                    if fName == '/Volumes/yoda/azuri/data/galaxia/sdss/galaxia_-25_-5.ebf':
#                        print 'fName = <',fName,'>: iIt read = ',iIt
                    if (fName in Galaxia.filesWorking) and (fName not in Galaxia.filesFinished):
#                        if fName == '/Volumes/yoda/azuri/data/galaxia/sdss/galaxia_-25_-5.ebf':
#                            print 'file <',fName,'> found in filesWorking but not in filesFinished'
                        fPos = -1
                        if len(Galaxia.logContent) > 0:
                            fNames = [Galaxia.logContent[i][0] for i in range(len(Galaxia.logContent))]
                            try:
                                fPos = fNames.index(fName)
#                                if fName == '/Volumes/yoda/azuri/data/galaxia/sdss/galaxia_-25_-5.ebf':
#                                    print 'file <',fName,'> found in logContent: fPos = ',fPos
                            except:
                                """do nothing"""
#                                if fName == '/Volumes/yoda/azuri/data/galaxia/sdss/galaxia_-25_-5.ebf':
#                                    print 'file <',fName,'> NOT found in logContent'
                        if fPos < 0:
                            Galaxia.logContent.append([fName, iIt])
                            fPos = len(Galaxia.logContent)-1
                        else:
                            Galaxia.logContent[fPos][1] = iIt
 #                       if fName == '/Volumes/yoda/azuri/data/galaxia/sdss/galaxia_-25_-5.ebf':
 #                           print 'Galaxia.logContent[',fPos,'][:] = ',Galaxia.logContent[fPos]
 #           print 'Galaxia.logContent = ',len(Galaxia.logContent),': ',Galaxia.logContent
        else:
            Galaxia.logContent = [['a',-1]]

    def getLonLatCombinations(self):
        if len(Galaxia.lonLatCombinations) == 0:
            for lon in np.arange(-175, 180, 10):
                for lat in np.arange(-85, 90, 10):
                    Galaxia.lonLatCombinations.append([lon, lat])
#                    print ('lon = Galaxia.lonLatCombinations[',len(Galaxia.lonLatCombinations)-1,'][0] = ',
#                           Galaxia.lonLatCombinations[len(Galaxia.lonLatCombinations)-1][0],', ',
#                           'lat = Galaxia.lonLatCombinations[',len(Galaxia.lonLatCombinations)-1,'][1] = ',
#                           Galaxia.lonLatCombinations[len(Galaxia.lonLatCombinations)-1][1])

    def getInFileNames(self):
        if len(Galaxia.lonLatCombinations) == 0:
            print 'ERROR: run Galaxia.getLonLatCombinations() first'
            STOP
        for combo in Galaxia.lonLatCombinations:
            Galaxia.inFileNames.append(self.fileNameIn % (combo[0], combo[1]))

    def getHeader(self):

#        print 'ebf.info(',self.headerFile,')'
#        ebf.info(self.headerFile)
#        print ' '

        data = ebf.iterate(self.headerFile, '/px+', 1)
        for it in data:
            it[Galaxia.ham.getKeyWordHammerX()] = np.ndarray(len(it['px']), dtype=np.float32)
            it[Galaxia.ham.getKeyWordHammerY()] = np.ndarray(len(it['px']), dtype=np.float32)

            for iStar in range(len(it['px'])):
                xy = Galaxia.ham.lonLatToXY(it['glon'][iStar], it['glat'][iStar])
                it[Galaxia.ham.getKeyWordHammerX()][iStar] = xy.x
                it[Galaxia.ham.getKeyWordHammerY()][iStar] = xy.y

            gxutil.append_pm(it)

            """convert absolute magnitudes to apparent ones"""
            gxutil.abs2app(it,corr=True)

            Galaxia.keys = list(it.keys())
#            print 'Galaxia.keys = ',Galaxia.keys
            break

        Galaxia.keyStr = Galaxia.keys[0]
        for key in Galaxia.keys[1:]:
            Galaxia.keyStr += ','+key
        Galaxia.keyStr += '\n'
#        print 'Galaxia.keyStr = ',Galaxia.keyStr
        return Galaxia.keys

    def getCSVData(self, data, window, inputFile, iIt):
        csvData = galcomp.CSVData()

        """create CSVData.header"""
        if len(Galaxia.keys) == 0:
            self.getHeader()
        csvData.header = Galaxia.keys

        lons = data['glon']
        ind=np.where(lons < 0.0)[0]
        lons[ind]=lons[ind] + 360.0
        lats = data['glat']

        dataArr = []

#        print 'Galaxia.keys = ',len(Galaxia.keys),': ',Galaxia.keys
        nStarsOut = 0
        for iStar in range(len(data['px'])):
            lon = lons[iStar]
            lat = lats[iStar]
#                        print 'iStar = ',iStar,': lon = ',lon,', lat = ',lat
            if ((lon >= window.xLow)
                and (lon < window.xHigh)
                and (lat >= window.yLow)
                and (lat < window.yHigh)):

                outVec = []
                for iDat in range(len(Galaxia.keys)):
                    dataVec = data[Galaxia.keys[iDat]]
#                    print 'key = ',Galaxia.keys[iDat],': dataVec = ',len(dataVec),': ',dataVec
                    outVec.append(str(dataVec[iStar]))
#                    print 'outVec[',len(outVec)-1,'] = ',outVec[len(outVec)-1]
                if len(outVec) != len(Galaxia.keys):
                    print 'getCSVData: ERROR: len(outVec)(=',len(outVec),') != len(Galaxia.keys)(=',len(Galaxia.keys),')'
                    STOP
                dataArr.append(outVec)
                nStarsOut += 1

        print 'file <',inputFile,'>: window: [',window.xLow,', ',window.xHigh,' : ',window.yLow,', ',window.yHigh,']: iIt = ',iIt,': nStarsOut = ',nStarsOut
        csvData.setData(dataArr)

        if csvData.size() != nStarsOut:
            print 'getCSVData: ERROR: csvData.size()(=',csvData.size(),') != nStarsOut(=',nStarsOut,')'
            STOP
        if len(csvData.data[0]) != len(Galaxia.keys):
            print 'getCSVData: ERROR: len(csvData.data[0])(=',len(csvData.data[0]),') != len(Galaxia.keys)(=',len(Galaxia.keys),')'
            STOP
        return csvData

    def addXYandPMandAbs2App(self, data):
        data[Galaxia.ham.getKeyWordHammerX()] = np.ndarray(len(data['px']), dtype=np.float32)
        data[Galaxia.ham.getKeyWordHammerY()] = np.ndarray(len(data['px']), dtype=np.float32)

        long = data['glon']
        ind=np.where(long < 0.0)[0]
        long[ind]=long[ind] + 360.0

        lati = data['glat']
        xys = Galaxia.ham.lonLatToXY(long, lati)
#                    print 'xys[0] = ',xys[0]
        data[Galaxia.ham.getKeyWordHammerX()] = xys[0]
        data[Galaxia.ham.getKeyWordHammerY()] = xys[1]

        gxutil.append_pm(data)

        """convert absolute magnitudes to apparent ones"""
        gxutil.abs2app(data,corr=True)

    def writeHeaders(self):

        if len(Galaxia.keys) == 0:
            self.getHeader()

        pixels = Galaxia.ham.getPixels()
        moveStarsToXY.writeHeaderToOutFiles(Galaxia.keys,
                                            pixels,
                                            'galaxia',
                                            False)

    def processGalaxia(self, iCombo):
#        print 'processGalaxia started'
#        print 'Galaxia.keys = ',Galaxia.keys
#        print 'Galaxia.keyStr = ',Galaxia.keyStr
#        print 'self.fileNameIn = ',self.fileNameIn
        doIt = True
        inputFile = ''

        pixels = Galaxia.ham.getPixels()
#        nPix = len(pixels)

        if doIt:
            cache = 1000000
            lon = Galaxia.lonLatCombinations[iCombo][0]
            lat = Galaxia.lonLatCombinations[iCombo][1]
#            print 'lon = ',lon,', lat = ',lat
            timeStart = time.time()
            inputFile = self.fileNameIn % (lon, lat)
            if inputFile not in Galaxia.filesFinished:
                fPos = -1
                iterationsDone = -2
                try:
                    fPos = [Galaxia.logContent[i][0] for i in range(len(Galaxia.logContent))].index(inputFile)
                except:
                    """do nothing"""
                if fPos > -1:
                    print "inputFile = <", inputFile, "> found in Galaxia.logContent"
                    iterationsDone = int(Galaxia.logContent[fPos][1])
                else:
                    print "inputFile = <", inputFile, "> NOT found in Galaxia.logContent"
                    self.writeToFileWorking(inputFile)
                if not os.path.isfile(inputFile):
                    print "ERROR: galaxia input file ",inputFile," not found"
                    STOP

                lonStart = lon-5
                lonEnd = lon+5
                if (lon < 0):
                    lonStart += 360.0
                    lonEnd += 360.0
                latStart = lat-5
                latEnd = lat+5
    #               print 'lonStart = ',lonStart,', lonEnd = ',lonEnd,', latStart = ',latStart,', latEnd = ',latEnd

    #                openFiles = []
    #                openFileNames = []
                nLines = len(ebf.read(inputFile, '/px'))

                data = ebf.iterate(inputFile, '/px+', cache)
    #                nStarsWritten = 0

                iIt = 0
                nLinesRead = 0;
                for it in data:
                    nLinesRead += cache
                    if iIt > iterationsDone:
                        print 'iIt = ',iIt,' > iterationsDone = ',iterationsDone
                        timeStartIt = time.time()

                        self.addXYandPMandAbs2App(it)

#                        keys = list(it.keys())
#
#                        keyStrTemp = keys[0]
#                        for key in keys[1:]:
#                            keyStrTemp += ','+key
#                        keyStrTemp += '\n'
#        #                    print 'keyStrTemp = ',keyStrTemp
#                        if Galaxia.keyStr != keyStrTemp:
#                            print 'Galaxia.keyStr = ',Galaxia.keyStr
#                            print 'keyStrTemp = ',keyStrTemp
#                            print "ERROR: keyStrings don't match!"
#                            STOP

                        window = hammer.Pixel()
                        window.xLow = lonStart
                        window.xHigh = lonEnd
                        window.yLow = latStart
                        window.yHigh = latEnd

                        csvData = self.getCSVData(it, window, inputFile, iIt)
                        doFind = False
                        if iIt == (iterationsDone+1):
                            doFind = True
                            print 'setting doFind to True'
                        moveStarsToXY.appendCSVDataToXYFiles(csvData,
                                                             pixels,
                                                             'galaxia',
                                                             Galaxia.ids,
                                                             doFind)
                        timeEndIt = time.time()
                        timeEnd = time.time()
                        duration = timeEnd-timeStart
                        print 'ran iIt = ',iIt,' for file <', inputFile,'> in ',timeEndIt-timeStartIt,' seconds: ',nLinesRead * 100.0 / nLines,' % done in ',duration,' seconds'

#                        STOP
                    else:
                        print 'already did iteration iIt=',iIt
                    iIt += 1
                timeEnd = time.time()
                duration = timeEnd-timeStart
                print 'ran file <',inputFile,'> in ',duration,' s'
                self.writeToFileFinished(inputFile+' done in '+str(duration)+'s')
            else:
                print 'file <',inputFile,'> already finished'
            ebf.clearEbfMap()
#                STOP

    #        globallock.release()
def processGalaxia(iCombo):
    gal = Galaxia()
    gal.processGalaxia(iCombo)

def main(argv):
    """Main program.

    Arguments:
    argv -- command line arguments
    """
    gal = Galaxia()
    gal.getLonLatCombinations()
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

    if True:
        p = Pool(processes=8)
    #    lon = np.arange(-175, 178, 10)
        iCombo = np.arange(len(Galaxia.lonLatCombinations))
        random.shuffle(iCombo)
        p.map(processGalaxia, iCombo)
    #    print 'starting processGalaxia '
        p.close()
    else:
        found = False
        for iCombo in range(len(Galaxia.lonLatCombinations)):
            combo = Galaxia.lonLatCombinations[iCombo]
            if ((combo[0] == -25)
                and (combo[1] == -5)):
                found = True
                break
        if found:
            gal.processGalaxia(iCombo)
        else:
            print 'ERROR: combination(lon=-25, lat=-5) not found in Galaxia.lonLatCombinations'

if __name__ == '__main__':
    main(sys.argv)
