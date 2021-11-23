import ebf
import fnmatch
from glob import glob
import gxutil
import numpy as np
import os
import subprocess
import time

import csvData2
import csvFree2
import hammer2
import moveStarsToXY2
from utils import mkdir_p

class Galaxia(object):
    ham = hammer2.Hammer()
    pixels = ham.getPixels()
    ebfFilesWritten = []
    keys = []
    ids = ['rad', 'hammerX', 'hammerY', 'exbv_solar']
    fSample = 1.0
    maxVMag = 27.
    lonMin = 5
    lonMax = 180
    photoSys = 'UBV'
    tmpDir = 'ubv_Vlt%.1f_%.1f' % (maxVMag, fSample)
    print('tmpDir = ',tmpDir)
    lockSuffix = '_'+tmpDir+'_'
    dir = os.path.join('/Volumes/discovery/azuri/data/galaxia', tmpDir)
    mkdir_p(dir)
    print('dir = ',dir)

    progressFile = os.path.join(dir, 'ebfFilesWritten.txt')
    appendToProgressFile = True

    xyDir = os.path.join(dir, 'xy/')
    mkdir_p(xyDir)

    append = True
    overwrite = True
    overwriteParameterFile = True
    doIt = True
    doCSV = True

    deleteOldXYFiles = True

    done = []
    if os.path.exists(progressFile):
        with open(progressFile) as f:
            done = f.readlines()
        # remove whitespace characters like `\n` at the end of each line
        done = [x.strip() for x in done]

    def __init__(self):
        self.headerFile = '/Users/azuri/entwicklung/gaia_galaxia/galaxia_2.5_-30_UBV_V-1000_13.ebf'#self.fileNameIn % (-85, -85)

    def getHeader(self):

        print('ebf.info(',self.headerFile,')')
        ebf.info(self.headerFile)
        print(' ')

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
#            print('Galaxia.keys = ',Galaxia.keys
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
##        print('Galaxia.keys = ',Galaxia.keys

    def writeHeaders(self):

        if len(Galaxia.keys) == 0:
            self.getHeader()

        moveStarsToXY2.writeHeaderToOutFiles(Galaxia.keys,
                                            Galaxia.pixels,
                                            'galaxia',
                                            Galaxia.append,
                                            Galaxia.xyDir)

    def addXYandPMandAbs2App(self, data):
        data[Galaxia.ham.getKeyWordHammerX()] = np.ndarray(len(data['px']), dtype=np.float32)
        data[Galaxia.ham.getKeyWordHammerY()] = np.ndarray(len(data['px']), dtype=np.float32)

        long = data['glon']
        ind=np.where(long < 0.0)[0]
        long[ind]=long[ind] + 360.0

        lati = data['glat']
        xys = Galaxia.ham.lonLatToXY(long, lati)
#                    print('xys[0] = ',xys[0]
        data[Galaxia.ham.getKeyWordHammerX()] = np.asarray(xys[0])
        data[Galaxia.ham.getKeyWordHammerY()] = np.asarray(xys[1])

        gxutil.append_pm(data)

        """convert absolute magnitudes to apparent ones"""
        gxutil.abs2app(data,corr=True,append=True)

    def getStarsInWindow(self, data, window):
        lons = data['glon']
#        print('lons = ',lons
        lats = data['glat']
#        print('lats = ',lats
#        print('len(lons) = ',len(lons)

        indicesInWindowXLow = np.where(lons >= window.xLow)[0]# and (lons < window.xHigh) and (lats >= window.yLow) and (lats < window.yHigh)).all())
#        print('getStarsInWindow: indicesInWindowXLow = ',indicesInWindowXLow
#        print('getStarsInWindow: len(lons[indicesInWindowXLow]) = ',len(lons[indicesInWindowXLow])

        indicesInWindowXHigh = np.where(lons[indicesInWindowXLow] < window.xHigh)[0]# and (lons < window.xHigh) and (lats >= window.yLow) and (lats < window.yHigh)).all())
