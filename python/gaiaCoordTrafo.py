#from galaxyMath import getICRSUnitVector
import numpy as np

import csvData
import csvFree
from galaxyMath import degToRad, radToDeg

transposeOfAG = np.zeros((3,3))
transposeOfAG[0,0] = -0.0548755604162154
transposeOfAG[1,0] = 0.4941094278755837
transposeOfAG[2,0] = -0.8676661490190047
transposeOfAG[0,1] = -0.8734370902348850
transposeOfAG[1,1] = -0.4448296299600112
transposeOfAG[2,1] = -0.1980763734312015
transposeOfAG[0,2] = -0.4838350155487132
transposeOfAG[1,2] = 0.7469822444972189
transposeOfAG[2,2] = 0.4559837761750669

#print('transposeOfAG = ',transposeOfAG)
#print(' ')

#
# @brief convert ICRS coordinates to Galactic coordinates
# @param rICRS - radius vector in ICRS coordinates [x_ICRS, y_ICRS, z_ICRS]
# @return radius vector in Galactic Coordinates [x_Gal, y_Gal, z_Gal]
#
# from http://gea.esac.esa.int/archive/documentation/GDR2/Data_processing/chap_cu3ast/sec_cu3ast_intro/ssec_cu3ast_intro_tansforms.html
def rICRSTorGal(rICRS):
    return transposeOfAG.dot(rICRS)

#
# @brief convert Galactic coordinates to ICRS coordinates
# @param rICRS - radius vector in Galactic coordinates [x_Gal, y_Gal, z_Gal]
# @return radius vector in ICRS Coordinates [x_ICRS, y_ICRS, z_ICRS]
#
# from http://gea.esac.esa.int/archive/documentation/GDR2/Data_processing/chap_cu3ast/sec_cu3ast_intro/ssec_cu3ast_intro_tansforms.html
def rGalTorICRS(rGal):
    return transposeOfAG.transpose().dot(rGal)

# @brief convert Right Ascension and Declination to unit vector in ICRS coordinates [x_ICRS, y_ICRS, z_ICRS]
# @param alpha - Right Ascension in degrees
# @param delta - Declination in degrees
# @return unit vector in ICRS Coordinates [x_ICRS, y_ICRS, z_ICRS]
#
# from http://gea.esac.esa.int/archive/documentation/GDR2/Data_processing/chap_cu3ast/sec_cu3ast_intro/ssec_cu3ast_intro_tansforms.html
def getICRSUnitVector(alpha, delta):
    alphaRad = degToRad(alpha)
    deltaRad = degToRad(delta)
    result = np.zeros((3));

#    print('alpha = ',alpha,': sin(alpha) = ',np.sin(alphaRad))
#    print('alpha = ',alpha,': cos(alpha) = ',np.cos(alphaRad))
#    print('delta = ',delta,': sin(delta) = ',np.sin(deltaRad))
#    print('delta = ',delta,': cos(delta) = ',np.cos(deltaRad))

    result[0] = np.cos(alphaRad) * np.cos(deltaRad);
    result[1] = np.sin(alphaRad) * np.cos(deltaRad);
    result[2] = np.sin(deltaRad);
    return result;

# @brief convert rICRS [xICRS, yICRS, zICRS] to Right Ascension and Declination
# @param rICRS: [xICRS, yICRS, zICRS]
# @return: [alpha, delta] in degrees
def rICRSToAlphaDelta(rICRS):
    delta = np.arcsin(rICRS[2])
    alpha = np.arccos(rICRS[0] / np.sin(delta))
    if np.isnan(alpha):
        alpha = np.arcsin(rICRS[1] / np.cos(delta))
    return [radToDeg(alpha), radToDeg(delta)]

# @brief convert Galactic Longitude and Latitude to unit vector in Galactic coordinates [x_Gal, y_Gal, z_Gal]
# @param l - Galactic Longitude in degrees
# @param b - Galactic Latitude in degrees
# @return unit vector in Galactic Coordinates [x_Gal, y_Gal, z_Gal]
#
# from http://gea.esac.esa.int/archive/documentation/GDR2/Data_processing/chap_cu3ast/sec_cu3ast_intro/ssec_cu3ast_intro_tansforms.html
def getGalUnitvector(l, b):
    return getICRSUnitVector(l,b)

