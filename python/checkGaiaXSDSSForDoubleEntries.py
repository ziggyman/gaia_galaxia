import csvData
import csvFree

fName = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2distXSDSS12/1552971988347A.csv'

csv = csvFree.readCSVFile(fName)

problematicStars = []
for iStar in range(csv.size()):
    posFound = csv.find('id', csv.getData('id', iStar))
    if len(posFound) > 1:
        print('PROBLEM: found star ',iStar,' with id ',csv.getData('id', iStar),' ',len(posFound),' times at positions ',posFound)
        if csv.getData('id', iStar) not in problematicStars:
            problematicStars.append(csv.getData('id', iStar))
            print(len(problematicStars),' found: ids = ',problematicStars)
            