#        print('getStarsInWindow: indicesInWindowXHigh = ',indicesInWindowXHigh
#        print('getStarsInWindow: len(lons[indicesInWindowXLow[indicesInWindowXHigh]]) = ',len(lons[indicesInWindowXLow[indicesInWindowXHigh]])

        indicesInWindowYLow = np.where(lats[indicesInWindowXLow[indicesInWindowXHigh]] >= window.yLow)[0]# and (lons < window.xHigh) and (lats >= window.yLow) and (lats < window.yHigh)).all())
#        print('getStarsInWindow: indicesInWindowYLow = ',indicesInWindowYLow
#        print('getStarsInWindow: len(lats[indicesInWindowXLow[indicesInWindowXHigh[indicesInWindowYLow]]]) = ',len(lats[indicesInWindowXLow[indicesInWindowXHigh[indicesInWindowYLow]]])

        indicesInWindowYHigh = np.where(lats[indicesInWindowXLow[indicesInWindowXHigh[indicesInWindowYLow]]] < window.yHigh)[0]# and (lons < window.xHigh) and (lats >= window.yLow) and (lats < window.yHigh)).all())
#        print('getStarsInWindow: indicesInWindowYHigh = ',indicesInWindowYHigh
#        print('getStarsInWindow: len(lats[indicesInWindowXLow[indicesInWindowXHigh[indicesInWindowYLow[indicesInWindowYHigh]]]]) = ',len(lats[indicesInWindowXLow[indicesInWindowXHigh[indicesInWindowYLow[indicesInWindowYHigh]]]])

        for key in data.keys():
#            print('getStarsInWindow: len(data[',key,']) = ',len(data[key])
#            print('getStarsInWindow: data[',key,'] = ',type(data[key]),': ',type(data[key][0]),': ',data[key]
            data[key] = data[key][indicesInWindowXLow[indicesInWindowXHigh[indicesInWindowYLow[indicesInWindowYHigh]]]]
#            print('getStarsInWindow: len(data[',key,']) = ',len(data[key])

    def getCSVData(self, data, inputFile=None, iIt=0):
        csv = csvData2.CSVData()

        """create CSVData.header"""
        if len(Galaxia.keys) == 0:
            self.getHeader()
        csv.header = Galaxia.keys

        dataArr = []

#        print('Galaxia.keys = ',len(Galaxia.keys),': ',Galaxia.keys
        for iStar in range(len(data['px'])):
            outVec = []
            for iDat in range(len(Galaxia.keys)):
                dataVec = data[Galaxia.keys[iDat]]
#                    print('key = ',Galaxia.keys[iDat],': dataVec = ',len(dataVec),': ',dataVec
                outVec.append(str(dataVec[iStar]))
#                    print('outVec[',len(outVec)-1,'] = ',outVec[len(outVec)-1]
            dataArr.append(outVec)

        csv.setData(dataArr)
        return csv

    def processGalaxia(self, lon, test=False):
#        reload(sys)
#        ebfOutputDir = '/Volumes/external/azuri/data/galaxia/ubv'
        outputFile = ''

        latRange = np.arange(-85, 90, 10)
        if test:
            latRange = [5, 15]
        print('processGalaxia: latRange = ',latRange)
        for lat in latRange:
            print('processGalaxia: lat = ',lat)
            timeStart = time.time()
    #    for lat in np.arange(15, 50, 10):
            lonLatStr = '%d_%d' % (lon, lat)
            outputFile = 'galaxia_' + lonLatStr
            outputDir = os.path.join(Galaxia.dir, lonLatStr)
            mkdir_p(outputDir)
            print('processGalaxia: outputDir <'+outputDir+'> created')

            xyOutputDir = outputDir+'/xy/'
            mkdir_p(xyOutputDir)
            print('processGalaxia: xyOutputDir <'+xyOutputDir+'> created')

#            print("outputFile = <", outputFile, ">"
    #        globallock.acquire()
            parameterFileOut = os.path.join(outputDir, 'parameterfile_' + lonLatStr)
            surveyArea = 157.08

            # Read parameterfile
            if (Galaxia.overwrite
                or (not os.path.isfile(parameterFileOut))
                or Galaxia.overwriteParameterFile):
