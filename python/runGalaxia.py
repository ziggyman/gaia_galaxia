#! /usr/bin/env python

import ebf
import fnmatch
from glob import glob
import gxutil
from multiprocessing import Pool
import numpy as np
import os
import random
import sys
import subprocess
import time

import csvData
import csvFree
import hammer
import moveStarsToXY

class Galaxia(object):
    ham = hammer.Hammer()
    pixels = ham.getPixels()
    ebfFilesWritten = []
    keys = []
    ids = ['rad', 'hammerX', 'hammerY', 'exbv_solar']
    lockSuffix = '_1'
    progressFile = '/Volumes/yoda/azuri/data/galaxia/ebfFilesWritten_Vlt13.txt'
    dir = '/Volumes/yoda/azuri/data/galaxia/ubv_Vlt13'

    def __init__(self):
        self.headerFile = '/Users/azuri/entwicklung/gaia_galaxia/galaxia_65_15_UBV_V-1000_21.5.ebf'#self.fileNameIn % (-85, -85)

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
            gxutil.abs2app(it,corr=True,append=True)

            Galaxia.keys = list(it.keys())
#            print 'Galaxia.keys = ',Galaxia.keys
            break
        return Galaxia.keys

#    def getHeader(self):
#        if len(Galaxia.keys) == 0:
#            cache = 1
#            for filename in glob("/Volumes/yoda/azuri/data/galaxia/sdss/*.ebf"):
#                data = ebf.iterate(filename, '/px+', cache)
#                for it in data:
#                    Galaxia.keys = it.keys()
#                    break
#        Galaxia.keys.append(Galaxia.ham.getKeyWordHammerX())
#        Galaxia.keys.append(Galaxia.ham.getKeyWordHammerY())
##        print 'Galaxia.keys = ',Galaxia.keys

    def writeHeaders(self):

        if len(Galaxia.keys) == 0:
            self.getHeader()

        moveStarsToXY.writeHeaderToOutFiles(Galaxia.keys,
                                            Galaxia.pixels,
                                            'galaxia',
                                            False)

    def addXYandPMandAbs2App(self, data):
        data[Galaxia.ham.getKeyWordHammerX()] = np.ndarray(len(data['px']), dtype=np.float32)
        data[Galaxia.ham.getKeyWordHammerY()] = np.ndarray(len(data['px']), dtype=np.float32)

        long = data['glon']
        ind=np.where(long < 0.0)[0]
        long[ind]=long[ind] + 360.0

        lati = data['glat']
        xys = Galaxia.ham.lonLatToXY(long, lati)
#                    print 'xys[0] = ',xys[0]
        data[Galaxia.ham.getKeyWordHammerX()] = np.asarray(xys[0])
        data[Galaxia.ham.getKeyWordHammerY()] = np.asarray(xys[1])

        gxutil.append_pm(data)

        """convert absolute magnitudes to apparent ones"""
        gxutil.abs2app(data,corr=True,append=True)

    def getStarsInWindow(self, data, window):
        lons = data['glon']
#        print 'lons = ',lons
        lats = data['glat']
#        print 'lats = ',lats
#        print 'len(lons) = ',len(lons)

        indicesInWindowXLow = np.where(lons >= window.xLow)[0]# and (lons < window.xHigh) and (lats >= window.yLow) and (lats < window.yHigh)).all())
#        print 'getStarsInWindow: indicesInWindowXLow = ',indicesInWindowXLow
#        print 'getStarsInWindow: len(lons[indicesInWindowXLow]) = ',len(lons[indicesInWindowXLow])

        indicesInWindowXHigh = np.where(lons[indicesInWindowXLow] < window.xHigh)[0]# and (lons < window.xHigh) and (lats >= window.yLow) and (lats < window.yHigh)).all())
