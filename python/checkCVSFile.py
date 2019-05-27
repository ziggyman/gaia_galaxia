import csvData
import csvFree
import os

fileName = '/Volumes/obiwan/azuri/data/simbad/xy/GaiaXSimbadI_1.803122-1.820800_-0.318198--0.300520.csv'
fileName = '/Volumes/obiwan/azuri/data/gaia/x-match/simbadI/simbad_ImagXGaia.csv'
fileName = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2xSimbad/xy/temp/GaiaXSimbad_-0.000000-0.017678_0.053033-0.070711.csv'

#fileList = '/Volumes/obiwan/azuri/data/gaia/x-match/simbadI/xyFiles.list'
fileList = None
if fileList is not None:
    path = fileList[0:fileList.rfind('/')+1]+'xy'
    files = []
    with open(fileList,'r') as f:
        files = [os.path.join(path,line.strip('\n')) for line in f]
else:
    path = fileName[0:fileName.rfind('/')+1]
    files = [fileName]

nBadLines = 0
nBadFiles = 0
nBadHeaders = 0
badFiles = []
nCommasExpected = 0# csvFree.countCommas(files[0])
nCommasPreviousLine = 0;
print('nCommasExpected = ',nCommasExpected,', fileName = ',files[0])
for fileName in files:
    lines = []
    with open(os.path.join(path,fileName),'r') as fa:
        lines = [os.path.join(path,line.strip('\n')) for line in fa]
    for line in lines:
        nCommas = csvFree.countCommasInLine(line);
    if nCommasExpected == 0:
        nCommasExpected = nCommas;
    if nCommas != nCommasExpected:
        print('problem: fileName = ',fileName,': nCommas = ',nCommas,', nCommasExpected = ',nCommasExpected)
        nBadLines += 1
        if fileName not in badFiles:
            nBadFiles += 1
            badFiles.append(fileName)
    if nCommas != nCommasExpected:
        print('problem: fileName = ',fileName,': nCommas = ',nCommas,', nCommasExpected = ',nCommasExpected)
        if fileName not in badFiles:
            nBadFiles += 1
            badFiles.append(fileName)
    header = csvFree.readHeader(fileName,',')
    if len(header) != (nCommasExpected + 1):
        print('real problem: fileName = ',fileName,': nCommas = ',nCommas,', len(header) = ',len(header))
        nBadHeaders += 1
        if fileName not in badFiles:
            nBadFiles += 1
            badFiles.append(fileName)
    #nCommasExpected = nCommas

    csv = csvFree.readCSVFile(fileName, ',', True);
    print('csv.size() = ',csv.size())
print(nBadLines,' bad lines in ',nBadFiles,' bad files. nBadHeaders = ',nBadHeaders)
print('badFiles = ',badFiles)
