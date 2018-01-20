#! /usr/bin/env python

import ebf
import fnmatch
from glob import glob
import gxutil
from multiprocessing import Pool
import numpy as np
import os
import sys
import subprocess

import csvData
import csvFree
import hammer
import moveStarsToXY

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

class Galaxia(object):
    ham = hammer.Hammer()
    pixels = ham.getPixels()
    ebfFilesWritten = []
    keys = []
    ids = ['rad', 'hammerX', 'hammerY', 'exbv_solar']
    progressFile = '/Volumes/yoda/azuri/data/galaxia/ebfFilesWritten.txt'

    def __init__(self):
        dir = '/Volumes/external/azuri/data/galaxia/sdss/'
        self.fileNameIn = os.path.join(dir, 'galaxia_%d_%d.ebf')
        self.headerFile = self.fileNameIn % (-85, -85)

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
        data[Galaxia.ham.getKeyWordHammerX()] = xys[0]
        data[Galaxia.ham.getKeyWordHammerY()] = xys[1]

        gxutil.append_pm(data)

        """convert absolute magnitudes to apparent ones"""
        gxutil.abs2app(data,corr=True)

    def getCSVData(self, data, window, inputFile=None, iIt=0):
        csv = csvData.CSVData()

        print 'getCSVData: window = ',window

        """create CSVData.header"""
        if len(Galaxia.keys) == 0:
            self.getHeader()
        csv.header = Galaxia.keys

        lons = data['glon']
        print 'lons = ',lons
        lats = data['glat']
        print 'lats = ',lats

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
        csv.setData(dataArr)

        if csv.size() != nStarsOut:
            print 'getCSVData: ERROR: csv.size()(=',csv.size(),') != nStarsOut(=',nStarsOut,')'
            STOP
        if csv.size() > 0:
            if len(csv.data[0]) != len(Galaxia.keys):
                print 'getCSVData: ERROR: len(csv.data[0])(=',len(csv.data[0]),') != len(Galaxia.keys)(=',len(Galaxia.keys),')'
                STOP
        return csv

    def processGalaxia(self, lon):
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
                                elif parameterName == 'fSample':
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
                        data = ebf.iterate(ebfFileName, '/px+', cache)

                        iIter = 0
                        for it in data:
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
                                                                 Galaxia.pixels,
                                                                 'galaxia',
                                                                 Galaxia.ids,
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
                Galaxia.ebfFilesWritten.append(ebfFileName)
                with open(Galaxia.progressFile, 'a+') as f:
                        f.write(ebfFileName+'\n')
                os.remove(ebfFileName)

#        globallock.release()
def processGalaxia(lon):
    gal = Galaxia()
    gal.processGalaxia(lon)

def main(argv):
    """Main program.

    Arguments:
    argv -- command line arguments
    """
    galaxia = Galaxia()
    Galaxia.pixels = Galaxia.ham.getPixels()
    galaxia.writeHeaders()

    """delete existing lock files"""
    for filename in glob("/var/lock/*"):
        os.remove(filename)

    """delete old progressFile"""
    if os.path.isfile(Galaxia.progressFile):
        os.remove(Galaxia.progressFile)

    """delete old Galaxia output ebf files"""
    for filename in glob("/Volumes/yoda/azuri/data/galaxia/sdss/*"):
        os.remove(filename)

    processes = 8
    if processes == 1:
        lon = -175
        processGalaxia(lon)
    else:
        p = Pool(processes=processes)
        lon = np.arange(-175, 178, 10)
#    lon = np.arange(5, 360, 10)
        print 'lon = ',lon
        p.map(processGalaxia, lon)
        p.close()

if __name__ == '__main__':
    main(sys.argv)
