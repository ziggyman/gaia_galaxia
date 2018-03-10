import numpy as np
import sys

def main(argv):
    progressFile = '/Volumes/yoda/azuri/data/galaxia/ubv_Vlt21.5_1.0.bak/ebfFilesWritten.txt'
    lineOut = '/Volumes/yoda/azuri/data/galaxia/ubv_Vlt21.5_1.0.bak/%d_%d/galaxia_%d_%d.ebf\n'
    with open(progressFile) as f:
        done = f.readlines()
    # remove whitespace characters like `\n` at the end of each line
    done = [x.strip() for x in done]
    lonLat = []
    for line in done:
        print 'line = <'+line+'>'
        lonStartPos = line.find('galaxia_')+8
        tempLine = line[lonStartPos:]
        print 'tempLine = <'+tempLine+'>'
        lonEndPos = tempLine.find('_')

        longitude = int(tempLine[0:lonEndPos])

        tempLine = tempLine[lonEndPos+1:]
        latitude = int(tempLine[0:tempLine.find('.')])
        print 'latitude = ',latitude

        found = False
        for i in range(len(lonLat)):
            if lonLat[i][0] == longitude:
                found = True
                if lonLat[i][1] < latitude:
                    lonLat[i][1] = latitude
                    print 'lonLat[',i,'] = ',lonLat[i]
        if not found:
            lonLat.append([longitude, latitude])
            print 'added [',longitude,', ',latitude,'] to lonLat'

    print 'lonLat = ',lonLat

    with open(progressFile, 'w') as f:
        for i in range(len(lonLat)):
            for lat in np.arange(-85, lonLat[i][1]+1, 10):
                line = lineOut % (lonLat[i][0], lat, lonLat[i][0], lat)
                print 'adding line = <'+line+'> to progressFile'
                f.write(line)

if __name__ == '__main__':
    main(sys.argv)
