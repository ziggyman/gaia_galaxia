#ifndef __MOVESTARSTOXY__
#define __MOVESTARSTOXY__

#include <algorithm>
#include <boost/format.hpp>
#include <cstdio>
#include <ctime> // time_t
#include <fcntl.h>
#include <sys/file.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <vector>
#include "galcomp.h"
using namespace std;

int lockFile(string const& fileName,
             string & lockName,
             ios_base::openmode const& mode=ofstream::in);

/**
 * @brief : if lock file exists, close all open files and remove their locks,
 *          and wait until lock file is deleted
 * @return
 */
int openAndLockFile(vector< std::shared_ptr< ofstream > > const& outFiles,
                    vector<string> const& outFileNames,
                    vector< std::shared_ptr< ofstream > > & filesOpened,
                    vector<string> & locks,
                    vector<int> & lockFds,
                    int iPix);

/**
 * @brief : close file and remove lockName
 * @return
 */
void closeFileAndDeleteLock(ofstream & file,
                            string const& lockName,
                            int fd);

/**
 * @brief : close all files in filesOpened and remove the locks
 */
void closeFilesAndDeleteLocks(vector< std::shared_ptr< ofstream > > & filesOpened,
                              vector<string> & locks,
                              vector<int> & lockFds);

/**
 * @brief : remove lock called lockName
 *          This method has been added because of reports on the internet that
 *          calling this method instead of directly removing the lock prevents
 *          Threads to try and create the same lock file
 */
void deleteLock(int fd, string const& lockName);

boost::format galaxiaGetFileNameOutRoot();
boost::format gaiaGetFileNameOutRoot();

string galaxiaGetDataDirOut();
string gaiaGetDataDirOut();

vector<string> galaxiaGetInputFileNames();
vector<string> gaiaGetInputFileNames();
vector<string> gaiaGetInputFileNamesFromLonLat();

vector< std::shared_ptr< ofstream > > getOutFiles(vector<Pixel> const& pixels);

vector<string> getOutFileNames(vector<Pixel> const& pixels,
                               string const& whichOne);

void writeHeaderToOutFiles(vector<string> const& header,
                           vector<Pixel> const& pixels,
                           string const& whichOne,
                           bool const& append);
//                           vector<string> const& outFileNames,
//                           vector< std::shared_ptr< ofstream > > const& outFiles);

void appendCSVDataToXYFiles(CSVData const& csvData,
                            vector<Pixel> const& pixels,
                            string const& whichOne,
                            vector<string> const& ids,
                            bool const& doFind=false);
//                            vector< std::shared_ptr< ofstream > > const& outFiles,
//                            vector<string> const& outFileNames);

void gaiaMoveStarsToXY();

void gaiaMoveStarsFromLonLatToXY();

void galaxiaMoveStarsFromLonLatToXY();

void moveStarsToXY(string const& whichOne);

vector<string> galaxiaGetLonLatFileNames();

void galaxiaFixHeaderLineEnd();

/**
 * @brief Check Gaia Input Files for the same number of elements per line
 */
void checkGaiaInputFiles();

int main();

#endif