#                print('creating parameterFileOut <',parameterFileOut,'>'
                if Galaxia.doIt:
                    with open(parameterFileOut, 'w') as fOut:
                        fOut.write('outputFile '+outputFile+'\n')
                        fOut.write('outputDir '+outputDir+'\n')
                        fOut.write('photoSys '+Galaxia.photoSys+'\n')
                        fOut.write('magcolorNames V,B-V\n')
                        fOut.write('appMagLimits[0] -1000\n')
                        fOut.write('appMagLimits[1] %.1f\n' % (Galaxia.maxVMag))
                        fOut.write('absMagLimits[0] -1000\n')
                        fOut.write('absMagLimits[1] 1000\n')
                        fOut.write('colorLimits[0] -1000\n')
                        fOut.write('colorLimits[1] 1000\n')
                        fOut.write('geometryOption 1\n')
                        fOut.write('longitude %d\n' % lon)
                        fOut.write('latitude %d\n' % lat)
                        fOut.write('surveyArea %f\n' % surveyArea)
                        fOut.write('fSample %.1f\n' % (Galaxia.fSample))
                        fOut.write('popID -1\n')
                        fOut.write('warpFlareOn 1\n')
                        fOut.write('seed 17\n')
                        fOut.write('r_max 1000\n')
                        fOut.write('starType 0\n')
                        fOut.write('photoError 0\n')
                    print('processGalaxia: parameterFileOut <'+parameterFileOut+'> written')
                else:
                    print('processGalaxia: Galaxia.doIt == False => not actually doing anything')
            else:
                if not Galaxia.overwrite:
                    print('processGalaxia: Galaxia.overwrite == False => not creating parameterfile')
                if os.path.isfile(parameterFileOut):
                    print('processGalaxia: parameterFileOut <',parameterFileOut,'> found => not creating parameterfile')

            filterMatch = fnmatch.filter(os.listdir(outputDir), outputFile+'.ebf.*')
    #        print('filterMatch = ',filterMatch
            tmpFiles = [n for n in filterMatch if os.path.isfile(os.path.join(outputDir, n))]
