#!/usr/bin/env python
import csv
import csvData
import csvFree
import hammer
import matplotlib.pyplot as plt
import numpy as np
import os
from sklearn import linear_model

def crossMatch(simbadFile, gaiaFile):
    simbadData = csvFree.readCSVFile(simbadFile)
    print('simbadData.header = ',simbadData.header)
    gaiaData = csvFree.readCSVFile(gaiaFile)
    print('gaiaData.header = ',gaiaData.header)

    outData = csvFree.crossMatch(simbadData, gaiaData, 'source_id')
    print('crossMatch: found ',outData.size(),' matching stars out of ',simbadData.size(),' stars in Simbad catalogue and ',gaiaData.size(),' stars in GAIA catalogue')
    return outData

# data: dictionary
#def getGoodStarIndices(data, distRange=[0.,1000.]):
#    goodStars = []

#    b = data.getData('B')
#    print('b = ',b)
#    v = data.getData('V')
#    print('v = ',v)
#    r = data.getData('R')
#    print('r = ',r)
#    g_bp = data.getData('phot_bp_mean_mag')
#    print('g_bp = ',g_bp)
#    dist = data.getData('angDist')
#    print('dist = ',dist)
#    logg = data.getData('rv_template_logg')
#    print('logg = ',logg)

#    for i in range(data.size()):
#        if (b[i] != '') and (v[i] != '') and (r[i] != '') and (g_bp[i] != '') and (dist[i] != '') and (logg[i] != ''):
#            if (float(dist[i]) >= distRange[0]) and (float(dist[i]) < distRange[1]):
#                goodStars.append(i)
#    return goodStars

# return x=[B, V, R, 1.0] and y='phot_bp_mean_mag' of stars in distance range between distRange[0] and distRange[1]
# data: dictionary of all stars
# indices: which stars to look at
# distRange: range of distances
def getXY(data, indices, xKeywords, yKeyword, distRange=[0.,10000.],nDegree=1):
    x = []
    y = []
    print('len(indices) = ',len(indices))
    for i in range(len(indices)):
        if (float(data.getData('angDist', indices[i])) >= distRange[0]) and (float(data.getData('angDist', indices[i])) < distRange[1]):
            tmp = [1]
            for keyword in xKeywords:
                xTemp = float(data.getData(keyword, indices[i]))
                for iDeg in np.arange(1,nDegree+1):
                    tmp.append(xTemp ** iDeg)
            x.append(tmp)
            y.append(float(data.getData(yKeyword, indices[i])))
    print('len(x) = ',len(x))
    print('len(y) = ',len(y))
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
#        print('data.getData(rv_tempate_logg, ',indices[i],') = ',data.getData('rv_template_logg', indices[i]))
        if float(data.getData('rv_template_logg', indices[i])) < 3.5:
            giants.append(indices[i])
        else:
            dwarfs.append(indices[i])
    print('len(dwarfs) = ',len(dwarfs))
    print('len(giants) = ',len(giants))
    return [dwarfs,giants]

#"""cross-match (Simbad x Gaia) with GAIA DR2"""
#print('reading file <'+fname+'>')
##dat = csvFree.readCSVFile(fname)
#fnameGaia = fnameGaiaRoot+getPixel(fname)+'.csv'
#dat = crossMatch(fname, fnameGaia)
##print('dat.header = ',dat.header)
##print dat.getData('phot_bp_mean_mag')[0:]

#"""get indices of stars which have data for B, V, R, and G_BP"""
#print('searching for stars with all needed parameters')
#goodStars = getGoodStarIndices(dat, distRange)
#print 'found ',len(goodStars),' good stars'

#"""stars in the test field"""
#print('reading test field')
#fnameGaia = fnameGaiaRoot+getPixel(fnameTest)+'.csv'
#datTest = crossMatch(fnameTest, fnameGaia)
#goodStarsTest = getGoodStarIndices(datTest, distRange)
#dwarfs_test, giants_test = getGiantsAndDwarfs(datTest, goodStarsTest)

def run():

    #parameters
    highExtinction = False
    distRange = [0.0, 1000000.0]
    if True:
