#include "matrix.h"

Matrix::Matrix(int nRows, int nCols){
    matrix = vector< vector< float > >(nRows);

    for (it=rows.begin(); it!=rows.end(); ++it){
        *it = vector<float>(nCols);
    }
}

Matrix::~Matrix(){

}
