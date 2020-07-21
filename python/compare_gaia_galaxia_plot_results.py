import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colorbar as cbar
import subprocess

import csvData
import csvFree
from hammer import Pixel,XY,LonLat,Hammer
from pnAlignment import plotLBMarks

resultsFile = '/Users/azuri/daten/illume_research/martin/results.csv'
results = csvFree.readCSVFile(resultsFile)

ham = Hammer()
pixels = ham.getPixels()
print('total number of pixels = ',len(pixels))

def plotHammerGrid():
    plotLBMarks(10)

def plotResults(fNameOut):
    fig = plt.figure(figsize=(25,10))
    ax = fig.add_subplot(111)
    plt.axis('off')

    nStarsGaia = np.array(csvFree.convertStringVectorToDoubleVector(results.getData('nStarsGaia')))
    nStarsGalaxia = np.array(csvFree.convertStringVectorToDoubleVector(results.getData('nStarsGalaxia')))
    difference = nStarsGalaxia - nStarsGaia
    maxDiff = np.amax(np.absolute(difference))
    percentDiff = 100. * difference / nStarsGalaxia
    percentDiff = np.nan_to_num(percentDiff)
    print('percentDiff = ',percentDiff)

    maxPercentDiff = 100.#np.amax(np.absolute(percentDiff))
    print('maxPercentDiff = ',maxPercentDiff)
#    normal = plt.Normalize(-maxDiff, maxDiff)
    normal = plt.Normalize(-maxPercentDiff, maxPercentDiff)
    print('normal = ',normal)
    cmap=plt.cm.jet
    print('cmap = ',cmap)
    print('dir(cmap) = ',dir(cmap))
#    c = [cmap((diff / maxDiff) / 2. + 0.5) for diff in difference]#cmap(difference)
    c = [cmap((diff / maxPercentDiff) / 2. + 0.5) for diff in percentDiff]#cmap(difference)
    print('c = ', c[0:100])
#    STOP

    for iPix in range(results.size()):
#        print('differnce[',iPix,'] = ',difference[iPix],', color = ',c[iPix])
        print('percentDiff[',iPix,'] = ',percentDiff[iPix],', color = ',c[iPix])
        rect1 = matplotlib.patches.Rectangle((float(results.getData('pixelxMin',iPix)), float(results.getData('pixelYMin',iPix))),
                                             float(results.getData('pixelXMax',iPix)) - float(results.getData('pixelxMin',iPix)),
                                             float(results.getData('pixelYMax',iPix)) - float(results.getData('pixelYMin',iPix)),
                                             facecolor = c[iPix],
                                             )

        ax.add_patch(rect1)

    cax, _ = cbar.make_axes(ax)
    cb2 = cbar.ColorbarBase(cax, cmap=cmap,norm=normal)
    ax.set_xlim(-2.82843, 2.82843)
    ax.set_ylim(-1.41421, 1.41421)
#    cbarTicks = np.arange(0.,1.0001,20./180.)
#    plt.clim(vmin=-maxDiff,
#             vmax=maxDiff)
#    cbar = plt.colorbar(ticks=cbarTicks)
#    cbar.set_label('Galactic Position Angle')
#    cbarTicks = cbarTicks*180.
#    cbarTicks = np.round(cbarTicks)
#    cbarTicks = [int(x) for x in cbarTicks]
#    cbar.ax.set_yticklabels(cbarTicks)
#    cbar.ax.tick_params(labelsize=26)
#    ax = cbar.ax
#    text = ax.yaxis.label
#    font = matplotlib.font_manager.FontProperties(size=26)#family='times new roman', style='italic',
#    text.set_font_properties(font)
#    plt.tick_params(axis='x',          # changes apply to the x-axis
#                    which='both',      # both major and minor ticks are affected
#                    bottom=False,      # ticks along the bottom edge are off
#                    top=False,         # ticks along the top edge are off
#                    labelbottom=False) # labels along the bottom edge are off
#    plt.tick_params(axis='y',          # changes apply to the y-axis
#                    which='both',      # both major and minor ticks are affected
#                    left=False,      # ticks along the bottom edge are off
#                    right=False,         # ticks along the top edge are off
#                    labelleft=False) # labels along the bottom edge are off
#    fig.tight_layout()
    if fNameOut is not None:
        print('plotHammerProjection: fNameOut = <'+fNameOut+'>')
        fNameOutTemp = fNameOut[:-3]+'.tmp.pdf'
        fig.savefig(fNameOutTemp, bbox_inches='tight')
        subprocess.run(["gs","-sDEVICE=pdfwrite","-dCompatibilityLevel=1.4","-dPDFSETTINGS=/ebook","-dNOPAUSE", "-dQUIET", "-dBATCH", "-sOutputFile="+fNameOut, fNameOutTemp])
        subprocess.run(["rm",fNameOutTemp])
    plt.show()
    plt.close(fig)
    print('after all_pne: ',plt.get_fignums(),' figures open')

if __name__ == '__main__':
    plotResults(resultsFile[:-3]+'pdf')