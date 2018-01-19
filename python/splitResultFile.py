#! /usr/bin/env python
import sys

def main(argv):
    outputFileGaia = '/Volumes/yoda/azuri/data/gaia/nStarsPerPixel.dat'
    fGaia = open(outputFileGaia,'w')
    outputFileGaiaTgas = '/Volumes/yoda/azuri/data/gaia-tgas/nStarsPerPixel.dat'
    fGaiaTgas = open(outputFileGaiaTgas,'w')
    outputFileGalaxia = '/Volumes/yoda/azuri/data/galaxia/nStarsPerPixel.dat'
    fGalaxia = open(outputFileGalaxia,'w')
    print 'starting for loop'
    for inputFile in ['/Volumes/yoda/azuri/data/gaia-galaxia/nStarsPerPixel.dat',
                        '/Volumes/yoda/azuri/data/gaiaTgas-galaxia/nStarsPerPixel.dat']:
        print 'inputFile = ',inputFile
        with open(inputFile, 'r') as f:
            iLine = 0
            for line in f:
                print 'line = ',line
                if iLine == 0:
                    headerId, headerGalaxia, headerGaia = line.split()
                    headerId = headerId[1:]
                    if inputFile == '/Volumes/yoda/azuri/data/gaia-galaxia/nStarsPerPixel.dat':
                        fGaia.write(headerId+','+headerGaia+'\n')
                    else:
                        fGaiaTgas.write(headerId+','+headerGaia+'\n')
                        fGalaxia.write(headerId+','+headerGalaxia+'\n')
                    iLine += 1
                else:
                    pixId, setGalaxia, setGaia = line.split()
                    if inputFile == '/Volumes/yoda/azuri/data/gaia-galaxia/nStarsPerPixel.dat':
                        fGaia.write(pixId+','+setGaia+'\n')
                    else:
                        fGaiaTgas.write(pixId+','+setGaia+'\n')
                        fGalaxia.write(pixId+','+setGalaxia+'\n')

if __name__ == '__main__':
    main(sys.argv)