#            print('outputFile = ',outputFile,': len(tmpFiles) = ',len(tmpFiles),': tmpFiles = ',tmpFiles
            ebfFileName = os.path.join(outputDir, outputFile+'.ebf')
            done = ebfFileName in Galaxia.done
            if done:
                print('ebfFileName = <'+ebfFileName+'> already done')
            print('processGalaxia: outputFile = ',outputFile,': calculating: parameterFileOut = ',parameterFileOut)
            if (Galaxia.overwrite
                or (not os.path.isfile(ebfFileName))
                or (os.path.isfile(ebfFileName)
                    and len(tmpFiles) > 0)):
                if Galaxia.doIt:
                    args = ['galaxia', '-r', parameterFileOut]
                    rv = subprocess.call(args)
                    if rv == 1:
                        print("processGalaxia: longitude=%d, latitude=%d processed." % (lon, lat))
                    else:
                        print("processGalaxia: Error when processing file longitude=%d, latitude=%d: error code = %d" % (lon, lat, rv))
                else:
                    print('processGalaxia: Galaxia.doIt == False = not running galaxia')
            else:
                if not Galaxia.overwrite:
                    print('processGalaxia: Galaxia.overwrite == false => not running galaxia')
                if os.path.isfile(ebfFileName):
                    print("processGalaxia: galaxia output file ",ebfFileName," found => not running galaxia")
                if (os.path.isfile(ebfFileName)
                    and len(tmpFiles) == 0):
                    print("processGalaxia: galaxia output file ",ebfFileName," found and no temp files => not running galaxia")
    #        if not os.path.isfile(os.path.join(outputDir, outputFile+'.ebf')):
    #            print("ERROR: file <",os.path.join(outputDir, outputFile+'.ebf'),"> not found"
    #            STOP
            if Galaxia.overwrite or (not done):
                if Galaxia.doCSV:
                    if Galaxia.deleteOldXYFiles:
                        for filename in glob(os.path.join(xyOutputDir,"*.csv")):
                            os.remove(filename)
                    nLines = len(ebf.read(ebfFileName, '/px'))
                    lonStart = lon-5
                    lonEnd = lon+5
                    if (lon < 0):
                        lonStart += 360.0
                        lonEnd += 360.0
                    latStart = lat-5
                    latEnd = lat+5
    #                print('lonStart = ',lonStart,', lonEnd = ',lonEnd,', latStart = ',latStart,', latEnd = ',latEnd
                    cache = 100000

                    nStarsWritten = 0
                    if Galaxia.doIt:
                        data = ebf.iterate(ebfFileName, '/px+', cache)

                        iIter = 0
    #                        ebfFileNameOut = os.path.join(ebfOutputDir, outputFile+'.ebf')
    #                        try:
    #                            ebf.initialize(ebfFileNameOut)
    #                        except Exception as e:
    #                            print("processGalaxia: Unexpected error initalizing ",ebfFileNameOut,": ",str(e)

                        durationAll = 0.0
                        nLinesRead = 0;
                        for it in data:
                            nLinesRead += cache
                            timeStartIt = time.time()
                            self.addXYandPMandAbs2App(it)

                            window = hammer2.Pixel()
                            window.xLow = lonStart
                            window.xHigh = lonEnd
                            window.yLow = latStart
                            window.yHigh = latEnd

                            self.getStarsInWindow(it, window)
                            print("processGalaxia: len(it['px']) = ",len(it['px']))
    #                            print('processGalaxia: it.keys() = ',it.keys()
    #                            print('processGalaxia: data.keys() = ',data.keys()
    #                            try:
    #                                for key in it.keys():
    #                                    print('processGalaxia: key = ',key
    #                                    ebf.write(ebfFileNameOut, '/'+key, it[key], 'a')
    #                            except Exception as e:
    #                                print("processGalaxia: Unexpected error writing to ",ebfFileNameOut,": ",str(e)

                            csv = self.getCSVData(it, ebfFileName, iIter)
    #                            for iStar in range(csv.size()):
    #                                print('lon[',iStar,'] = ',csv.getData('glon',iStar),', lat[',iStar,'] = ',csv.getData('glat',iStar),': hammerX[',iStar,'] = ',csv.getData('hammerX',iStar),', hammerY[',iStar,'] = ',csv.getData('hammerY',iStar)
                            doFind = False
                            lockSuffix = Galaxia.lockSuffix + lonLatStr

                            for filename in glob(os.path.join('/Users/azuri/lock/',"lock*"+lockSuffix)):
                                os.remove(filename)

                            nStarsWritten += moveStarsToXY2.appendCSVDataToXYFiles(csv,
                                                                                  Galaxia.pixels,
                                                                                  'galaxia',
                                                                                  Galaxia.ids,
                                                                                  doFind,
                                                                                  lockSuffix,
                                                                                  xyOutputDir)
                            timeEnd = time.time()
                            duration = timeEnd-timeStartIt
                            durationAll += duration
                            print('ran file <',ebfFileName,'> iIter=',iIter,' in ',int(duration),' s: ',nLinesRead * 100.0 / nLines,' % done in ',int(durationAll),' seconds')
                            iIter += 1
                        print(nStarsWritten,' stars written')
                                    #STOP
                    else:
                        print('not actually doing anything')

                if os.path.exists(ebfFileName):
                    Galaxia.ebfFilesWritten.append(ebfFileName)
                    with open(Galaxia.progressFile, 'a+') as f:
                            f.write(ebfFileName+'\n')
