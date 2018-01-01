#include "gaiaXSDSSMeanOfMultipleEntriesWriteToXY.h"

int main(void){
    string filename = "/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2distXSDSS12/1552971988347A.csv";
    string outFilename = "/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2distXSDSS12/GaiaXSDSS_mean.csv";

    Hammer ham;
    vector< Pixel > pixels = ham.getPixels();

    CSVData csv = readCSVFile(filename, ',', true);
    cout << "csv.size() = " << csv.size() << endl;

    string idKey = "id";
    vector<string> keysToCombine(0);
    keysToCombine.push_back("umag");
    keysToCombine.push_back("gmag");
    keysToCombine.push_back("rmag");
    keysToCombine.push_back("imag");
    keysToCombine.push_back("zmag");
    CSVData csvMean = csv.combineMultipleEntries(idKey, keysToCombine, outFilename);

    cout << "csvMean.size() = " << csvMean.size() << endl;
//    writeCSVFile(csvMean, outFilename);
}