#        print 'getStarsInWindow: indicesInWindowXHigh = ',indicesInWindowXHigh
#        print 'getStarsInWindow: len(lons[indicesInWindowXLow[indicesInWindowXHigh]]) = ',len(lons[indicesInWindowXLow[indicesInWindowXHigh]])

        indicesInWindowYLow = np.where(lats[indicesInWindowXLow[indicesInWindowXHigh]] >= window.yLow)[0]# and (lons < window.xHigh) and (lats >= window.yLow) and (lats < window.yHigh)).all())
#        print 'getStarsInWindow: indicesInWindowYLow = ',indicesInWindowYLow
#        print 'getStarsInWindow: len(lats[indicesInWindowXLow[indicesInWindowXHigh[indicesInWindowYLow]]]) = ',len(lats[indicesInWindowXLow[indicesInWindowXHigh[indicesInWindowYLow]]])

        indicesInWindowYHigh = np.where(lats[indicesInWindowXLow[indicesInWindowXHigh[indicesInWindowYLow]]] < window.yHigh)[0]# and (lons < window.xHigh) and (lats >= window.yLow) and (lats < window.yHigh)).all())
#        print 'getStarsInWindow: indicesInWindowYHigh = ',indicesInWindowYHigh
#        print 'getStarsInWindow: len(lats[indicesInWindowXLow[indicesInWindowXHigh[indicesInWindowYLow[indicesInWindowYHigh]]]]) = ',len(lats[indicesInWindowXLow[indicesInWindowXHigh[indicesInWindowYLow[indicesInWindowYHigh]]]])

        for key in data.keys():
#            print 'getStarsInWindow: len(data[',key,']) = ',len(data[key])
#            print 'getStarsInWindow: data[',key,'] = ',type(data[key]),': ',type(data[key][0]),': ',data[key]
            data[key] = data[key][indicesInWindowXLow[indicesInWindowXHigh[indicesInWindowYLow[indicesInWindowYHigh]]]]
#            print 'getStarsInWindow: len(data[',key,']) = ',len(data[key])

    def getCSVData(self, data, inputFile=None, iIt=0):
        csv = csvData.CSVData()

        """create CSVData.header"""
        if len(Galaxia.keys) == 0:
            self.getHeader()
        csv.header = Galaxia.keys

        dataArr = []

#        print 'Galaxia.keys = ',len(Galaxia.keys),': ',Galaxia.keys
        for iStar in range(len(data['px'])):
            outVec = []
            for iDat in range(len(Galaxia.keys)):
                dataVec = data[Galaxia.keys[iDat]]
#                    print 'key = ',Galaxia.keys[iDat],': dataVec = ',len(dataVec),': ',dataVec
                outVec.append(str(dataVec[iStar]))
#                    print 'outVec[',len(outVec)-1,'] = ',outVec[len(outVec)-1]
            dataArr.append(outVec)

        csv.setData(dataArr)
        return csv

    def processGalaxia(self, lon, test=False):
#        reload(sys)
        outputDir = Galaxia.dir#os.path.join(dir, 'ubv_vLT13')
#        ebfOutputDir = '/Volumes/external/azuri/data/galaxia/ubv'
        outputFile = ''
        overwrite = True
        doIt = True
        doCSV = True

        latRange = np.arange(-85, 90, 10)
        if test:
            latRange = [-15]
        for lat in latRange:
            timeStart = time.time()
    #    for lat in np.arange(15, 50, 10):
            outputFile = 'galaxia_%d_%d' % (lon, lat)
#            print "outputFile = <", outputFile, ">"
    #        globallock.acquire()
            parameterFileOut = os.path.join(Galaxia.dir, 'parameterfile_%d_%d' % (lon, lat))
            surveyArea = 157.08

            # Read parameterfile
            if (overwrite
                or (not os.path.isfile(parameterFileOut))):
