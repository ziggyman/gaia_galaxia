import csv

import hammer
from myUtils import raDecToLonLat

dr2DistFileName = '/Volumes/discovery/azuri/data/gaia/dr2_distances/dist_%d.csv'
healPixFileName = '/Volumes/discovery/azuri/data/gaia/dr2_distances/HEALpixel_level5_radec_longlat_coordinates.csv'
myDistFileName = '/Volumes/discovery/azuri/data/gaia/dr2_distances/xy/GaiaSource_%.6f-%.6f_%.6f-%.6f_xyz_dist.csv'

hPix = 9999
gLon = 0.0
gLat = 0.0
ra = 0.0
dec = 0.0
hPixFound = False
with open(healPixFileName,'r') as healPixFile:
    healPix = csv.DictReader(healPixFile)

    for pix in healPix:
        if int(pix['healpix']) == hPix:
            gLon = float(pix[' glon'])
            gLat = float(pix[' glat'])
            ra = float(pix[' ra'])
            dec = float(pix[' dec'])
            hPixFound = True

if not hPixFound:
    print("ERROR: could not find hPix = ",hPix)
print('hPix = ',hPix,': gLon = ',gLon,', gLat = ',gLat,', ra = ',ra,', dec = ',dec)

ham = hammer.Hammer()
xy = ham.lonLatToXY(gLon, gLat)
pix = ham.getPixelContaining(xy)
print('coordinates contained in Hammer pixel ',pix)

i = 0
with open(dr2DistFileName % (hPix),'r') as dr2DistFile:
    dr2Dists = csv.DictReader(dr2DistFile)
    with open(myDistFileName % (pix.xLow,pix.xHigh,pix.yLow,pix.yHigh),'r') as myDistFile:
        for dr2Dist in dr2Dists:
            sourceId = dr2Dist['source_id']
            print('i = ',i,': searching for sourceId ',sourceId)
            myDists = csv.DictReader(myDistFile)
            for myDist in myDists:
                if myDist['source_id'] == sourceId:
                    dr2rMed = dr2Dist['rMedGeo']
                    myrMed = myDist['rEst[pc]']
                    print('sourceId ',sourceId,' found: dr2rMed = ',dr2rMed,', myrMed = ',myrMed)
                    STOP
            i += 1
