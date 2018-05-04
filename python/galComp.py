#! /usr/bin/env python

import ebf
import fnmatch
import gxutil
import numpy as np
import os
import subprocess

import csvData
#import csvFree
import hammer
import moveStarsToXY

class GalComp(object):
    ham = hammer.Hammer()
    pixels = ham.getPixels()
    galaxiaKeys = GalComp.getGalaxiaHeader()
    gaiaKeys = GalComp.getGaiaKeys()
    progressFile = '/Volumes/yoda/azuri/data/gaia-galaxia/pixelsFinished.txt'
    galaxiaDir = '/Volumes/yoda/azuri/data/galaxia/xy'
    gaiaDir = '/Volumes/yoda/azuri/data/gaia-tgas/xy/'

    def __init__(self):
        dir = '/Volumes/external/azuri/data/galaxia/sdss/'
        self.fileNameIn = os.path.join(dir, )
        self.headerFile = self.fileNameIn % (-85, -85)

    def getGalaxiaHeader(self):
        if len(GalComp.galaxiaKeys) == 0:
            cache = 1
            for filename in glob("/Volumes/yoda/azuri/data/galaxia/sdss/*.ebf"):
                ebfData = ebf.iterate(filename, '/px+', cache)
                for it in ebfData:
                    GalComp.galaxiaKeys = it.keys()
                    break

#    def getGaiaHeader(self):


    def writeHeaders(self):

        if len(GalComp.keys) == 0:
            self.getGalaxiaHeaderWithPmAppMagHammer()

        moveStarsToXY.writeHeaderToOutFiles(GalComp.keys,
                                            GalComp.pixels,
                                            'galaxia',
                                            False)

    def addXYandPMandAbs2App(self, ebfData):
        ebfData[GalComp.ham.getKeyWordHammerX()] = np.ndarray(len(ebfData['px']), dtype=np.float32)
        ebfData[GalComp.ham.getKeyWordHammerY()] = np.ndarray(len(ebfData['px']), dtype=np.float32)

        long = ebfData['glon']
        ind=np.where(long < 0.0)[0]
        long[ind]=long[ind] + 360.0

        lati = ebfData['glat']
        xys = GalComp.ham.lonLatToXY(long, lati)
#                    print 'xys[0] = ',xys[0]
        ebfData[GalComp.ham.getKeyWordHammerX()] = xys[0]
        ebfData[GalComp.ham.getKeyWordHammerY()] = xys[1]

        gxutil.append_pm(ebfData)

        """convert absolute magnitudes to apparent ones"""
        gxutil.abs2app(ebfData,corr=True)

    def getCSVData(self, ebfData, window=None, inputFile=None, iIt=0):
        csv = csvData.CSVData()

        print 'getCSVData: window = ',window

        """create CSVData.header"""
        if len(GalComp.keys) == 0:
            self.getGalaxiaHeaderWithPmAppMagHammer()
        csv.header = GalComp.keys

        lons = ebfData['glon']
        print 'lons = ',lons
        lats = ebfData['glat']
        print 'lats = ',lats

        dataArr = []

#        print 'GalComp.keys = ',len(GalComp.keys),': ',GalComp.keys
        nStarsOut = 0
        for iStar in range(len(ebfData['px'])):
            lon = lons[iStar]
            lat = lats[iStar]
#                        print 'iStar = ',iStar,': lon = ',lon,', lat = ',lat
            if ((lon >= window.xLow)
                and (lon < window.xHigh)
                and (lat >= window.yLow)
                and (lat < window.yHigh)):

                outVec = []
                for iDat in range(len(GalComp.keys)):
                    dataVec = ebfData[GalComp.keys[iDat]]
#                    print 'key = ',GalComp.keys[iDat],': dataVec = ',len(dataVec),': ',dataVec
                    outVec.append(str(dataVec[iStar]))
#                    print 'outVec[',len(outVec)-1,'] = ',outVec[len(outVec)-1]
                if len(outVec) != len(GalComp.keys):
                    print 'getCSVData: ERROR: len(outVec)(=',len(outVec),') != len(GalComp.keys)(=',len(GalComp.keys),')'
                    STOP
                dataArr.append(outVec)
                nStarsOut += 1

        print 'file <',inputFile,'>: window: [',window.xLow,', ',window.xHigh,' : ',window.yLow,', ',window.yHigh,']: iIt = ',iIt,': nStarsOut = ',nStarsOut
        csv.setData(dataArr)

        if csv.size() != nStarsOut:
            print 'getCSVData: ERROR: csv.size()(=',csv.size(),') != nStarsOut(=',nStarsOut,')'
            STOP
        if csv.size() > 0:
            if len(csv.data[0]) != len(GalComp.keys):
                print 'getCSVData: ERROR: len(csv.data[0])(=',len(csv.data[0]),') != len(GalComp.keys)(=',len(GalComp.keys),')'
                STOP
        return csv

    def processGalComp(self, lon):
        dir = '/Volumes/yoda/azuri/data/galaxia'
        outputDir = os.path.join(dir, 'sdss')
        parameterFileIn = os.path.join(dir, 'parameterfile')
        outputFile = ''
        overwrite = True
        doIt = True
        doCSV = True

        for lat in np.arange(-85, 90, 10):
    #    for lat in np.arange(15, 50, 10):
            outputFile = 'galaxia_%d_%d' % (lon, lat)
