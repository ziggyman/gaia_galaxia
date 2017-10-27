# if error "too many files open" occurs:
# ulimit -n 1000
from astropy import units as u
from astropy.coordinates import SkyCoord
import ebf
import numpy as np
import os

def openOutFiles(keys):
    outFiles = []
    lonStart = []
    lonEnd = []
    latStart = []
    latEnd = []

    fileNameOut = os.path.join(dir,'galaxia_%d-%d_%d-%d.csv')

    iFile = 0
    for lon in np.arange(5,360,10):
        for lat in np.arange(-85,90,10):
            try:
                fileName = fileNameOut % (lon-5, lon+5, lat-5, lat+5)
                print 'iFile = ',iFile,': opening fileName = ,',fileName,'>'
                outFiles.append(open(fileName,'w'))
                lonStart.append(lon-5)
                lonEnd.append(lon+5)
                latStart.append(lat-5)
                latEnd.append(lat+5)
                outFiles[len(outFiles)-1].write(keys)
                iFile += 1
            except Exception as e:
                print 'iFile = ',iFile,': ',e.message
                raise
    return [outFiles, lonStart, lonEnd, latStart, latEnd]

def closeFiles(files):
    for file in files:
        close(file)

dir = '/Volumes/yoda/azuri/data/galaxia/sdss/'
fileToRead = os.path.join(dir,'galaxia_25_-5.ebf')

# print statistics
#ebf.info(fileToRead)

"""read one parameter + all other parameters with the same size in iterations"""
cache = 100
data = ebf.iterate(fileToRead, '/px+', cache)
keys = []
for it in data:
    keys = it.keys()
    break
print 'keys = ',keys

shouldHaveKeys = ['px', 'py', 'pz', 'vx', 'vy', 'vz', 'glon', 'glat', 'age',
                  'feh', 'alpha', 'smass', 'mag0', 'mag1', 'mag2', 'rad',
                  'popid', 'satid', 'fieldid', 'partid', 'center', 'log', 'teff',
                  'grav', 'mbol', 'photosys_band', 'exbv_schelegl',
                  'exbv_schlegel_inf', 'exbv_solar', 'mact', 'mtip']
for key in shouldHaveKeys:
    if key not in keys:
        print 'key <',key,'> not found in keys'

if len(keys) == 0:
    STOP
keyStr = keys[0]
for key in keys[1:]:
    keyStr += ','+key

outFiles, lonStarts, lonEnds, latStarts, latEnds = openOutFiles(keyStr)

data = ebf.iterate(fileToRead, '/px+', cache)

iIter = 0
for it in data:
    if iIter == 0:
        keys = it.keys()
        iIter = 1

    for iStar in range(len(it['px'])):
        x = it['px'][iStar]
        y = it['py'][iStar]
        z = it['pz'][iStar]
        print 'iStar = ',iStar,': len(it["px"]) = ',len(it['px'])

        c = SkyCoord(x=x, y=y, z=z, unit='kpc', representation='cartesian').galactic
        print 'c = ',c

        lon = c.l.deg
        lat = c.b.deg
        r = c.distance.kpc
        print 'lon = ',lon,', lat = ',lat,', r = ',r
        for iLon in range(len(lonStarts)):
            if ((lon >= lonStarts[iLon])
            and (lon < lonEnds[iLon])
            and (lat >= latStarts[iLon])
            and (lat < latEnds[iLon])):
                outString = str(it[keys[0]][iStar])
                for key in keys[1:]:
                    outString += ','+str(it[key][iStar])
                print 'iLon = ',iLon,': outString = <',outString,'>'
                STOP
#                outFiles[iLon].write(outString+'\n')

closeFiles(outFiles)
