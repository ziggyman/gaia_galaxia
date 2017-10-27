#! /usr/bin/env python

from astropy import units as u
from astropy.coordinates import SkyCoord
import ebf
import fnmatch
import gxutil
import os
import sys
import subprocess
from multiprocessing import Pool, Lock
import numpy as np

globallock = Lock()

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

def processGalaxia(lon):
    dir = '/Volumes/yoda/azuri/data/galaxia'
    outputDir = os.path.join(dir, 'sdss')
    parameterFileIn = os.path.join(dir, 'parameterfile')
    outputFile = ''
    fileNameOut = os.path.join(dir,'galaxia_%d-%d_%d-%d.csv')
    overwrite = True

    for lat in np.arange(-85, 90, 10):
        globallock.acquire()
        parameterFileOut = os.path.join(dir, 'parameterfile_%d_%d' % (lon, lat))
        surveyArea = 157.08

        # Read parameterfile
        with open(parameterFileIn, 'r') as fIn:
            with open(parameterFileOut, 'w') as fOut:
                for line in fIn:
                    words = line.split(' ')
                    parameterName = words[0]
                    parameterValue = words[len(words)-1]
                    if parameterName == 'outputFile':
                        outputFile = 'galaxia_%d_%d' % (lon, lat)
                        parameterValue = outputFile+'\n'
                    elif parameterName == 'longitude':
                        parameterValue = '%d\n' % lon
                    elif parameterName == 'latitude':
                        parameterValue = '%d\n' % lat
                    elif parameterName == 'surveyArea':
                        parameterValue = '%f\n' % surveyArea
                    fOut.write(parameterName+' '+parameterValue)

        filterMatch = fnmatch.filter(os.listdir(outputDir), outputFile+'.ebf.*')
        print 'filterMatch = ',filterMatch
        tmpFiles = [n for n in filterMatch if os.path.isfile(os.path.join(outputDir, n))]
        print 'outputFile = ',outputFile,': len(tmpFiles) = ',len(tmpFiles),': tmpFiles = ',tmpFiles
        if (overwrite
            or (not os.path.isfile(os.path.join(outputDir, outputFile+'.ebf')))
            or (os.path.isfile(os.path.join(outputDir, outputFile+'.ebf'))
                and len(tmpFiles) > 0)):
            print 'outputFile = ',outputFile,': calculating'

            args = ['galaxia', '-r', parameterFileOut]
            rv = subprocess.call(args)
            if rv == 1:
                print "longitude=%d, latitude=%d processed." % (lon, lat)
            else:
                print "Error when processing file longitude=%d, latitude=%d: error code = %d" % (lon, lat, rv)

        else:
            print 'outputFile = ',outputFile,': output file found and no tmp files => not calculating'

        """Add proper motions, radial velocity"""
        data = ebf.read(os.path.join(outputDir, outputFile+'.ebf'),'/')
        gxutil.append_pm(data)

        """convert absolute magnitudes to apparent ones"""
        gxutil.abs2app(data,corr=True)

        lonStart = lon-5
        lonEnd = lon+5
        latStart = lat-5
        latEnd = lat+5
        cache = 10000
        data = ebf.iterate(os.path.join(outputDir, outputFile+'.ebf'), '/px+', cache)

        keys = []
        for it in data:
            keys = it.keys()
            break
        print 'keys = ',keys
        keys.append('glon')
        keys.append('glat')
        keyStr = keys[0]
        for key in keys[1:]:
            keyStr += ','+key

        with open(fileNameOut % (lonStart, lonEnd, latStart, latEnd),'w') as csvFileOut:

            csvFileOut.write(keyStr)

            data = ebf.iterate(os.path.join(outputDir, outputFile+'.ebf'), '/px+', cache)

            iIter = 0
            for it in data:
                if iIter == 0:
                    keys = it.keys()
                    iIter = 1
                print 'type(it["px"]) = ',type(it['px']),': ',type(it['px'][0])
                it['glon'] = np.ndarray(len(it['px']), dtype=np.float32)
                it['glat'] = np.ndarray(len(it['px']), dtype=np.float32)

                for iStar in range(len(it['px'])):
                    x = it['px'][iStar]
                    y = it['py'][iStar]
                    z = it['pz'][iStar]
                    print 'iStar = ',iStar,': x = ',x,', y = ',y,', z = ',z

                    c = SkyCoord(x=x, y=y, z=z, unit='kpc', representation='cartesian').galactic
                    print 'c = ',c

                    a = np.degrees(np.arctan(z/np.sqrt(x*x+y*y)))
                    print 'a = ',a

                    it['glon'][iStar] = c.l.deg
                    it['glat'][iStar] = c.b.deg
#                    it['dist'][iStar] = c.distance.kpc
                    print 'lon = ',lon,', lat = ',lat,': glon = ',it['glon'][iStar],', glat = ',it['glat'][iStar],', dist = ',c.distance.kpc,': it["rad"][',iStar,'] = ',it['rad'][iStar]
                    if np.fabs(c.distance.kpc - it['rad'][iStar]) > 0.001:
                        print 'error: np.fabs(it["dist"][iStar] - it["rad"][iStar]) > 0.001'
                    if ((lon >= lonStart)
                        and (lon < lonEnd)
                        and (lat >= latStart)
                        and (lat < latEnd)):
                        outString = str(it[keys[0]][iStar])
                        for key in keys[1:]:
                            outString += ','+str(it[key][iStar])
                        print 'outString = <',outString,'>'
                        csvFileOut.write(outString+'\n')
                    STOP


        globallock.release()

def main(argv):
    """Main program.

    Arguments:
    argv -- command line arguments
    """
    p = Pool()
    lon = np.arange(5, 360, 10)
    print 'lon = ',lon
    p.map(processGalaxia, lon)
    p.close()

if __name__ == '__main__':
    main(sys.argv)
