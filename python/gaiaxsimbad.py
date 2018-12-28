#!/usr/bin/env python
import csv
import csvData
import csvFree
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model

#parameters
highExtinction = False
distRange = [0, 1000.]

# high extinction fields:
if highExtinction:
    fnameTest = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2xSimbad/xy/GaiaXSimbad_-0.000000-0.017678_-0.000000-0.017678.csv'
    fname = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2xSimbad/xy/GaiaXSimbad_-0.000000-0.017678_0.017678-0.035355.csv'
else:
# low extinction fields
    fname = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2xSimbad/xy/GaiaXSimbad_-0.000000-0.017678_-1.414214--1.396536.csv'
#    fnameTest = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2xSimbad/xy/GaiaXSimbad_-0.000000-0.017678_-1.396536--1.378858.csv'
    fnameTest = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2xSimbad/xy/GaiaXSimbad_-0.017678--0.000000_-1.414214--1.396536.csv'

fnameGaiaRoot = '/Volumes/obiwan/azuri/data/gaia/xy/GaiaSource_'

def crossMatch(simbadFile, gaiaFile):
    simbadData = csvFree.readCSVFile(simbadFile)
    gaiaData = csvFree.readCSVFile(gaiaFile)

    outData = csvFree.crossMatch(simbadData, gaiaData, 'source_id')
    print('crossMatch: found ',outData.size(),' matching stars out of ',simbadData.size(),' stars in Simbad catalogue and ',gaiaData.size(),' stars in GAIA catalogue')
    return outData

# data: dictionary
def getGoodStarIndices(data, distRange=[0.,1000.]):
    goodStars = []

    b = data.getData('B')
    v = data.getData('V')
    r = data.getData('R')
    g_bp = data.getData('phot_bp_mean_mag')
    dist = data.getData('angDist')
    logg = data.getData('a_g_val')
    print('a_g_val = ',logg)

    for i in range(data.size()):
        if (b[i] != '') and (v[i] != '') and (r[i] != '') and (g_bp[i] != '') and (dist[i] != '') and (logg[i] != ''):
            if (float(dist[i]) >= distRange[0]) and (float(dist[i]) < distRange[1]):
                goodStars.append(i)
    return goodStars

# return x=[B, V, R, 1.0] and y='phot_bp_mean_mag' of stars in distance range between distRange[0] and distRange[1]
# data: dictionary of all stars
# indices: which stars to look at
# distRange: range of distances
def getXY(data, indices, distRange=[0.,1000.]):
    x = []
    y = []
    for i in range(len(indices)):
        if (float(data.getData('angDist', indices[i])) >= distRange[0]) and (float(data.getData('angDist', indices[i])) < distRange[1]):
            x.append([float(data.getData('B', indices[i])),
                      float(data.getData('V', indices[i])),
                      float(data.getData('R', indices[i])),
                      1.0])
            y.append(float(data.getData('phot_bp_mean_mag', indices[i])))
    print 'len(x) = ',len(x)
    print 'len(y) = ',len(y)
    return [x,y]

#
def calcY(xs, coeffs):
    yOut = []
    for i in range(len(xs)):
        y = 0.0
        for iCoeff in range(len(coeffs)):
            y += xs[i][iCoeff] * coeffs[iCoeff]
        yOut.append(y)
    return yOut

def getPixel(fName):
    pixel = fName[fName.rfind('d_')+2:fName.rfind('.csv')]
    return pixel

#giant stars have B-V < 1, dwarfs have B-V > 1
#data: dictionary
#return: indices of dwarfs and giants
def getGiantsAndDwarfs(data, indices):
    dwarfs = []
    giants = []
    for i in range(len(indices)):
        if float(data.getData('rv_template_logg', indices[i])) < 3.5:
            giants.append(indices[i])
        else:
            dwarfs.append(indices[i])
    print 'len(dwarfs) = ',len(dwarfs)
    print 'len(giants) = ',len(giants)
    return [dwarfs,giants]

"""read data file"""
print('reading file <'+fname+'>')
#dat = csvFree.readCSVFile(fname)
fnameGaia = fnameGaiaRoot+getPixel(fname)+'.csv'
dat = crossMatch(fname, fnameGaia)
print('dat.header = ',dat.header)
#print dat.getData('phot_bp_mean_mag')[0:]

"""get indices of stars which have data for B, V, R, and G_BP"""
print('searching for stars with all needed parameters')
goodStars = getGoodStarIndices(dat, distRange)
print 'found ',len(goodStars),' good stars'

"""stars we fit"""
print('searching for dwarfs and giants')
dwarfs, giants = getGiantsAndDwarfs(dat, goodStars)

"""stars in the test field"""
print('reading test field')
datTest = csvFree.readCSVFile(fnameTest)
goodStarsTest = getGoodStarIndices(datTest, distRange)
dwarfs_test, giants_test = getGiantsAndDwarfs(datTest, goodStarsTest)


"""fit G_BP as a function of B, V, and R"""
for stars in ['dwarfs', 'giants']:
    if stars == 'darfs':
        indices = dwarfs
    else:
        indices = giants
    x,y = getXY(dat, indices, distRange)

    #clf = linear_model.LinearRegression(fit_intercept=False, normalize=False, copy_X=True)
    #clf.fit(x, y)
    clf = np.linalg.lstsq(x,y)#[0]
    #print 'dir(clf) = ',dir(clf)
    #print 'type(clf) = ',type(clf)
    #print 'clf = ',clf
    coeffs = clf[0]
    print '============================== coeffs = ',coeffs
    #print 'clf.get_params = ',clf.get_params

    if True:
        """check fit on our input data"""
        yCalc = calcY(x, clf[0])
        yDiff = np.array(y) - np.array(yCalc)
        print 'len(yDiff) = ',len(yDiff)
        print 'yDiff = ',yDiff
        mean = np.mean(yDiff)
        stdev = np.std(yDiff)
        print 'mean = ',mean,', stdev = ',stdev
        dist = []
        for i in range(len(indices)):
            dist.append(float(dat.getData('angDist', indices[i])))
    #    plt.xlabel('angular distance')
    #    plt.ylabel('G_BP difference')
    #    plt.show()


    if True:
        """check fit on neighbouring field"""

        if stars == 'dwarfs':
            indicesTest = dwarfs_test
        else:
            indicesTest = giants_test

        xTest, yTest = getXY(datTest, indicesTest, distRange)
        print 'yTest = ',yTest
        yCalc = calcY(xTest, clf[0])
        print 'yCalc = ',yCalc
        yDiffTest = np.array(yTest) - np.array(yCalc)
        print 'yDiffTest = ',yDiffTest
        mean = np.mean(yDiffTest)
        stdev = np.std(yDiffTest)
        print 'mean = ',mean,', stdev = ',stdev

        distTest = []
        for i in range(len(indicesTest)):
            distTest.append(float(datTest.getData('angDist', indicesTest[i])))
        plt.scatter(dist, yDiff, c='b')
        print('len(distTest) = ',len(distTest))
        print('len(yDiffTest) = ',len(yDiffTest))
        plt.scatter(distTest, yDiffTest, c='g')
        plt.xlabel('angular distance')
        plt.ylabel('G_BP difference')
        plt.title(stars)
        plt.show()
