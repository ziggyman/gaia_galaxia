#include "../galcomp.h"
#include "../moveStarsToXY.h"
#include "gtest/gtest.h"

using namespace std;

namespace {

// The fixture for testing class Galcomp.
class GalCompTest : public ::testing::Test {
 protected:
  // You can remove any or all of the following functions if its body
  // is empty.

  GalCompTest() {
    // You can do set-up work for each test here.
  }

  virtual ~GalCompTest() {
    // You can do clean-up work that doesn't throw exceptions here.
  }

  // If the constructor and destructor are not enough for setting up
  // and cleaning up each test, you can define the following methods:

  virtual void SetUp() {
    // Code here will be called immediately after the constructor (right
    // before each test).
  }

  virtual void TearDown() {
    // Code here will be called immediately after each test (right
    // before the destructor).
  }

  // Objects declared here can be used by all tests in the test case for Galcomp.
};

// Tests that the Galcomp::Bar() method does Abc.
/*TEST_F(GalCompTest, testReadCSVFile) {
    cout << "running testReadCSVFile" << endl;
    string fileName("/Volumes/discovery/azuri/data/gaia/dr2/xy/GaiaSource_-0.000000-0.017678_-0.601041--0.583363_xyz.csv");
    CSVData csvData = readCSVFile(fileName);
    cout << "csvData.header.size() = " << csvData.header.size() << ", csvData.data.size() = "
            << csvData.data.size() << ", csvData.data[0].size() = " << csvData.data[0].size() << endl;
    ASSERT_GT(csvData.header.size(), 1);
    ASSERT_GT(csvData.data.size(), 1);
    ASSERT_EQ(csvData.data[0].size(), csvData.header.size());
}

TEST_F(GalCompTest, testGetData){
    cout << "running testGetData" << endl;
    string fileName("/Volumes/discovery/azuri/data/gaia/dr2/xy/GaiaSource_-0.000000-0.017678_-0.601041--0.583363_xyz.csv");
    CSVData csvData = readCSVFile(fileName);
    string l = csvData.getData(string("l"), 0);
    ASSERT_NE(l, string(""));
    vector<string> ls = csvData.getData(string("l"));
    ASSERT_EQ(ls.size(), csvData.data.size());
}

TEST_F(GalCompTest, testConvertStringVectorToDoubleVector){
    cout << "running testConvertStringVectorToDoubleVector" << endl;
    vector<string> strVec(3);
    strVec[0] = string("0");
    strVec[1] = string("1.2");
    strVec[2] = string("");
    vector<double> dblVec = convertStringVectorToDoubleVector(strVec);
    ASSERT_EQ(dblVec[0], 0.0);
    ASSERT_EQ(dblVec[1], 1.2);
    cout << "dblVec[2] = " << dblVec[2] << endl;
}

TEST_F(GalCompTest, testCalcIcFromBVg){
    Hammer hammer;
    vector<Pixel> pixels = hammer.getPixels();
    Pixel xyWindow;// = pixels[pixels.size()/2];
    xyWindow.xLow = 0.01;
    xyWindow.xHigh = 0.05;
    xyWindow.yLow = -0.6;
    xyWindow.yHigh = -0.5;

    CSVData csvData = getStarsInXYWindow(pixels, xyWindow, "galaxia");
    cout << "testCalcIcFromBVg: csvData.size() = " << csvData.size() << endl;

    vector<double> ubv_b = convertStringVectorToDoubleVector(csvData.getData(modelGetFilterKeyWord("B")));
    vector<double> ubv_v = convertStringVectorToDoubleVector(csvData.getData(modelGetFilterKeyWord("V")));
    vector<double> ubv_i = convertStringVectorToDoubleVector(csvData.getData(modelGetFilterKeyWord("I")));
    vector<double> log_g = convertStringVectorToDoubleVector(csvData.getData(modelGetFilterKeyWord("log_g")));

    vector<double> ubv_i_calc = calcIcFromBVg(ubv_b, ubv_v, log_g);
    vector<double> diff = difference(ubv_i, ubv_i_calc);
    cout << "testCalcIcFromBVg: mean(ubv_i - ubv_i_calc) = " << mean(diff) << ", sDev(ubv_i - ubv_i_calc) = " << standardDeviation(diff) << endl;
}*/

TEST_F(GalCompTest, testComparePixel){
    Hammer hammer;
    vector<Pixel> pixels = hammer.getPixels();
    Pixel xyWindow;// = pixels[pixels.size()/2];
    xyWindow.xLow = 0.01;
    xyWindow.xHigh = 0.05;
    xyWindow.yLow = -0.6;
    xyWindow.yHigh = -0.5;
    Pixel lonLatWindowA;// = pixels[pixels.size()/2];
    lonLatWindowA.xLow = hammer.xYToLonLat(xyWindow.xLow, xyWindow.yLow).lon;
    lonLatWindowA.xHigh = hammer.xYToLonLat(xyWindow.xHigh, xyWindow.yHigh).lon;
    lonLatWindowA.yLow = hammer.xYToLonLat(xyWindow.xLow, xyWindow.yLow).lat;
    lonLatWindowA.yHigh = hammer.xYToLonLat(xyWindow.xHigh, xyWindow.yHigh).lat;
    Pixel lonLatWindowB;// = pixels[pixels.size()/2];
    lonLatWindowB.xLow = hammer.xYToLonLat(xyWindow.xLow, xyWindow.yHigh).lon;
    lonLatWindowB.xHigh = hammer.xYToLonLat(xyWindow.xHigh, xyWindow.yLow).lon;
    lonLatWindowB.yLow = hammer.xYToLonLat(xyWindow.xHigh, xyWindow.yLow).lat;
    lonLatWindowB.yHigh = hammer.xYToLonLat(xyWindow.xLow, xyWindow.yHigh).lat;
    string keyWord("distance");
    cout << "testComparePixel: xyWindow: xLow = " << xyWindow.xLow << ", xHigh = " << xyWindow.xHigh << ", yLow = " << xyWindow.yLow << ", yHigh = " << xyWindow.yHigh << endl;
    cout << "testComparePixel: lonLatWindowA: lonLow = " << lonLatWindowA.xLow << ", lonHigh = " << lonLatWindowA.xHigh << ", latLow = " << lonLatWindowA.yLow << ", latHigh = " << lonLatWindowA.yHigh << endl;
    cout << "testComparePixel: lonLatWindowB: lonLow = " << lonLatWindowB.xLow << ", lonHigh = " << lonLatWindowB.xHigh << ", latLow = " << lonLatWindowB.yLow << ", latHigh = " << lonLatWindowB.yHigh << endl;
    comparePixel(pixels,
                 xyWindow,
                 keyWord,
                 "gaia");
}

TEST_F(GalCompTest, testHistogram){
    Hammer hammer;
    vector<Pixel> pixels = hammer.getPixels();

    Pixel xyWindow;// = pixels[pixels.size()/2];
    xyWindow.xLow = 0.01;
    xyWindow.xHigh = 0.05;
    xyWindow.yLow = -0.6;
    xyWindow.yHigh = -0.5;

    string whichOne("galaxia");

    string keyWord = "G";

    int nBars = 20;
    float xMin = 5.0;
    float xMax = 21.0;

    vector< pair< float, float > > limits = getHistogramLimits(nBars,
                                                               xMin,
                                                               xMax);

    vector<int> hist = getHistogram(pixels,
                                    xyWindow,
                                    whichOne,
                                    keyWord,
                                    limits);
    for (int i=0; i<hist.size(); i++){
      cout << "hist[" << i << "]  = " << hist[i] << endl;

    }
}

//TEST_F(GalCompTest, testGaiaMoveStarsToXY){
//    cout << "running gaiaMoveStars" << endl;
//    gaiaMoveStarsToXY();
//}

}  // namespace

int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
