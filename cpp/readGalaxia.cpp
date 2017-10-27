#include "ebfvector.hpp"
#include "ebf.hpp"
#include <iostream>
#include <iomanip>
#include <stdexcept>
#include <cmath>

using namespace std;
int main(){
    string fileName("/Volumes/yoda/azuri/data/galaxia/sdss/galaxia_25_-5.ebf");
    ebf::EbfFile efile;
    ebf::EbfDataInfo dinfo;

    efile.Open(fileName,"/px");
    cout << "efile.elements = " << efile.elements() << endl;
    cout << "Units are " << efile.unit() << endl;

    vector<float> px(efile.elements());
    efile.Read(&px[0], efile.elements());

    cout << "px[0] = " << px[0] << endl;

    efile.Close();

    return 1;
}
