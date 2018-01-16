import os
import sys

import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle

def readFile(fileName):
    """ extract Galactic Longitude and Latitude from the file names in file fileName"""
    print 'reading fileName <',fileName,'>'
    lonLat = []
    fn = open(fileName, 'r')
    lines = fn.readlines()
    fn.close()
    for line in lines:
        print 'line = ',type(line),': ',line
        subLine = line[line.find('_')+1:]
        print 'subLine = ',subLine
        lon = float(subLine[0:subLine.find('_')])
        subLine = subLine[subLine.find('_')+1:]
        print 'subLine = ',subLine
        lat = float(subLine[0:subLine.find('.')])
        print 'line = ',line,': lon = ',lon,', lat = ',lat
        lonLat.append([lon, lat])
    return lonLat

def main(argv):
    dir = '/Volumes/yoda/azuri/data/galaxia'
    fileNameWorking = 'workinOnFiles.txt'
    fileNameFinished = 'finishedFiles.txt'
    lonLatWorking = readFile(os.path.join(dir, fileNameWorking))
    lonLatFinished = readFile(os.path.join(dir, fileNameFinished))

    fig, ax = plt.subplots(1)
    recsWorking = []
    for i in range(len(lonLatWorking)):
        recsWorking.append(
            Rectangle(
                (lonLatWorking[i][0]-5, lonLatWorking[i][1]-5),   # (x,y)
                10,          # width
                10,          # height
            )
        )
    pcWorking = PatchCollection(recsWorking, facecolor='red')#, alpha=0.9,
                         #edgecolor='None')

    recsFinished = []
    for i in range(len(lonLatFinished)):
        recsFinished.append(
            Rectangle(
                (lonLatFinished[i][0]-5, lonLatFinished[i][1]-5),   # (x,y)
                10,          # width
                10,          # height
            )
        )
    pcFinished = PatchCollection(recsFinished, facecolor='green')#, alpha=0.9,
                         #edgecolor='None')

    ax.add_collection(pcWorking)
    ax.add_collection(pcFinished)

    plt.axis([-180, 180, -90, 90])
    plt.show()

if __name__ == '__main__':
    main(sys.argv)