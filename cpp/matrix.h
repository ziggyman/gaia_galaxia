#ifndef __MATRIX_H__
#define __MATRIX_H__

//#include <algorithm>
//#include <cmath>
//#include <iostream>
//#include <random>
//#include <string>
#include <vector>

using namespace std;

class Matrix{
public:
    Matrix(int nRows, int nCols);
    ~Matrix();

    vector<float> dot(vector<float> const& vec);
    Matrix dot(Matrix const& mat);

private:
    vector< vector< float > > matrix;


};


#endif
