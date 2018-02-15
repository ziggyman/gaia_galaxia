from glob import glob
import os
import shutil
import sys

from runGalaxia import Galaxia
from utils import mkdir_p

def main(argv):
#    dir = '/Volumes/yoda/azuri/data/galaxia/ubv_Vlt21_5_fsample100'
    dir = '/Volumes/yoda/azuri/data/galaxia/ubv_Vlt21_5_fsample50'
    print 'looking for ebf files in <'+dir+'>'
    for filename in glob(os.path.join(dir, 'galaxia*.ebf')):
        print 'filename = ',filename
        f = filename[filename.rfind('/')+1 :]
        print 'f = ',f
        startPos = f.find('_')+1
        endPos = f.rfind('_')
        print 'startPos for lon = ',startPos,', endPos = ',endPos
        lon = f[startPos : endPos]
        print 'lon = ',lon
        startPos = f.rfind('_')+1
        endPos = f.rfind('.')
        print 'startPos for lat = ',startPos,', endPos = ',endPos
        lat = f[startPos:endPos]
        print 'lat = ',lat

        lonLatStr = lon+'_'+lat
        outDir = os.path.join(Galaxia.dir, lonLatStr)
        print 'moving <'+filename+'> to <'+outDir+'>'
        mkdir_p(outDir)

        outFile = os.path.join(outDir, f)
        print 'moving <'+filename+'> to <'+outFile+'>'

        shutil.move(filename, outFile)

    for filename in glob(os.path.join(dir, 'parameterfile*')):
        print 'filename = ',filename
        f = filename[filename.rfind('/')+1 :]
        print 'f = ',f
        startPos = f.find('_')+1
        endPos = f.rfind('_')
        print 'startPos for lon = ',startPos,', endPos = ',endPos
        lon = f[startPos : endPos]
        print 'lon = ',lon
        startPos = f.rfind('_')+1
        print 'startPos for lat = ',startPos
        lat = f[startPos:]
        print 'lat = ',lat

        lonLatStr = lon+'_'+lat
        outDir = os.path.join(Galaxia.dir, lonLatStr)
        print 'moving <'+filename+'> to <'+outDir+'>'
        mkdir_p(outDir)

        outFile = os.path.join(outDir, f)
        print 'moving <'+filename+'> to <'+outFile+'>'

        shutil.move(filename, outFile)

if __name__ == '__main__':
    main(sys.argv)
