from multiprocessing import Pool
import numpy as np
import os
import random

import csvFree, csvData
from gaiaCoordTrafo import properMotionLonLatToGal,rICRSTorGal,getICRSUnitVector,properMotionAlphaDeltaToICRS

path = '/Volumes/work/azuri/data/gaia/dr2/xy'
fileName = 'GaiaSource_-1.555635--1.537957_0.459619-0.477297.csv'
fileList = 'dataFileNames.txt'

def process(fileName):
    try:
        print('running on '+fileName)
        csv = csvFree.readCSVFile(os.path.join(path, fileName))
        print(csv.size())
        print(csv.header)

        xGalArr = []
        yGalArr = []
        zGalArr = []
        pmXGalArr = []
        pmYGalArr = []
        pmZGalArr = []
        for iStar in range(csv.size()):

            ra = float(csv.getData('ra',iStar))
            dec = float(csv.getData('dec',iStar))

    #        print('ra = ',ra,', dec = ',dec)

            xICRS,yICRS,zICRS = getICRSUnitVector(ra, dec)
    #        print('xICRS = ',xICRS,', yICRS = ',yICRS,', zICRS = ',zICRS)

            xGal,yGal,zGal = rICRSTorGal([xICRS,yICRS,zICRS])
    #        print('xGal = ',xGal,', yGal = ',yGal,', zGal = ',zGal)
            xGalArr.append('%.10f' % xGal)
            yGalArr.append('%.10f' % yGal)
            zGalArr.append('%.10f' % zGal)

            if csv.getData('pmra',iStar) != '':

    #            print("csv.getData('pmra',iStar) = <"+csv.getData('pmra',iStar)+'>')
                pmra = float(csv.getData('pmra',iStar))
                pmdec = float(csv.getData('pmdec',iStar))

                pmXICRS,pmYICRS,pmZICRS, = properMotionAlphaDeltaToICRS(ra, dec, pmra, pmdec)
    #            print('pmXICRS = ',pmXICRS,', pmYICRS = ',pmYICRS,', pmZICRS = ',pmZICRS)

                pmXGal,pmYGal,pmZGal = rICRSTorGal([pmXICRS,pmYICRS,pmZICRS])
    #            print('pmXGal = ',pmXGal,', pmYGal = ',pmYGal,', pmZGal = ',pmZGal)
                pmXGalArr.append('%.10f' % pmXGal)
                pmYGalArr.append('%.10f' % pmYGal)
                pmZGalArr.append('%.10f' % pmZGal)
            else:
    #            print('pmra is not a valid number')
                pmXGalArr.append('')
                pmYGalArr.append('')
                pmZGalArr.append('')

    #    print('xGalArr = ',xGalArr)
        csv.addColumn('xGal',xGalArr)
        csv.addColumn('yGal',yGalArr)
        csv.addColumn('zGal',zGalArr)

        csv.addColumn('pmXGal',pmXGalArr)
        csv.addColumn('pmYGal',pmYGalArr)
        csv.addColumn('pmZGal',pmZGalArr)

    #    print(csv.header)
        csvFree.writeCSVFile(csv,os.path.join(path,fileName))
        os.rename(os.path.join(path,fileName),os.path.join(path,fileName[:-4]+'_xyz.csv'))
        print('finished '+fileName)
    except:
        print('error on '+fileName)
        pass
    return csv

if __name__ == '__main__':
    with open(os.path.join(path, fileList),'r') as f:
        fileNames = f.readlines()
    print('fileNames = ',fileNames)
    newFileNames = [os.path.join(path,a.strip('\n')) for a in fileNames]
    print('newFileNames = ',newFileNames)

    p = Pool(processes=16)
    iCombo = np.arange(len(newFileNames))
    print('iCombo = ',iCombo)
    #gal.processGaiaXSimbad(iCombo[0])
    random.shuffle(iCombo)
    print('iCombo = ',iCombo)
    newFileNamesRandomized = [newFileNames[iCombo[i]] for i in iCombo]
    print(newFileNamesRandomized)
    p.map(process, newFileNamesRandomized)
    p.close()
