#include "math.h"

void Histogram::makeBinLimits(double startIn, double endIn, unsigned nStepsIn){
    start = startIn;
    end = endIn;
    nSteps = nStepsIn;
    double step = (end - start) / double(nSteps);
    limits.resize(nSteps);

    double binStart = start;
    double binEnd = start + step;
    for (auto itBin=limits.begin(); itBin!=limits.end(); ++itBin, binStart+=step, binEnd+=step){
        itBin->first = binStart;
        itBin->second = binEnd;
    }
}

void Histogram::make(vector<double> const& vecIn){
    indices.resize(nSteps);
    double step = (end - start) / double(nSteps);
    for (auto itInd=indices.begin(); itInd!=indices.end(); ++itInd)
        itInd->resize(0);
    unsigned idx = 0;
    for (auto it=vecIn.begin(); it!=vecIn.end(); ++it, ++idx){
        int iStep = (*it) - start] / step;
        if ((iStep >= 0) && (iStep < nSteps)
            indices[unsigned(iStep)].push_back(idx);
    }
}

vector< vector< unsigned > > Histogram::fillRandomly(vector< double > const& dataIn){
    vector< vector< unsigned > > out(indices.size());

    /// create Histogram for dataIn
    Histogram allDataHist;
    allDataHist.start = start;
    allDataHist.end = end;
    allDataHist.nSteps = nSteps;
    allDataHist.limits = limits;
    allDataHist.make(dataIn);

    
}