#    for withSquares in [False, True]:

        # high extinction fields:
        if highExtinction:
            #'GaiaXSimbad_-1.255114--1.237437_-0.017678--0.000000.csv'
            #'GaiaXSimbad_-0.000000-0.017678_-0.035355--0.017678.csv','GaiaXSimbad_-0.000000-0.017678_-0.053033--0.035355.csv','GaiaXSimbad_-0.000000-0.017678_-0.070711--0.053033.csv'
            fnameTest = '/Volumes/external/azuri/data/gaia/x-match/GaiaDR2xSimbad/xy/GaiaXSimbad_1.449569-1.467247_-0.000000-0.017678.csv'
            fname = '/Volumes/external/azuri/data/gaia/x-match/GaiaDR2xSimbad/xy/GaiaXSimbad_1.449569-1.467247_-0.017678--0.000000.csv'
        else:
        # low extinction fields
            #fname = '/Volumes/external/azuri/data/gaia/x-match/GaiaDR2xSimbad/xy/GaiaXSimbad_0.813173-0.830850_0.707107-0.724784.csv'
            #fnameTest = '/Volumes/external/azuri/data/gaia/x-match/GaiaDR2xSimbad/xy/GaiaXSimbad_1.007627-1.025305_-0.494975--0.477297.csv'
            #'GaiaXSimbad_0.176777-0.194454_1.272792-1.290470.csv'
            #'GaiaXSimbad_0.017678-0.035355_-0.070711--0.053033.csv'
            fname = '/Volumes/external/azuri/data/gaia/x-match/GaiaDR2xSimbad/xy/GaiaXSimbad_-1.219759--1.202081_-0.583363--0.565685.csv'
            fnameTest = '/Volumes/external/azuri/data/gaia/x-match/GaiaDR2xSimbad/xy/GaiaXSimbad_-1.219759--1.202081_-0.601041--0.583363.csv'
            #'GaiaXSimbad_-1.202081--1.184404_-0.583363--0.565685.csv', 'GaiaXSimbad_-1.202081--1.184404_-0.601041--0.583363.csv', 'GaiaXSimbad_-1.202081--1.184404_-0.618718--0.601041.csv'
            #'GaiaXSimbad_-1.184404--1.166726_-0.601041--0.583363.csv','GaiaXSimbad_-1.184404--1.166726_-0.618718--0.601041.csv','GaiaXSimbad_-1.184404--1.166726_-0.636396--0.618718.csv'
            #'GaiaXSimbad_-0.795495--0.777817_-0.760140--0.742462.csv','GaiaXSimbad_-0.795495--0.777817_-0.777817--0.760140.csv','GaiaXSimbad_-0.795495--0.777817_-0.795495--0.777817.csv'
            #'GaiaXSimbad_-0.777817--0.760140_-0.760140--0.742462.csv','GaiaXSimbad_-0.777817--0.760140_-0.777817--0.760140.csv','GaiaXSimbad_-0.777817--0.760140_-0.795495--0.777817.csv'
            #'GaiaXSimbad_-0.760140--0.742462_-0.777817--0.760140.csv','GaiaXSimbad_-0.760140--0.742462_-0.795495--0.777817.csv'
        #    fname = '/Volumes/external/azuri/data/gaia/x-match/GaiaDR2xSimbad/xy/GaiaXSimbad_0.282843-0.300520_-1.166726--1.149049.csv'
        #    fnameTest = '/Volumes/external/azuri/data/gaia/x-match/GaiaDR2xSimbad/xy/GaiaXSimbad_-0.000000-0.017678_-1.396536--1.378858.csv'
        #    fnameTest = '/Volumes/external/azuri/data/gaia/x-match/GaiaDR2xSimbad/xy/GaiaXSimbad_0.282843-0.300520_-1.149049--1.131371.csv'

        fnameGaiaXSimbadRoot = '/Volumes/external/azuri/data/gaia/x-match/GaiaDR2xSimbad/xy/GaiaXSimbad_%.6f-%.6f_%.6f-%.6f'
        #fnameGaiaRoot = '/Volumes/external/azuri/data/gaia/dr2/xy/GaiaSource_'
        ham = hammer.Hammer()
        pixels = ham.getPixels()

        """fit G_BP as a function of B, V, and R"""
        xKeyWords = [['B','V','R'],['g','r'],['r','i','z'],['g','r','i','z'],['R','I'],['B','V','R','I'],]#
        yKeyWords = ['phot_bp_mean_mag', 'phot_bp_mean_mag', 'phot_rp_mean_mag','phot_g_mean_mag','phot_rp_mean_mag', 'phot_g_mean_mag',]#
        resultFile = '/Volumes/external/azuri/data/gaia/x-match/GaiaDR2xSimbad/gaiaxsimbad_results.txt'