#                os.remove(ebfFileName)

            timeEnd = time.time()
            duration = timeEnd-timeStart
            print('ran file <',ebfFileName,'> in ',int(duration),' s')

    def aebv_factor(filterName):
        if filterName == 'Landolt U':#LamEff = 3372, A/A(V) = 1.664
            return 5.434
        elif filterName == 'Landolt B':#LamEff = 4404, A/A(V) = 1.321
            return  4.315
        elif filterName == 'Landolt V':#LamEff = 5428, A/A(V) = 1.015
            return 3.315
        elif filterName == 'Landolt R':#LamEff =            6509    , A/A(V) = 0.819
            return 2.673
        elif filterName == 'Landolt I':#LamEff =           8090    , A/A(V) = 0.594   
            return 1.940
        elif filterName == 'CTIO U':#LamEff =              3683    , A/A(V) = 1.521   
            return 4.968
        elif filterName == 'CTIO B':#LamEff =              4393    , A/A(V) = 1.324   
            return 4.325
        elif filterName == 'CTIO V':#LamEff =             5519    , A/A(V) = 0.992   
            return 3.240
        elif filterName == 'CTIO R':#LamEff =             6602    , A/A(V) = 0.807   
            return 2.634
        elif filterName == 'CTIO I':#LamEff =              8046    , A/A(V) = 0.601   
            return 1.962
        elif filterName == 'UKIRT J':#LamEff =            12660    , A/A(V) = 0.276   
            return 0.902
        elif filterName == 'UKIRT H':#LamEff =            16732    , A/A(V) = 0.176   
            return 0.576
        elif filterName == 'UKIRT K':#LamEff =            22152    , A/A(V) = 0.112   
            return 0.367
        elif filterName == "UKIRT L'":#LamEff =           38079    , A/A(V) = 0.047   
            return 0.153
        elif filterName == "Gunn g":#LamEff =              5244    , A/A(V) = 1.065   
            return 3.476
        elif filterName == "Gunn r":#LamEff =              6707    , A/A(V) = 0.793   
            return 2.590
        elif filterName == "Gunn i":#LamEff =              7985    , A/A(V) = 0.610   
            return 1.991
        elif filterName == "Gunn z":#LamEff =              9055    , A/A(V) = 0.472   
            return 1.540
        elif filterName == "Spinrad R":#LamEff =           6993    , A/A(V) = 0.755   
            return 2.467
        elif filterName == "APM b_J":#LamEff =             4690    , A/A(V) = 1.236   
            return 4.035
        elif filterName == "Stromgren u":#LamEff =         3502    , A/A(V) = 1.602   
            return 5.231
        elif filterName == "Stromgren b":#LamEff =         4676    , A/A(V) = 1.240   
            return 4.049
        elif filterName == "Stromgren v":#LamEff =         4127    , A/A(V) = 1.394   
            return 4.552
        elif filterName == "Stromgren beta":#LamEff =      4861    , A/A(V) = 1.182   
            return 3.858
        elif filterName == "Stromgren y":#LamEff =         5479    , A/A(V) = 1.004   
            return 3.277
        elif filterName == "Sloan u'":#LamEff =            3546    , A/A(V) = 1.579   
            return 5.155
        elif filterName == "Sloan g'":#LamEff =            4925    , A/A(V) = 1.161   
            return 3.793
        elif filterName == "Sloan r'":#LamEff =            6335    , A/A(V) = 0.843   
            return 2.751
        elif filterName == "Sloan i'":#LamEff =            7799    , A/A(V) = 0.639   
            return 2.086
        elif filterName == "Sloan z'":#LamEff =            9294    , A/A(V) = 0.453   
            return 1.479
        elif filterName == "WFPC2 F300W":#LamEff =         3047    , A/A(V) = 1.791   
            return 5.849
        elif filterName == "WFPC2 F450W":#LamEff =         4711    , A/A(V) = 1.229   
            return 4.015
        elif filterName == "WFPC2 F555W":#LamEff =         5498    , A/A(V) = 0.996   
            return 3.252
        elif filterName == "WFPC2 F606W":#LamEff =         6042    , A/A(V) = 0.885   
            return 2.889
        elif filterName == "WFPC2 F702W":#LamEff =        7068    , A/A(V) = 0.746   
            return 2.435
        elif filterName == "WFPC2 F814W":#LamEff =         8066    , A/A(V) = 0.597   
            return 1.948
        elif filterName == "DSS-II g":#LamEff =            4814    , A/A(V) = 1.197   
            return 3.907
        elif filterName == "DSS-II r":#LamEff =            6571    , A/A(V) = 0.811   
            return 2.649
        elif filterName == "DSS-II i":#LamEff =            8183    , A/A(V) = 0.580   
            return 1.893
        else:
            raise "aebv_factor: ERROR: Could not find filterName ",filterName)
