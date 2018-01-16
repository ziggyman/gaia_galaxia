#include "filesAndLocks.h"

int lockFile(string const& fileName,
             string const& lockName,
             float sleepTime){
    int fd = open( lockName.c_str(), O_RDWR | O_CREAT | O_EXCL, 0666 );
    if (fd == -1){
        time_t start, end;
        cout << "waiting for file <" << fileName << "> to become available" << endl;
        time (&start); // note time before execution

        /// keep trying until lock is deleted
        while (fd == -1){
            sleep(sleepTime);
            fd = open( lockName.c_str(), O_RDWR | O_CREAT | O_EXCL, 0666 );
        }
        time (&end); // note time before execution
        cout << "waited " << end-start << "s to get a lock on file <" << fileName << ">" << endl;
    }
    cout << "locked " << fileName << " for reading" << endl;

    return fd;
}

int openAndLockFile(vector< std::shared_ptr< ofstream > > const& outFiles,
                    vector<string> const& outFileNames,
                    vector< std::shared_ptr< ofstream > > & filesOpened,
                    vector<string> & locks,
                    vector<int> & lockFds,
                    int iPix,
                    float sleepTime){
    string lockName = "/var/lock/lock_" + to_string(iPix);
    /// if lock file exists, close all open files and remove their locks,
    /// and wait until lock file is deleted
    int fd = open( lockName.c_str(), O_RDWR | O_CREAT | O_EXCL, 0666 );
    if (fd == -1){
        time_t start, end;
        cout << "waiting for file <" << outFileNames[iPix] << "> to become available" << endl;
        time (&start); // note time before execution
        closeFilesAndDeleteLocks(filesOpened, locks, lockFds);

        /// keep trying until lock is deleted
        while (fd == -1){
            sleep(sleepTime);
            fd = open( lockName.c_str(), O_RDWR | O_CREAT | O_EXCL, 0666 );
        }
        time (&end); // note time before execution
        cout << "waited " << end-start << "s to get a lock on file <" << outFileNames[iPix] << ">" << endl;
    }
    locks.push_back(lockName);
    lockFds.push_back(fd);
    outFiles[iPix]->open(outFileNames[iPix], ofstream::app);
    filesOpened.push_back(outFiles[iPix]);
//    cout << "opened file <" << outFileNames[iPix] << ">" << endl;

    return fd;
}

void closeFileAndDeleteLock(ofstream & file,
                            string const& lockName,
                            int fd){
    file.close();
    deleteLock(fd, lockName);
}

void closeFilesAndDeleteLocks(vector< std::shared_ptr< ofstream > > & filesOpened,
                              vector<string> & locks,
                              vector<int> & lockFds){
    auto lockName = locks.begin();
    auto fd = lockFds.begin();
    for (auto open=filesOpened.begin(); open!=filesOpened.end(); ++open, ++lockName, ++fd){
        closeFileAndDeleteLock(*(*open), *lockName, *fd);
    }
    filesOpened.resize(0);
    locks.resize(0);
    lockFds.resize(0);
}

void deleteLock(int fd, string const& lockName){
    remove(lockName.c_str());
    close(fd);
}

unsigned countLines(string const& fileName){
    std::ifstream myfile(fileName);

    // new lines will be skipped unless we stop it from happening:
    myfile.unsetf(std::ios_base::skipws);

    // count the newlines with an algorithm specialized for counting:
    unsigned line_count = std::count(
        std::istream_iterator<char>(myfile),
        std::istream_iterator<char>(),
        '\n');

    return line_count-1;/// Minus 1 as all files are supposed to have a header line
}
