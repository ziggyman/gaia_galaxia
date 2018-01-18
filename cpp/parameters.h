#ifndef __PARAMETERS_H__
#define __PARAMETERS_H__

#include <boost/format.hpp>
#include <string>

using namespace std;

boost::format galaxiaGetFileNameOutRoot();

boost::format gaiaGetFileNameOutRoot();

boost::format gaiaTgasGetFileNameOutRoot();

string galaxiaGetDataDirOut();

string gaiaGetDataDirOut();

string gaiaTgasGetDataDirOut();

#endif