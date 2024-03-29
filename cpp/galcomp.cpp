#include "galcomp.h"

vector<Pixel> getPixels(){
    calcOuterLimits();
    vector<Pixel> pixels(0);
    pixels.reserve(320*160);
    Pixel pix;
    double xStep = (_OuterLimitsXY[1].x-_OuterLimitsXY[0].x)/_NPixX;
    double yStep = (_OuterLimitsXY[1].y-_OuterLimitsXY[0].y)/_NPixY;
    for (int xPosLeft=_OuterLimitsXY[0].x; xPosLeft<_OuterLimitsXY[1].x; xPosLeft+=xStep){
        for (int yPosBottom=_OuterLimitsXY[0].y; yPosBottom<_OuterLimitsXY[1].y; yPosBottom+=yStep){
            pix.xLow = xPosLeft;
            pix.xHigh = xPosLeft + xStep;
            pix.yLow = yPosBottom;
            pix.yHigh = yPosBottom + yStep;
            if (isInside(pix.xLow, pix.yLow) || isInside(pix.xLow, pix.yHigh) ||
                isInside(pix.yHigh, pix.yLow) || isInside(pix.xHigh, pix.yHigh))
                pixels.push_back(pix);
        }
    }
    return pixels;
}

CSVData readCSVFile(string const& fileName){
    ifstream inStream(fileName);

    CSVData csvData;
    int pos;
    string substring;
    struct timeval start, end;

    if (inStream.is_open()){
        int iLine = 0;
        string line;
        while (getline(inStream, line)){
            if (iLine == 0){
                stringstream lineStream(line.c_str());
                pos = 0;
                if(lineStream.good()){
                    getline(lineStream, substring, ',');
                    cout << "pos = " << pos << ": substring = " << substring << endl;
                    csvData.header.push_back(substring);
                    cout << "pos = " << pos << ": added " << csvData.header[csvData.header.size()-1] << " to header" << endl;
                    pos++;
                }
                iLine = 1;
                continue;
            }
            stringstream lineStream(line.c_str());
            pos = 0;
            vector<string> dataLine(0);
            while(lineStream.good()){
                getline(lineStream, substring, ',');
                cout << "pos = " << pos << ": substring = " << substring << endl;

                dataLine.push_back(substring);
                pos++;
            }
            csvData.data.push_back(dataLine);
        }
        inStream.close();
        gettimeofday(&end, NULL);
        cout << "fileName <" << fileName << "> read in " << ((end.tv_sec * 1000000 + end.tv_usec)
                        - (start.tv_sec * 1000000 + start.tv_usec))/1000000 << " s" << endl;
        cout << "csvData.data.size() = " << csvData.data.size() << endl;
    }
    else{
        cout << "ERROR: file " << fileName << " not open" << endl;
    }
    return csvData;
}
