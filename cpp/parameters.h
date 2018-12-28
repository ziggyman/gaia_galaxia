#ifndef __PARAMETERS_H__
#define __PARAMETERS_H__

#include <boost/format.hpp>
#include <string>

using namespace std;

boost::format modelGetFileNameOutRoot();

boost::format obsGetFileNameOutRoot(string const& whichOne = "gaia");

boost::format gaiaGetFileNameOutRoot();

boost::format gaiaTgasGetFileNameOutRoot();

boost::format gaiaXSimbadGetFileNameOutRoot();

string modelGetDataDirOut();

string obsGetDataDirOut(string const& whichOne = "gaia");

string gaiaGetDataDirOut();

string gaiaDR2GetDataDirOut();

string gaiaXSimbadGetDataDirOut();

string gaiaTgasGetDataDirOut();

string obsGetFilter();

string modelGetFilters();

string obsGetFilterKeyWord(string const& filter, string const& whichOne = "gaia");

string modelGetFilterKeyWord(string const& filter);

string modelGetHeaderKeyWord(string const& keyWord);
string obsGetHeaderKeyWord(string const& keyWord);

unsigned getNStepsMagnitude();

unsigned getNSims();

string getPhotometricSystem();

#endif