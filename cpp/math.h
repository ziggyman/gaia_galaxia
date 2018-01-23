#include <iostream>
#include <string>
#include <vector>
#include "csvData.h"

struct Histogram{
    vector< std::pair< double, double > > limits;/// limit=[limits[i].first, limits[i].second)
    vector< vector< unsigned > > indices;
    double start;
    double end;
    unsigned nSteps;

    void makeBinLimits(double startIn, double endIn, unsigned nStepsIn);

    /**
     * @brief Populate this->indices and eturn vector of vectors of indices of vecIn which fall into step i
     */
    void make(vector<double> const& vecIn);

    /**
     * @brief Fill a vector of vectors of indices randomly with elements of dataIn
     *        Requires that dataIn has more elements per bin than the original vector
     *        this was constructed from
     */
    vector< vector< unsigned > > fillRandomly(vector< double > const& dataIn);
    
};