#        with open(resultFile,'a') as f:
        if True:
            for iKey in range(len(yKeyWords)):
                xKeys = xKeyWords[iKey]
                yKey = yKeyWords[iKey]
                dat = None
                datTest = None
                k = 0.
                for pixel in pixels:
                    fname = fnameGaiaXSimbadRoot % (pixel.xLow, pixel.xHigh, pixel.yLow, pixel.yHigh)
                    if yKey == 'phot_g_mean_mag':
                        fname = os.path.join(os.path.join(fname[0:fname.rfind('/')],'temp'),fname[fname.rfind('/')+1:])
                    print('fname = <'+fname+'>')
                    print('xKeys = ',xKeys)
                    for key in xKeys:
                        print('key = ',key)
                        fname = fname + '_' + key
                    fname = fname + '_' + yKey + '_rv_template_logg.csv'
                    print('fname = <'+fname+'>')
                    if os.path.isfile(fname):
                        if k / 10. == int(k/10.):#use as test data
                            if datTest == None:
                                datTest = csvFree.readCSVFile(fname)
                            else:
                                datTest.append(csvFree.readCSVFile(fname))
                        else:
                            if dat == None:
                                dat = csvFree.readCSVFile(fname)
                            else:
                                dat.append(csvFree.readCSVFile(fname))
                        k += 1.

                fnameOut = '/Volumes/external/azuri/data/gaia/x-match/GaiaDR2xSimbad/xy/allStars'
                for key in xKeys:
                    fnameOut = fnameOut + '_' + key
                fnameOut = fnameOut + '_' + yKey + '_rv_template_logg.csv'

                datOut = dat
                datOut.append(datTest)
                csvFree.writeCSVFile(datOut, fnameOut)
                datOut = None

                """stars we fit"""
                print('searching for dwarfs and giants')
                dwarfs, giants = getGiantsAndDwarfs(dat, range(dat.size()))
                dwarfs_test, giants_test = getGiantsAndDwarfs(datTest, range(datTest.size()))
                print('len(dwarfs) = ',len(dwarfs))
                print('len(giants) = ',len(giants))
                print('len(dwarfs_test) = ',len(dwarfs_test))
                print('len(giants_test) = ',len(giants_test))

                for degree in np.arange(1,6):
                    for stars in ['dwarfs', 'giants']:
                        print('Calculating '+stars)
                        if stars == 'dwarfs':
                            indices = dwarfs
                            print('indices set to dwarfs')
                        else:
                            indices = giants
                            print('indices set to giants')
            #            print('indices = ',indices)
                        x,y = getXY(dat, indices, xKeys, yKey, distRange, degree)
                        print('len(x) = ',len(x),', len(y) = ',len(y))

                        #clf = linear_model.LinearRegression(fit_intercept=False, normalize=False, copy_X=True)
                        #clf.fit(x, y)
                        clf = np.linalg.lstsq(x,y)#[0]
                        #print 'dir(clf) = ',dir(clf)
                        #print 'type(clf) = ',type(clf)
                        #print 'clf = ',clf
                        coeffs = clf[0]
                        print('============================== coeffs = ',coeffs)
                        #print 'clf.get_params = ',clf.get_params

                        if True:
                            """check fit on our input data"""
                            yCalc = calcY(x, clf[0])
                            yDiff = np.array(y) - np.array(yCalc)
                            print('len(yDiff) = ',len(yDiff))
                            #print 'yDiff = ',yDiff
                            mean = np.mean(yDiff)
                            stdev = np.std(yDiff)
                            print('mean = ',mean,', stdev = ',stdev)
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
                            print('testing '+stars+' with ',len(indicesTest),' stars')

                            xTest, yTest = getXY(datTest, indicesTest, xKeys, yKey, distRange, degree)
                            #print 'yTest = ',yTest
                            yCalc = calcY(xTest, clf[0])
                            #print 'yCalc = ',yCalc
                            yDiffTest = np.array(yTest) - np.array(yCalc)
                            #print 'yDiffTest = ',yDiffTest
                            mean = np.mean(yDiffTest)
                            stdev = np.std(yDiffTest)
                            print('test mean = ',mean,', stdev = ',stdev)

                            distTest = []
                            for i in range(len(indicesTest)):
                                distTest.append(float(datTest.getData('angDist', indicesTest[i])))
                            plt.scatter(dist, yDiff, c='b', s=3)
            #                print('len(distTest) = ',len(distTest))
            #                print('len(yDiffTest) = ',len(yDiffTest))
                            plt.scatter(distTest, yDiffTest, c='g', s=3)
                            plt.xlabel('angular distance')
                            if yKey == 'phot_bp_mean_mag':
                                plt.ylabel('G_BP difference (measured - calcuated)')
                            elif yKey == 'phot_rp_mean_mag':
                                plt.ylabel('G_RP difference (measured - calcuated)')
                            title = stars+' '+str(degree)
                            if degree == 1:
                                title += 'st'
                            elif degree == 2:
                                title += 'nd'
                            elif degree == 3:
                                title += 'rd'
                            else:
                                title += 'th'
                            title += ' degree polynomial'
                            plt.title(title)
                            plotname = '/Volumes/external/azuri/data/gaia/x-match/GaiaDR2xSimbad/'
                            for xKey in xKeys:
                                plotname += xKey
                            plotname += '_'+yKey+'_'+stars
                            plotname += '_'+str(degree)+'degree'
                            plotname += '.pdf'
                            plt.savefig(plotname, format='pdf', frameon=False, bbox_inches='tight', pad_inches=0.1)
                            plt.show()

                            plt.scatter(yTest, yCalc, c='b', s=3)
                            plt.plot([np.min(yTest)-0.5, np.max(yTest)+0.5],[np.min(yTest)-0.5, np.max(yTest)+0.5])
                            plt.xlim([np.min(yTest)-0.5, np.max(yTest)+0.5])
                            plt.ylim([np.min(yTest)-0.5, np.max(yTest)+0.5])
            #                print('len(distTest) = ',len(distTest))
            #                print('len(yDiffTest) = ',len(yDiffTest))
            #                plt.scatter(distTest, yDiffTest, c='g')
                            if yKey == 'phot_bp_mean_mag':
                                plt.xlabel('G_BP measured')
                                plt.ylabel('G_BP calcuated')
                            elif yKey == 'phot_rp_mean_mag':
                                plt.xlabel('G_RP measured')
                                plt.ylabel('G_RP calcuated')
                            else:
                                plt.xlabel('G measured')
                                plt.ylabel('G calcuated')
                            title = stars+' '+str(degree)
                            if degree == 1:
                                title += 'st'
                            elif degree == 2:
                                title += 'nd'
                            elif degree == 3:
                                title += 'rd'
                            else:
                                title += 'th'
                            title += ' degree polynomial'
                            plt.title(title)
                            plotname = '/Volumes/external/azuri/data/gaia/x-match/GaiaDR2xSimbad/'
                            for xKey in xKeys:
                                plotname += xKey
                            plotname += '_'+yKey+'_'+stars
                            plotname += '_'+str(degree)+'th-degree'
                            plotname += '_calc_vs_Gaia.pdf'
                            plt.savefig(plotname, format='pdf', frameon=False, bbox_inches='tight', pad_inches=0.1)
                            plt.show()

                            outLine = plotname
                            if degree == 1:
                                plotname += ' 1st'
                            elif degree == 2:
                                plotname += ' 2nd'
                            else:
                                plotname += ' '+str(degree)+'th'
                            plotname += ' degree'
                            outLine += ': '+str(len(x))+' stars, '+str(len(xTest))+' test stars:'
                            outLine += ' coeffs=['
                            for iCoeff in np.arange(0,len(clf[0])):
                                outLine += str(clf[0][iCoeff])+', '
                            outLine += ' mean difference = '+str(mean)+', stddev = '+str(stdev)+'\n'
                            print('writing outLine = <'+outLine+'> to file <'+resultFile+'>')
                            with open(resultFile,'a') as f:
                                f.write(outLine)

if False:
    run()