#! /usr/bin/env python

import ebf
import gxutil
from multiprocessing import Pool
import os
import sys
import time
import numpy as np

import galcomp
import hammer
import moveStarsToXY

#globallock = Lock()

class Galaxia(object):
    ham = hammer.Hammer()
    outFileNames = []
    keys = []
    keyStr = ''

    def __init__(self):
        dir = '/Volumes/yoda/azuri/data/galaxia/sdss/'
        self.outputDir = '/Volumes/yoda/azuri/data/galaxia/xy/'
        self.fileNameIn = os.path.join(dir, 'galaxia_%d_%d.ebf')
        self.fileNameOut = os.path.join(self.outputDir,'galaxia_%0.6f-%0.6f_%0.6f-%0.6f.csv')
        self.headerFile = self.fileNameIn % (-85, -85)

    def getHeader(self):

        print 'ebf.info(',self.headerFile,')'
        ebf.info(self.headerFile)
        print ' '

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
            print 'Galaxia.keys = ',Galaxia.keys
            break

        Galaxia.keyStr = Galaxia.keys[0]
        for key in Galaxia.keys[1:]:
            Galaxia.keyStr += ','+key
        Galaxia.keyStr += '\n'
        print 'Galaxia.keyStr = ',Galaxia.keyStr
        return Galaxia.keys

    def getCSVData(self, data, window):
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

        print 'Galaxia.keys = ',len(Galaxia.keys),': ',Galaxia.keys
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

        print 'nStarsOut = ',nStarsOut
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

#        Galaxia.keyStr = Galaxia.keys[0]
#        for key in Galaxia.keys[1:]:
#            Galaxia.keyStr += ','+key
#        Galaxia.keyStr += '\n'
#        print 'Galaxia.keyStr = ',Galaxia.keyStr

        pixels = Galaxia.ham.getPixels()
#        nPix = len(pixels)
#        Galaxia.outFileNames = [None] * nPix
#        for iPix in range(nPix):
#            Galaxia.outFileNames[iPix] = self.fileNameOut % (pixels[iPix].xLow,
#                                                             pixels[iPix].xHigh,
#                                                             pixels[iPix].yLow,
#                                                             pixels[iPix].yHigh)
#    #        print 'Galaxia.outFileNames[',iPix,'] = ',Galaxia.outFileNames[iPix]
#            """write headers"""
#            with open(Galaxia.outFileNames[iPix],'w') as csvFileOut:
#                csvFileOut.write(Galaxia.keyStr)
        moveStarsToXY.writeHeaderToOutFiles(Galaxia.keys,
                                            pixels,
                                            'galaxia',
                                            False)

    def processGalaxia(self):
        print 'processGalaxia started'
        print 'Galaxia.outFileNames = ',Galaxia.outFileNames
        print 'Galaxia.keys = ',Galaxia.keys
        print 'Galaxia.keyStr = ',Galaxia.keyStr
        print 'self.fileNameIn = ',self.fileNameIn
        print 'self.fileNameOut = ',self.fileNameOut
        doIt = True
        inputFile = ''

        pixels = Galaxia.ham.getPixels()
#        nPix = len(pixels)

        if doIt:
            cache = 10000000
            for lon in np.arange(-175, 178, 10):
                for lat in np.arange(-85, 90, 10):
                    timeStart = time.time()
                    inputFile = self.fileNameIn % (lon, lat)
                    print "inputFile = <", inputFile, ">"
                    if os.path.isfile(inputFile):
                        print "galaxia input file ",inputFile," found => moving stars to xy"
                    else:
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

                    data = ebf.iterate(inputFile, '/px+', cache)
    #                nStarsWritten = 0

                    for it in data:

    #                    long = it['glon']
    #                    ind=np.where(long < 0.0)[0]
    #                    long[ind]=long[ind] + 360.0
    #
    #                    lati = it['glat']

                        self.addXYandPMandAbs2App(it)

                        keys = list(it.keys())

                        keyStrTemp = keys[0]
                        for key in keys[1:]:
                            keyStrTemp += ','+key
                        keyStrTemp += '\n'
        #                    print 'keyStrTemp = ',keyStrTemp
                        if Galaxia.keyStr != keyStrTemp:
                            print 'Galaxia.keyStr = ',Galaxia.keyStr
                            print 'keyStrTemp = ',keyStrTemp
                            print "ERROR: keyStrings don't match!"
                            STOP

                        window = hammer.Pixel()
                        window.xLow = lonStart
                        window.xHigh = lonEnd
                        window.yLow = latStart
                        window.yHigh = latEnd

                        csvData = self.getCSVData(it, window)
                        moveStarsToXY.appendCSVDataToXYFiles(csvData,
                                                             pixels,
                                                             'galaxia')
    #                    for iStar in range(len(it['px'])):
    #                        longi = long[iStar]
    #                        latit = lati[iStar]
    #    #                        print 'iStar = ',iStar,': longi = ',longi,', latit = ',latit
    #                        if (longi >= lonStart) and (longi < lonEnd) and (latit >= latStart) and (latit < latEnd):
    #                            pixFound = False
    #                            xy = hammer.XY(it[Galaxia.ham.getKeyWordHammerX()][iStar],
    #                                           it[Galaxia.ham.getKeyWordHammerY()][iStar])
    ##                            print 'iStar = ',iStar,': xy = ',xy
    #                            for iPix in range(len(pixels)):
    #                                if pixels[iPix].isInside(xy):
    #                                    outFileName = Galaxia.outFileNames[iPix]
    #                                    pixFound = True
    #
    #                                    if outFileName not in openFileNames:
    #                                        openFileNames.append(outFileName)
    #                                        fn = open(outFileName,'a')
    #                                        print 'opened file name <',outFileName,'>'
    #                                        openFiles.append(fn)
    #
    #                                    outString = str(it[keys[0]][iStar])
    #                                    for key in Galaxia.keys[1:]:
    #                                        outString += ','+str(it[key][iStar])
    #                                    #print 'outString = <',outString,'>'
    #                                    openFiles[openFileNames.index(outFileName)].write(outString+'\n')
    #                                    nStarsWritten += 1
    #                            if not pixFound:
    #                                print 'ERROR: no pixel found for star (iStar) = ',iStar
    #                                STOP
    #                print nStarsWritten,' stars written'
    #                print 'opened ',len(openFiles),' files, closing them now'
    #                for file in openFiles:
    #                    file.close()
                    timeEnd = time.time()
                    print 'ran file <',inputFile,'> in ',timeEnd-timeStart,' s'
#                STOP

    #        globallock.release()
#def processGalaxia(lon):
#    gal = Galaxia()
#    gal.processGalaxia(lon)

def main(argv):
    """Main program.

    Arguments:
    argv -- command line arguments
    """
    gal = Galaxia()
    gal.getHeader()
    gal.writeHeaders()

#    p = Pool(processes=1)
#    lon = np.arange(-175, 178, 10)
#    lon = np.arange(5, 360, 10)
#    print 'lon = ',lon
#    p.map(processGalaxia, lon)
#    print 'starting processGalaxia '
    gal.processGalaxia()
#    p.close()

if __name__ == '__main__':
    main(sys.argv)