#            print "outputFile = <", outputFile, ">"
    #        globallock.acquire()
            parameterFileOut = os.path.join(dir, 'parameterfile_%d_%d' % (lon, lat))
            surveyArea = 157.08

            # Read parameterfile
            if (overwrite
                or (not os.path.isfile(parameterFileOut))):
#                print 'creating parameterFileOut <',parameterFileOut,'>'
                if doIt:
                    with open(parameterFileIn, 'r') as fIn:
                        with open(parameterFileOut, 'w') as fOut:
                            for line in fIn:
                                words = line.split(' ')
                                parameterName = words[0]
                                parameterValue = words[len(words)-1]
                                if parameterName == 'outputFile':
                                    parameterValue = outputFile+'\n'
                                elif parameterName == 'outputDir':
                                    parameterValue = outputDir+'\n'
                                elif parameterName == 'longitude':
                                    parameterValue = '%d\n' % lon
                                elif parameterName == 'latitude':
                                    parameterValue = '%d\n' % lat
                                elif parameterName == 'surveyArea':
                                    parameterValue = '%f\n' % surveyArea
                                elif parameterName == 'seed':
                                    parameterValue = '3\n'
                                elif parameterName == 'geometryOption':
                                    parameterValue = '1\n'
                                elif parameterName == 'fsample':
                                    parameterValue = '0.1\n'
                                fOut.write(parameterName+' '+parameterValue)
                else:
                    print 'doIt == False => not actually doing anything'
            else:
                if not overwrite:
                    print 'overwrite == False => not creating parameterfile'
                if os.path.isfile(parameterFileOut):
                    print 'parameterFileOut <',parameterFileOut,'> found => not creating parameterfile'

            filterMatch = fnmatch.filter(os.listdir(outputDir), outputFile+'.ebf.*')
    #        print 'filterMatch = ',filterMatch
            tmpFiles = [n for n in filterMatch if os.path.isfile(os.path.join(outputDir, n))]
#            print 'outputFile = ',outputFile,': len(tmpFiles) = ',len(tmpFiles),': tmpFiles = ',tmpFiles
            ebfFileName = os.path.join(outputDir, outputFile+'.ebf')
            if (overwrite
                or (not os.path.isfile(ebfFileName))
                or (os.path.isfile(ebfFileName)
                    and len(tmpFiles) > 0)):
                print 'outputFile = ',outputFile,': calculating'
                if doIt:
                    args = ['galaxia', '-r', parameterFileOut]
                    rv = subprocess.call(args)
                    if rv == 1:
                        print "longitude=%d, latitude=%d processed." % (lon, lat)
                    else:
                        print "Error when processing file longitude=%d, latitude=%d: error code = %d" % (lon, lat, rv)
                else:
                    print 'doIt == False = not running galaxia'
            else:
                if not overwrite:
                    print 'overwrite == false => not running galaxia'
                if os.path.isfile(ebfFileName):
                    print "galaxia output file ",ebfFileName," found => not running galaxia"
                if (os.path.isfile(ebfFileName)
                    and len(tmpFiles) == 0):
                    print "galaxia output file ",ebfFileName," found and no temp files => not running galaxia"
    #        if not os.path.isfile(os.path.join(outputDir, outputFile+'.ebf')):
    #            print "ERROR: file <",os.path.join(outputDir, outputFile+'.ebf'),"> not found"
    #            STOP
            if doCSV:
                lonStart = lon-5
                lonEnd = lon+5
                if (lon < 0):
                    lonStart += 360.0
                    lonEnd += 360.0
                latStart = lat-5
                latEnd = lat+5
#                print 'lonStart = ',lonStart,', lonEnd = ',lonEnd,', latStart = ',latStart,', latEnd = ',latEnd
                if (overwrite):
                    cache = 10000

                    nStarsWritten = 0
                    if doIt:
                        ebfData = ebf.iterate(ebfFileName, '/px+', cache)

                        iIter = 0
                        for it in ebfData:
                            self.addXYandPMandAbs2App(it)

                            window = hammer.Pixel()
                            window.xLow = lonStart
                            window.xHigh = lonEnd
                            window.yLow = latStart
                            window.yHigh = latEnd

                            csv = self.getCSVData(it, window, ebfFileName, iIter)

#                            for iStar in range(csv.size()):
#                                print 'lon[',iStar,'] = ',csv.getData('glon',iStar),', lat[',iStar,'] = ',csv.getData('glat',iStar),': hammerX[',iStar,'] = ',csv.getData('hammerX',iStar),', hammerY[',iStar,'] = ',csv.getData('hammerY',iStar)
                            doFind = False
                            moveStarsToXY.appendCSVDataToXYFiles(csv,
                                                                 GalComp.pixels,
                                                                 'galaxia',
                                                                 GalComp.ids,
                                                                 doFind)
                            iIter += 1
                        print nStarsWritten,' stars written'
                                    #STOP
                    else:
                        print 'not actually doing anything'
                else:
                    if not overwrite:
                        print 'overwrite == False => not calculating'
            if os.path.exists(ebfFileName):
                GalComp.ebfFilesWritten.append(ebfFileName)
                with open(GalComp.progressFile, 'a+') as f:
                        f.write(ebfFileName+'\n')
                os.remove(ebfFileName)
