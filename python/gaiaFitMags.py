import csv
import csvData
import csvFree
import hammer
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model

from gaiaxsimbad import calcY,getGiantsAndDwarfs,getGoodStarIndices,getXY

fNameGaiaXSDSS_mean = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2distXSDSS12/GaiaXSDSS_mean.csv'

xForGBP = ['umag','gmag','rmag']
xForGRP = ['rmag','imag','zmag']

