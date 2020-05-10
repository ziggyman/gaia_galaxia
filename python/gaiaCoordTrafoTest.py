import numpy as np

import gaiaCoordTrafo

def compareTo(valA, valB):
    limit = 1.0e-16
    absDiff = np.absolute(valA - valB)
#    print('valA = ',valA,', valB = ',valB,': absDiff = ',absDiff)
    if (absDiff < limit):
#        print('absDiff = ',absDiff,' < limit = ',limit)
        return True
#    else:
#        print('absDiff = ',absDiff,' >= limit = ',limit)
    return False

def test_getICRSUnitVector():
    """Test that [0,0] points towards x axis"""
    alpha = 0.
    delta = 0.
    rICRS = gaiaCoordTrafo.getICRSUnitVector(alpha, delta)
    print('alpha = ',alpha,', delta = ',delta,': rICRS = ',rICRS)
    if not compareTo(rICRS[0],1.):
        print('problem calculating xICRS')
        return False
    if not compareTo(rICRS[1], 0.):
        print('problem calculating yICRS')
        return False
    if not compareTo(rICRS[2], 0.):
        print('problem calculating zICRS')
        return False

    """Test that [90,0] points towards y axis"""
    alpha = 90.
    delta = 0.
    rICRS = gaiaCoordTrafo.getICRSUnitVector(alpha, delta)
    print('alpha = ',alpha,', delta = ',delta,': rICRS = ',rICRS)
    if not compareTo(rICRS[0],0.):
        print('problem calculating xICRS')
        return False
    if not compareTo(rICRS[1],1.):
        print('problem calculating yICRS')
        return False
    if not compareTo(rICRS[2],0.):
        print('problem calculating zICRS')
        return False

    """Test that [0,90] points towards z axis"""
    alpha = 0.
    delta = 90.
    rICRS = gaiaCoordTrafo.getICRSUnitVector(alpha, delta)
    print('alpha = ',alpha,', delta = ',delta,': rICRS = ',rICRS)
    if not compareTo(rICRS[0],0.):
        print('problem calculating xICRS')
        return False
    if not compareTo(rICRS[1],0.):
        print('problem calculating yICRS')
        return False
    if not compareTo(rICRS[2],1.):
        print('problem calculating zICRS')
        return False

    return True

def test_lbTorICRS_and_back():
    alpha = 0.
    delta = 0.
    rICRS = gaiaCoordTrafo.getICRSUnitVector(alpha, delta)
    print('rICRS = ',rICRS)

    alphaTest, deltaTest = gaiaCoordTrafo.rICRSToAlphaDelta(rICRS)
    print('alpha = ',alpha,': alphaTest = ',alphaTest)
    print('delta = ',delta,': deltaTest = ',deltaTest)
    if not compareTo(alpha,alphaTest):
        print('problem calculating alpha')
        return False
    if not compareTo(delta,deltaTest):
        print('problem calculating delta')
        return False

    return True

def test_rICRSTorGalAndBack():
    rICRS = np.array([1,0,0])
    print('rICRS = ',rICRS)

    rGal = gaiaCoordTrafo.rICRSTorGal(rICRS)
    print('rGal = ',rGal)

    rTest = gaiaCoordTrafo.rGalTorICRS(rGal)
    print('rTest = ',rTest)
    for i in range(rICRS.shape[0]):
        if not compareTo(rICRS[i],rTest[i]):
            print('we have a problem')
            return False
    return True

def test_getGalUnitvector():
    l = 0
    b = 0
    rGal = gaiaCoordTrafo.getGalUnitvector(l, b)
    print('rGal = ',rGal)
    if not compareTo(rGal[0],1.):
        print('Houston we have a problem')
        return False
    if not compareTo(rGal[1],0.):
        print('Houston we have a problem')
        return False
    if not compareTo(rGal[2],0.):
        print('Houston we have a problem')
        return False

    l = 0
    b = 90
    rGal = gaiaCoordTrafo.getGalUnitvector(l, b)
    print('rGal = ',rGal)
    if not compareTo(rGal[0],0.):
        print('Houston we have a problem')
        return False
    if not compareTo(rGal[1],0.):
        print('Houston we have a problem')
        return False
    if not compareTo(rGal[2],1.):
        print('Houston we have a problem')
        return False

    l = 90
    b = 0
    rGal = gaiaCoordTrafo.getGalUnitvector(l, b)
    print('rGal = ',rGal)
    if not compareTo(rGal[0],0.):
        print('Houston we have a problem')
        return False
    if not compareTo(rGal[1],1.):
        print('Houston we have a problem')
        return False
    if not compareTo(rGal[2],0.):
        print('Houston we have a problem')
        return False
    return True

def test_rGalToLB():
    rGal = np.zeros(3)
    rGal[0] = 1.
    l, b = gaiaCoordTrafo.rGalToLB(rGal)
    print('l = ',l,', b = ',b)
    if not compareTo(l,0.):
        print('Houston we have a problem')
        return False
    if not compareTo(b,0.):
        print('Houston we have a problem')
        return False

    rGal[0] = 0.
    rGal[1] = 1.
    l, b = gaiaCoordTrafo.rGalToLB(rGal)
    print('l = ',l,', b = ',b)
    if not compareTo(l,90.):
        print('Houston we have a problem')
        return False
    if not compareTo(b,0.):
        print('Houston we have a problem')
        return False

    rGal[0] = 0.
    rGal[1] = 0.
    rGal[2] = 1.
    l, b = gaiaCoordTrafo.rGalToLB(rGal)
    print('l = ',l,', b = ',b)
    if not compareTo(l,0.):
        print('Houston we have a problem')
        return False
    if not compareTo(b,90.):
        print('Houston we have a problem')
        return False

    return True

def test_properMotionAlphaDeltaToICRS():
    print(' ')
    #(alpha, delta, mu_alpha_star, mu_delta):

def test_properMotionLonLatToGal():
    print(' ')
    #(l, b, mu_l_star, mu_b):

def test_get_p_ICRS():
    print(' ')
    #(alpha)

def test_get_q_ICRS():
    print(' ')
    #(alpha, delta)

def test_get_p_Gal():
    print(' ')
    #(l)

def test_get_q_Gal():
    print(' ')
    #(l, b):



if __name__ == '__main__':
    gaiaCoordTrafo.errorPropagation(90., 0., 90., 0., 0, 0, 0, 0, 0)
    print(' ')
    print('====================================')
    print(' ')

    gaiaCoordTrafo.errorPropagation(90., 0., 90., 0., 1, 1, 1, 1, 1)

    if test_getICRSUnitVector():
        print('test_getICRSUnitVector passed')
    else:
        print('test_getICRSUnitVector failed')

    if test_lbTorICRS_and_back():
        print('test_lbTorICRS_and_back passed')
    else:
        print('test_lbTorICRS_and_back failed')

    if test_rICRSTorGalAndBack():
        print('test_rICRSTorGalAndBack passed')
    else:
        print('test_rICRSTorGalAndBack failed')

    if test_getGalUnitvector():
        print('test_getGalUnitvector passed')
    else:
        print('test_getGalUnitvector failed')

    if test_rGalToLB():
        print('test_rGalToLB passed')
    else:
        print('test_rGalToLB failed')
#test_rICRSTorGal()