# @brief convert rGal [xGal, yGal, zGal] to Galactic Longitude l and Latitude b
# @param rGal: [xGal, yGal, zGal]
# @return: [l, b] in degrees
#def rGalToLB(rGal):
#    return rICRSToAlphaDelta(rGal)

# @brief convert radius / unit vector in Galactic coordinates to Galactic Longitude l and Latitude b
# @param rGal - radius / unit vector in Galactic coordinates [x_Gal, y_Gal, z_Gal]
# @return [l,b] - list containing Galactic Longitude l and Galactic Latitude b in degrees
def rGalToLB(rGal):
    l = np.arctan2(rGal[1], rGal[0])
    b = np.arctan2(rGal[2], np.sqrt((rGal[0] * rGal[0]) + (rGal[1] * rGal[1])))
    return [radToDeg(l),radToDeg(b)]

# @brief convert Proper Motion in Right Ascension and Declination to ICRS coordinate system
# @param alpha - Right Ascension of the star in degrees
# @param delta - Declination of the star in degrees
# @param mu_alpha_star - mu_alpha * cos(delta) - mu_alpha: proper motion in Right Ascension NOTE: CHECK
# @param mu_delta - proper motion in Declination
# @return mu_ICRS [mu_x_ICRS, mu_y_ICRS, mu_z_ICRS]
def properMotionAlphaDeltaToICRS(alpha, delta, mu_alpha_star, mu_delta):
    alphaRad = degToRad(alpha)
    deltaRad = degToRad(delta)
    pICRS = np.zeros((3))
    pICRS[0] = 0. - np.sin(alphaRad)
    pICRS[1] = np.cos(alphaRad)
    pICRS[2] = 0.0

    qICRS = np.zeros((3))
    qICRS[0] = 0. - np.cos(alphaRad) * np.sin(deltaRad)
    qICRS[1] = 0. - np.sin(alphaRad) * np.sin(deltaRad)
    qICRS[2] = np.cos(deltaRad)

    muICRS = pICRS * mu_alpha_star + qICRS * mu_delta

    return muICRS

# @brief convert Proper Motion in Right Ascension and Declination to ICRS coordinate system
# @param l - Galactic Longitude in degrees
# @param b - Galactic Latitude in degrees
# @param mu_l_star - mu_l * cos(b) - mu_b: proper motion in Galactic Longitude NOTE: CHECK
# @param mu_b - proper motion in Galactic Latitude
# @return mu_Gal [mu_x_Gal, mu_y_Gal, mu_z_Gal]
def properMotionLonLatToGal(l, b, mu_l_star, mu_b):
    return properMotionAlphaDeltaToICRS(l, b, mu_l_star, mu_b)

# @brief return p_ICRS as a function of Right Ascension
# @param alpha: Right Ascension in degrees
# @return p_ICRS(alpha)
def get_p_ICRS(alpha):
    alphaInRadians = degToRad(alpha)
    p_ICRS = np.zeros(3)
    p_ICRS[0] = 0. - np.sin(alphaInRadians)
    p_ICRS[1] = np.cos(alphaInRadians)
#    print('p_ICRS = ',p_ICRS)
#    print(' ')
    return p_ICRS

# @brief return q_ICRS as a function of Right Ascension and Declination
# @param alpha: Right Ascension in degrees
# @param delta: Declination in degrees
# @return q_ICRS(alpha, delta)
def get_q_ICRS(alpha, delta):
    alphaInRadians = degToRad(alpha)
    deltaInRadians = degToRad(delta)
    q_ICRS = np.zeros(3)
    q_ICRS[0] = 0. - (np.cos(alphaInRadians) * np.sin(deltaInRadians))
    q_ICRS[1] = 0. - (np.sin(alphaInRadians) * np.sin(deltaInRadians))
    q_ICRS[2] = np.cos(delta)
#    print('q_ICRS = ',q_ICRS)
#    print(' ')
    return q_ICRS

