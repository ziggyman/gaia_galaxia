import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colorbar as cbar
import subprocess

import csvData
import csvFree
from hammer import Pixel,XY,LonLat,Hammer
from myUtils import plotLBMarks

resultsFile = '/Users/azuri/daten/illume_research/martin/results.csv'
results = csvFree.readCSVFile(resultsFile)

ham = Hammer()
pixels = ham.getPixels()
print('total number of pixels = ',len(pixels))

def plotHammerGrid():
    plotLBMarks(10)

def createPlot(cMap, c, normal, fNameOut):
    fig = plt.figure(figsize=(25,10))
    ax = fig.add_subplot(111)
    plt.axis('off')
#    STOP

    for iPix in range(results.size()):
#        print('differnce[',iPix,'] = ',difference[iPix],', color = ',c[iPix])
        #print('percentDiff[',iPix,'] = ',percentDiff[iPix],', color = ',c[iPix])
        rect1 = matplotlib.patches.Rectangle((float(results.getData('pixelxMin',iPix)), float(results.getData('pixelYMin',iPix))),
                                             float(results.getData('pixelXMax',iPix)) - float(results.getData('pixelxMin',iPix)),
                                             float(results.getData('pixelYMax',iPix)) - float(results.getData('pixelYMin',iPix)),
                                             facecolor = c[iPix],
                                             )

        ax.add_patch(rect1)

    cax, _ = cbar.make_axes(ax)
    cb2 = cbar.ColorbarBase(cax, cmap=cMap,norm=normal)
    ax.set_xlim(-2.82843, 2.82843)
    ax.set_ylim(-1.41421, 1.41421)
    if fNameOut is not None:
        print('plotHammerProjection: fNameOut = <'+fNameOut+'>')
        fNameOutTemp = fNameOut[:-3]+'.tmp.pdf'
        fig.savefig(fNameOutTemp, bbox_inches='tight')
        subprocess.run(["gs","-sDEVICE=pdfwrite","-dCompatibilityLevel=1.4","-dPDFSETTINGS=/ebook","-dNOPAUSE", "-dQUIET", "-dBATCH", "-sOutputFile="+fNameOut, fNameOutTemp])
        subprocess.run(["rm",fNameOutTemp])
    plt.show()
    plt.close(fig)
    print('after all_pne: ',plt.get_fignums(),' figures open')


def plotResults():


    cmap=plt.cm.jet
    for par in [['nStarsGaia','nStarsGalaxia'],['mean_pm_x_gaia','mean_pm_x_galaxia'],['mean_pm_y_gaia','mean_pm_y_galaxia'],['mean_pm_z_gaia','mean_pm_z_galaxia']]:
        dataGaia = np.nan_to_num(np.array(csvFree.convertStringVectorToDoubleVector(results.getData(par[0]))))
        dataGalaxia = np.nan_to_num(np.array(csvFree.convertStringVectorToDoubleVector(results.getData(par[1]))))
        difference = dataGalaxia - dataGaia
        #   maxDiff = np.amax(np.absolute(difference))
        percentDiff = 100. * difference / np.absolute(dataGalaxia)
        percentDiff = np.nan_to_num(percentDiff)
        maxPercentDiff = 100.#np.amax(np.absolute(percentDiff))
        print('percentDiff = ',percentDiff)
        print('maxPercentDiff = ',maxPercentDiff)
    #    normal = plt.Normalize(-maxDiff, maxDiff)
        normal = plt.Normalize(-maxPercentDiff, maxPercentDiff)
        print('normal = ',normal)

        print('cmap = ',cmap)
        print('dir(cmap) = ',dir(cmap))
    #    c = [cmap((diff / maxDiff) / 2. + 0.5) for diff in difference]#cmap(difference)
        c = [cmap((diff / maxPercentDiff) / 2. + 0.5) for diff in percentDiff]#cmap(difference)
        print('c = ', c[0:100])
        fNameOut = resultsFile[:-4]+par[1]+'-'+par[0]+'.pdf'
        createPlot(cmap, c, normal, fNameOut)

        max = np.amax(np.absolute(dataGaia))
        if 'mean_pm_x' in par[0]:
            max = 10.
        elif 'mean_pm_y' in par[0]:
            max = 10.
        elif 'mean_pm_z' in par[0]:
            max = 10.
        if 'nStars' in par[0]:
            normal = plt.Normalize(0, max)
        else:
            normal = plt.Normalize(-max, max)
        c = [cmap((diff / max) / 2. + 0.5) for diff in dataGaia]#cmap(difference)
        print('normal = ',normal)
        print('max = ',max)
        print('dataGaia[0:100] = ',dataGaia[0:100])
        print('c = ', c[0:100])
        fNameOut = resultsFile[:-4]+par[0]+'.pdf'
        createPlot(cmap, c, normal, fNameOut)

        max = np.amax(np.absolute(dataGalaxia))
        if 'mean_pm_x' in par[0]:
            max = 10.
        elif 'mean_pm_y' in par[0]:
            max = 10.
        elif 'mean_pm_z' in par[0]:
            max = 10.
        c = [cmap((diff / max) / 2. + 0.5) for diff in dataGalaxia]#cmap(difference)
        if 'nStars' in par[0]:
            normal = plt.Normalize(0, max)
        else:
            normal = plt.Normalize(-max, max)
        print('normal = ',normal)
        print('max = ',max)
        print('dataGalaxia[0:100] = ',dataGalaxia[0:100])
        print('c = ', c[0:100])
        fNameOut = resultsFile[:-4]+par[1]+'.pdf'
        createPlot(cmap, c, normal, fNameOut)

if __name__ == '__main__':
    plotResults()
