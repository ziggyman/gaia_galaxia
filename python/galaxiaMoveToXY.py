#! /usr/bin/env python

import ebf
import gxutil
from multiprocessing import Pool
import os
import sys
import time
import numpy as np
import hammer

#globallock = Lock()

class Galaxia(object):
    ham = hammer.Hammer()
    outFileNames = []
    keys = []
    keyStr = ''

    def __init__(self):
        dir = '/Volumes/yoda/azuri/data/galaxia/sdss/'
        outputDir = '/Volumes/yoda/azuri/data/galaxia/xy/'
        self.fileNameIn = os.path.join(dir, 'galaxia_%d_%d.ebf')
        self.fileNameOut = os.path.join(outputDir,'galaxia_%0.6f-%0.6f_%0.6f-%0.6f.csv')

    def writeHeaders(self):
        headerFile = self.fileNameIn % (-85, -85)

        print 'ebf.info(',headerFile,')'
        ebf.info(headerFile)
        print ' '

        cache = 10
        data = ebf.iterate(headerFile, '/px+', cache)
        for it in data:
            it['hammer_x'] = np.ndarray(len(it['px']), dtype=np.float32)
            it['hammer_y'] = np.ndarray(len(it['px']), dtype=np.float32)

            for iStar in range(len(it['px'])):
                xy = Galaxia.ham.lonLatToXY(it['glon'][iStar], it['glat'][iStar])
                it['hammer_x'][iStar] = xy.x
                it['hammer_y'][iStar] = xy.y

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

        pixels = Galaxia.ham.getPixels()
        nPix = len(pixels)
        Galaxia.outFileNames = [None] * nPix
        for iPix in range(nPix):
            Galaxia.outFileNames[iPix] = self.fileNameOut % (pixels[iPix].xLow,
                                                pixels[iPix].xHigh,
                                                pixels[iPix].yLow,
                                                pixels[iPix].yHigh)
    #        print 'Galaxia.outFileNames[',iPix,'] = ',Galaxia.outFileNames[iPix]
            with open(Galaxia.outFileNames[iPix],'w') as csvFileOut:
                csvFileOut.write(Galaxia.keyStr)

    def processGalaxia(self, lon):
        print 'processGalaxia started'
        print 'Galaxia.outFileNames = ',Galaxia.outFileNames
        print 'Galaxia.keys = ',Galaxia.keys
        print 'Galaxia.keyStr = ',Galaxia.keyStr
        print 'self.fileNameIn = ',self.fileNameIn
        print 'self.fileNameOut = ',self.fileNameOut
        doIt = True
        inputFile = ''

        pixels = Galaxia.ham.getPixels()
        nPix = len(pixels)

        if doIt:
            cache = 100000
    #        for lon in np.arange(-175, 178, 10):
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

                openFiles = []
                openFileNames = []

                data = ebf.iterate(inputFile, '/px+', cache)
                nStarsWritten = 0

                for it in data:

                    long = it['glon']
                    ind=np.where(long < 0.0)[0]
                    long[ind]=long[ind] + 360.0

                    lati = it['glat']

                    it['hammer_x'] = np.ndarray(len(it['px']), dtype=np.float32)
                    it['hammer_y'] = np.ndarray(len(it['px']), dtype=np.float32)
                    xys = Galaxia.ham.lonLatToXY(long, lati)
    #                    print 'xys[0] = ',xys[0]
                    it['hammer_x'] = xys[0]
                    it['hammer_y'] = xys[1]

    #                    for iStar in range(len(it['px'])):
    #                        xy = Galaxia.ham.lonLatToXY(it['glon'][iStar], it['glat'][iStar])
    #                        it['hammer_x'][iStar] = xy.x
    #                        it['hammer_y'][iStar] = xy.y

                    gxutil.append_pm(it)

                    """convert absolute magnitudes to apparent ones"""
                    gxutil.abs2app(it,corr=True)

                    keys = list(it.keys())

                    keyStrTemp = keys[0]
                    for key in keys[1:]:
                        keyStrTemp += ','+key
                    keyStrTemp += '\n'
    #                    print 'keyStrTemp = ',keyStrTemp
                    if Galaxia.keyStr != keyStrTemp:
                        print "ERROR: keyStrings don't match!"
                        STOP

                    for iStar in range(len(it['px'])):
                        longi = long[iStar]
                        latit = lati[iStar]
    #                        print 'iStar = ',iStar,': longi = ',longi,', latit = ',latit
                        if (longi >= lonStart) and (longi < lonEnd) and (latit >= latStart) and (latit < latEnd):
                            pixFound = False
                            xy = hammer.XY(it['hammer_x'][iStar], it['hammer_y'][iStar])
#                            print 'iStar = ',iStar,': xy = ',xy
                            for iPix in range(len(pixels)):
                                if pixels[iPix].isInside(xy):
                                    outFileName = Galaxia.outFileNames[iPix]
                                    pixFound = True

                                    if outFileName not in openFileNames:
                                        openFileNames.append(outFileName)
                                        fn = open(outFileName,'a')
                                        print 'opened file name <',outFileName,'>'
                                        openFiles.append(fn)

                                    outString = str(it[keys[0]][iStar])
                                    for key in Galaxia.keys[1:]:
                                        outString += ','+str(it[key][iStar])
                                    #print 'outString = <',outString,'>'
                                    openFiles[openFileNames.index(outFileName)].write(outString+'\n')
                                    nStarsWritten += 1
                            if not pixFound:
                                print 'ERROR: no pixel found for star (iStar) = ',iStar
                                STOP
                print nStarsWritten,' stars written'
                print 'opened ',len(openFiles),' files, closing them now'
                for file in openFiles:
                    file.close()
                timeEnd = time.time()
                print 'ran file <',inputFile,'> in ',timeEnd-timeStart,' s'
#                STOP

    #        globallock.release()
def processGalaxia(lon):
    gal = Galaxia()
    gal.processGalaxia(lon)

def main(argv):
    """Main program.

    Arguments:
    argv -- command line arguments
    """
    gal = Galaxia()
    gal.writeHeaders()

    p = Pool(processes=1)
    lon = np.arange(-175, 178, 10)
#    lon = np.arange(5, 360, 10)
    print 'lon = ',lon
    p.map(processGalaxia, lon)
#    print 'starting processGalaxia '
#    processGalaxia()
    p.close()

if __name__ == '__main__':
    main(sys.argv)