# @brief return p_Gal as a function of Galactic Longitude l
# @param l: Galactic Longitude in Degrees
# @return p_Gal(l)
def get_p_Gal(l):
    lInRadians = degToRad(l)
    p_Gal = np.zeros(3)
    p_Gal[0] = 0. - np.sin(lInRadians)
    p_Gal[1] = np.cos(lInRadians)
#    print('p_Gal = ',p_Gal)
#    print(' ')
    return p_Gal

# @brief return q_Gal as a function of Galactic Longitude l and Galactic Latitude b
# @param l: Galactic Longitude in Degrees
# @param b: Galactic Latitude in Degrees
# @return q_Gal(l, b)
def get_q_Gal(l, b):
    lInRadians = degToRad(l)
    bInRadians = degToRad(b)
    q_Gal = np.zeros(3)
    q_Gal[0] = 0. - (np.cos(lInRadians) * np.sin(bInRadians))
    q_Gal[1] = 0. - (np.sin(lInRadians) * np.sin(bInRadians))
    q_Gal[2] = np.cos(bInRadians)
#    print('q_Gal = ',q_Gal)
#    print(' ')
    return q_Gal

# @brief return a vector of the propagated uncertainties
# @param alpha: Right Ascension in Degrees
# @param delta: Declination in Degrees
# @param l: Galactic Longitude in Degrees
# @param b: Galactic Latitude in Degrees
def errorPropagation(alpha, delta, l, b, deltaAlphaStar, deltaDelta, deltaOmega, deltaMuAlphaStar, deltaMuDelta):
    p_ICRS = get_p_ICRS(alpha)
    q_ICRS = get_q_ICRS(alpha, delta)
    p_Gal = get_p_Gal(l)
    q_Gal = get_q_Gal(l, b)
    pq = np.array([p_Gal, q_Gal])
#    print('pq = ',pq)
#    print(' ')
    pqDotAGTrans = pq.dot(transposeOfAG)
#    print('pqDotAGTrans = ',pqDotAGTrans)
#    print(' ')
    G = pqDotAGTrans.dot(np.array([p_ICRS, q_ICRS]).transpose())
#    print('G = ',G)
#    print(' ')

    J = np.zeros((5,5))
    J[0,0] = G[0,0]
    J[0,1] = G[0,1]
    J[1,0] = G[0,1]
    J[1,1] = G[1,1]
    J[2,2] = 1.
    J[3,3] = G[0,0]
    J[3,4] = G[0,1]
    J[4,3] = G[0,1]
    J[4,4] = G[1,1]
#    print('J = ',J)
#    print(' ')

    e = np.zeros(5)
    e[0] = deltaAlphaStar
    e[1] = deltaDelta
    e[2] = deltaOmega
    e[3] = deltaMuAlphaStar
    e[4] = deltaMuDelta
#    print('e = ',e)

    g = J.dot(e)
#    print('g = ',g)


if __name__ == '__main__':
    alpha = 0.
    delta = 0.

    xyzICRS = getICRSUnitVector(alpha, delta)
#    print('xyzICRS = ',xyzICRS)

    rGal = rICRSTorGal(xyzICRS)
#    print('rGal = ',rGal)

    rTest = rGalTorICRS(rGal)
#    print('rTest = ',rTest)

    l,b = rGalTolb(rGal)
#    print('l = ',l,', b = ',b)

    fName = '/Volumes/work/azuri/data/gaia/GaiaSource_1008431284282695936_1008626993058019840.csv'

    csv = csvFree.readCSVFile(fName)

    #print('csv.getData(ra) = ',csv.getData('ra'))

    ra = np.array(csvFree.convertStringVectorToDoubleVector(csv.getData('ra')))
    dec = np.array(csvFree.convertStringVectorToDoubleVector(csv.getData('dec')))

    xyzOneStar = getICRSUnitVector(ra[0], dec[0])
#    print('xyzOneStar = ',xyzOneStar)

    xyzAllStars = getICRSUnitVector(ra, dec)
#    print('xyzAllStars = ',xyzAllStars)
