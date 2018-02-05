#ifndef __FILESANDLOCKS_H__
#define __FILESANDLOCKS_H__

#include <cstdio>
#include <fcntl.h>
#include <fstream>
#include <iostream>
#include <sys/file.h>
#include <string>
#include <unistd.h>
#include <vector>

using namespace std;

int lockFile(string const& fileName,
             string const& lockName,
             float sleepTime=0.1);

/**
 * @brief : if lock file exists, close all open files and remove their locks,
 *          and wait until lock file is deleted
 * @return
 */
int openAndLockFile(vector< std::shared_ptr< ofstream > > const& outFiles,
                    vector<string> const& outFileNames,
                    vector< shared_ptr< ofstream > > & filesOpened,
                    vector<string> & locks,
                    vector<int> & lockFds,
                    int iPix,
                    float sleepTime=5.0);

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
void closeFilesAndDeleteLocks(vector< shared_ptr< ofstream > > & filesOpened,
                              vector<string> & locks,
                              vector<int> & lockFds);

/**
 * @brief : remove lock called lockName
 *          This method has been added because of reports on the internet that
 *          calling this method instead of directly removing the lock prevents
 *          Threads to try and create the same lock file
 */
void deleteLock(int fd, string const& lockName);

unsigned countLines(string const& fileName);

#endif
