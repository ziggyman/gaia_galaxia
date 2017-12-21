#ifndef __GALAXIA_H__
#define __GALAXIA_H__

#include <iostream>
#include <math.h>       /* sqrt */
#include <string>
#include <vector>

#include "galcomp.h"

using namespace std;

double getAEbfFactor(string const& band);

vector<double> vxyz2lbr(vector<double> const& px,
                        vector<double> const& py,
                        vector<double> const& pz,
                        vector<double> const& vx,
                        vector<double> const& vy,
                        vector<double> const& vz);

/**
 * @brief Append proper motion and radial velocity to data.
 * Keys mul (arcsec/yr), mub (arcsec/yr) and vr (km/s)
 * added to data
 * @param data : data to add mul, mub, and vr to
 */
void appendPM(CSVData & data);


#endif