#                print 'creating parameterFileOut <',parameterFileOut,'>'
                if doIt:
                    with open(parameterFileOut, 'w') as fOut:
                        fOut.write('outputFile '+outputFile+'\n')
                        fOut.write('outputDir '+outputDir+'\n')
                        fOut.write('photoSys UBV\n')
                        fOut.write('magcolorNames V,B-V\n')
                        fOut.write('appMagLimits[0] -1000\n')
                        fOut.write('appMagLimits[1] 13.0\n')
                        fOut.write('absMagLimits[0] -1000\n')
                        fOut.write('absMagLimits[1] 1000\n')
                        fOut.write('colorLimits[0] -1000\n')
                        fOut.write('colorLimits[1] 1000\n')
                        fOut.write('geometryOption 1\n')
                        fOut.write('longitude %d\n' % lon)
                        fOut.write('latitude %d\n' % lat)
                        fOut.write('surveyArea %f\n' % surveyArea)
                        fOut.write('fSample 1.0\n')
                        fOut.write('popID -1\n')
                        fOut.write('warpFlareOn 1\n')
                        fOut.write('seed 3\n')
                        fOut.write('r_max 1000\n')
                        fOut.write('starType 0\n')
                        fOut.write('photoError 0\n')
                else:
                    print 'processGalaxia: doIt == False => not actually doing anything'
            else:
                if not overwrite:
                    print 'processGalaxia: overwrite == False => not creating parameterfile'
                if os.path.isfile(parameterFileOut):
                    print 'processGalaxia: parameterFileOut <',parameterFileOut,'> found => not creating parameterfile'

            filterMatch = fnmatch.filter(os.listdir(outputDir), outputFile+'.ebf.*')
    #        print 'filterMatch = ',filterMatch
            tmpFiles = [n for n in filterMatch if os.path.isfile(os.path.join(outputDir, n))]
#            print 'outputFile = ',outputFile,': len(tmpFiles) = ',len(tmpFiles),': tmpFiles = ',tmpFiles
            ebfFileName = os.path.join(outputDir, outputFile+'.ebf')
            if (overwrite
                or (not os.path.isfile(ebfFileName))
                or (os.path.isfile(ebfFileName)
                    and len(tmpFiles) > 0)):
                print 'processGalaxia: outputFile = ',outputFile,': calculating'
                if doIt:
                    args = ['galaxia', '-r', parameterFileOut]
                    rv = subprocess.call(args)
                    if rv == 1:
                        print "processGalaxia: longitude=%d, latitude=%d processed." % (lon, lat)
                    else:
                        print "processGalaxia: Error when processing file longitude=%d, latitude=%d: error code = %d" % (lon, lat, rv)
                else:
                    print 'processGalaxia: doIt == False = not running galaxia'
            else:
                if not overwrite:
                    print 'processGalaxia: overwrite == false => not running galaxia'
                if os.path.isfile(ebfFileName):
                    print "processGalaxia: galaxia output file ",ebfFileName," found => not running galaxia"
                if (os.path.isfile(ebfFileName)
                    and len(tmpFiles) == 0):
                    print "processGalaxia: galaxia output file ",ebfFileName," found and no temp files => not running galaxia"
    #        if not os.path.isfile(os.path.join(outputDir, outputFile+'.ebf')):
    #            print "ERROR: file <",os.path.join(outputDir, outputFile+'.ebf'),"> not found"
    #            STOP
            if doCSV:
                nLines = len(ebf.read(ebfFileName, '/px'))
                lonStart = lon-5
                lonEnd = lon+5
                if (lon < 0):
                    lonStart += 360.0
                    lonEnd += 360.0
                latStart = lat-5
                latEnd = lat+5
#                print 'lonStart = ',lonStart,', lonEnd = ',lonEnd,', latStart = ',latStart,', latEnd = ',latEnd
                if (overwrite):
                    cache = 100000

                    nStarsWritten = 0
                    if doIt:
                        data = ebf.iterate(ebfFileName, '/px+', cache)

                        iIter = 0
