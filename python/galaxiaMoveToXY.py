#! /usr/bin/env python

import ebf
import gxutil
import os
import sys
import time
import numpy as np
import hammer

#globallock = Lock()

def get_aebv_factor(band):
    if band == 'sdss_u':
        return 5.155
    elif band == 'sdss_g':
        return 3.793
    elif band == 'sdss_r':
        return 2.751
    elif band == 'sdss_i':
        return 2.086
    elif band == 'sdss_z':
        return 1.479
    else:
        print 'get_aebv_factor: unknown band <',band,'>'
        STOP

def processGalaxia():
    print 'processGalaxia started'
    dir = '/Volumes/yoda/azuri/data/galaxia/sdss/'
    outputDir = '/Volumes/yoda/azuri/data/galaxia/xy/'
    inputFile = ''
    outputFile = ''

    fileNameIn = os.path.join(dir, 'galaxia_%d_%d.ebf')
    fileNameOut = os.path.join(outputDir,'galaxia_%0.6f-%0.6f_%0.6f-%0.6f.csv')
    overwrite = False
    doIt = True

    headerFile = fileNameIn % (-85, -85)

    print 'ebf.info(',headerFile,')'
    ebf.info(headerFile)
    print ' '

    ham = hammer.Hammer()

    cache = 10
    data = ebf.iterate(headerFile, '/px+', cache)
    keys = []
    for it in data:
        it['hammer_x'] = np.ndarray(len(it['px']), dtype=np.float32)
        it['hammer_y'] = np.ndarray(len(it['px']), dtype=np.float32)

        for iStar in range(len(it['px'])):
            xy = ham.lonLatToXY(it['glon'][iStar], it['glat'][iStar])
            it['hammer_x'][iStar] = xy.x
            it['hammer_y'][iStar] = xy.y

        gxutil.append_pm(it)

        """convert absolute magnitudes to apparent ones"""
        gxutil.abs2app(it,corr=True)

        keys = list(it.keys())
        print 'keys = ',keys
        break

    keyStr = keys[0]
    for key in keys[1:]:
        keyStr += ','+key
    keyStr += '\n'
    print 'keyStr = ',keyStr

    pixels = ham.getPixels()
    nPix = len(pixels)
    outFileNames = [None] * nPix
    for iPix in range(nPix):
        outFileNames[iPix] = fileNameOut % (pixels[iPix].xLow,
                                            pixels[iPix].xHigh,
                                            pixels[iPix].yLow,
                                            pixels[iPix].yHigh)
#        print 'outFileNames[',iPix,'] = ',outFileNames[iPix]
        with open(outFileNames[iPix],'w') as csvFileOut:
            csvFileOut.write(keyStr)

    if True:
        cache = 100000
        for lon in np.arange(-175, 178, 10):
            for lat in np.arange(-85, 90, 10):
                timeStart = time.time()
                inputFile = fileNameIn % (lon, lat)
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

                for it in data:

                    long = it['glon']
                    ind=np.where(long < 0.0)[0]
                    long[ind]=long[ind] + 360.0

                    lati = it['glat']

                    it['hammer_x'] = np.ndarray(len(it['px']), dtype=np.float32)
                    it['hammer_y'] = np.ndarray(len(it['px']), dtype=np.float32)
                    xys = ham.lonLatToXY(long, lati)
#                    print 'xys[0] = ',xys[0]
                    it['hammer_x'] = xys[0]
                    it['hammer_y'] = xys[1]

#                    for iStar in range(len(it['px'])):
#                        xy = ham.lonLatToXY(it['glon'][iStar], it['glat'][iStar])
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
                    if keyStr != keyStrTemp:
                        print "ERROR: keyStrings don't match!"
                        STOP

                    nStarsWritten = 0
                    for iStar in range(len(it['px'])):
                        longi = long[iStar]
                        latit = lati[iStar]
#                        print 'iStar = ',iStar,': longi = ',longi,', latit = ',latit
                        if (longi >= lonStart) and (longi < lonEnd) and (latit >= latStart) and (latit < latEnd):
                            pixFound = False
                            xy = hammer.XY(it['hammer_x'][iStar], it['hammer_y'][iStar])
                            print 'iStar = ',iStar,': xy = ',xy
                            for iPix in range(len(pixels)):
                                if pixels[iPix].isInside(xy):
                                    outFileName = outFileNames[iPix]
                                    pixFound = True

                                    if outFileName not in openFileNames:
                                        openFileNames.append(outFileName)
                                        fn = open(outFileName,'a')
                                        print 'opened file name <',outFileName,'>'
                                        openFiles.append(fn)

                                    outString = str(it[keys[0]][iStar])
                                    for key in keys[1:]:
                                        outString += ','+str(it[key][iStar])
                                    #print 'outString = <',outString,'>'
                                    openFiles[openFileNames.index(outFileName)].write(outString+'\n')
                                    nStarsWritten += 1
                            if not pixFound:
                                print 'ERROR: no pixel found for star (iStar) = ',iStar
                    print nStarsWritten,' stars written'
                print 'opened ',len(openFiles),' files, closing them now'
                for file in openFiles:
                    file.close()
                timeEnd = time.time()
                print 'ran file <',inputFile,'> in ',timeEnd-timeStart,' s'
                STOP

#        globallock.release()

def main(argv):
    """Main program.

    Arguments:
    argv -- command line arguments
    """
#    p = Pool(processes=1)
#    lon = np.arange(-175, 178, 10)
#    lon = np.arange(5, 360, 10)
#    print 'lon = ',lon
#    p.map(processGalaxia, lon)
    print 'starting processGalaxia'
    processGalaxia()
#    p.close()

if __name__ == '__main__':
    main(sys.argv)
