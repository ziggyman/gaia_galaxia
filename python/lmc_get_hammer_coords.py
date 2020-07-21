from myUtils import hmsToDeg, dmsToDeg, raDecToLonLat
from hammer import Hammer

raLMC = hmsToDeg('5:23:34')
decLMC = dmsToDeg('-69:45:22')

lLMC, bLMC = raDecToLonLat(raLMC, decLMC)

ham = Hammer()
xy = ham.lonLatToXY(lLMC, bLMC)
print('x = ',xy.x,', y = ',xy.y)