#                        ebfFileNameOut = os.path.join(ebfOutputDir, outputFile+'.ebf')
#                        try:
#                            ebf.initialize(ebfFileNameOut)
#                        except Exception as e:
#                            print "processGalaxia: Unexpected error initalizing ",ebfFileNameOut,": ",str(e)

                        durationAll = 0.0
                        nLinesRead = 0;
                        for it in data:
                            nLinesRead += cache
                            timeStartIt = time.time()
                            self.addXYandPMandAbs2App(it)

                            window = hammer.Pixel()
                            window.xLow = lonStart
                            window.xHigh = lonEnd
                            window.yLow = latStart
                            window.yHigh = latEnd

                            self.getStarsInWindow(it, window)
                            print "processGalaxia: len(it['px']) = ",len(it['px'])
#                            print 'processGalaxia: it.keys() = ',it.keys()
#                            print 'processGalaxia: data.keys() = ',data.keys()
#                            try:
#                                for key in it.keys():
#                                    print 'processGalaxia: key = ',key
#                                    ebf.write(ebfFileNameOut, '/'+key, it[key], 'a')
#                            except Exception as e:
#                                print "processGalaxia: Unexpected error writing to ",ebfFileNameOut,": ",str(e)

                            csv = self.getCSVData(it, ebfFileName, iIter)
#                            for iStar in range(csv.size()):
#                                print 'lon[',iStar,'] = ',csv.getData('glon',iStar),', lat[',iStar,'] = ',csv.getData('glat',iStar),': hammerX[',iStar,'] = ',csv.getData('hammerX',iStar),', hammerY[',iStar,'] = ',csv.getData('hammerY',iStar)
                            doFind = False
                            moveStarsToXY.appendCSVDataToXYFiles(csv,
                                                                 Galaxia.pixels,
                                                                 'galaxia',
                                                                 Galaxia.ids,
                                                                 doFind,
                                                                 Galaxia.lockSuffix)
                            timeEnd = time.time()
                            duration = timeEnd-timeStartIt
                            durationAll += duration
                            print 'ran file <',ebfFileName,'> iIter=',iIter,' in ',int(duration),' s: ',nLinesRead * 100.0 / nLines,' % done in ',int(durationAll),' seconds'
                            iIter += 1
                        print nStarsWritten,' stars written'
                                    #STOP
                    else:
                        print 'not actually doing anything'
                else:
                    if not overwrite:
                        print 'overwrite == False => not calculating'
            if os.path.exists(ebfFileName):
                Galaxia.ebfFilesWritten.append(ebfFileName)
                with open(Galaxia.progressFile, 'a+') as f:
                        f.write(ebfFileName+'\n')
#                os.remove(ebfFileName)

            timeEnd = time.time()
            duration = timeEnd-timeStart
            print 'ran file <',ebfFileName,'> iIter=',iIter,' in ',int(duration),' s'

#        globallock.release()
def processGalaxia(lon, test=False):
    gal = Galaxia()
    gal.processGalaxia(lon, test=test)

def main(argv):
    """Main program.

    Arguments:
    argv -- command line arguments
    """
    galaxia = Galaxia()
    Galaxia.pixels = Galaxia.ham.getPixels()
    galaxia.writeHeaders()

    """delete existing lock files"""
    for filename in glob("/var/lock/*"+lockSuffix):
        os.remove(filename)

    """delete old progressFile"""
    if os.path.isfile(Galaxia.progressFile):
        os.remove(Galaxia.progressFile)

    """delete old Galaxia outputs files"""
    for filename in glob(os.path.join(Galaxia.dir,"*.ebf*")):
        os.remove(filename)

    processes = 16
    if processes == 1:
        lon = -75
        processGalaxia(lon, test=True)
    else:
        p = Pool(processes=processes)
        lon = np.arange(-175, 178, 10)
        random.shuffle(lon)
        #    lon = np.arange(5, 360, 10)
        print 'lon = ',lon
        p.map(processGalaxia, lon)
        p.close()

if __name__ == '__main__':
    main(sys.argv)
