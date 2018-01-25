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
TEST_F(GalCompTest, testReadCSVFile) {
    cout << "running testReadCSVFile" << endl;
    string fileName("/Volumes/yoda/azuri/data/gaia-tgas/xy/TgasSource_-0.000000-0.017678_-0.601041--0.583363.csv");
    CSVData csvData = readCSVFile(fileName);
    cout << "csvData.header.size() = " << csvData.header.size() << ", csvData.data.size() = "
            << csvData.data.size() << ", csvData.data[0].size() = " << csvData.data[0].size() << endl;
    ASSERT_GT(csvData.header.size(), 1);
    ASSERT_GT(csvData.data.size(), 1);
    ASSERT_EQ(csvData.data[0].size(), csvData.header.size());
}

TEST_F(GalCompTest, testGetData){
    cout << "running testGetData" << endl;
    string fileName("/Volumes/yoda/azuri/data/gaia-tgas/xy/TgasSource_-0.000000-0.017678_-0.601041--0.583363.csv");
    CSVData csvData = readCSVFile(fileName);
    string l = csvData.getData(string("l"), 0);
    ASSERT_NE(l, string(""));
    vector<string> ls = csvData.getData(string("l"));
    ASSERT_EQ(ls.size(), csvData.data.size());
}

TEST_F(GalCompTest, testConvertStringVectortoDoubleVector){
    cout << "running testConvertStringVectortoDoubleVector" << endl;
    vector<string> strVec(3);
    strVec[0] = string("0");
    strVec[1] = string("1.2");
    strVec[2] = string("");
    vector<double> dblVec = convertStringVectorToDoubleVector(strVec);
    ASSERT_EQ(dblVec[0], 0.0);
    ASSERT_EQ(dblVec[1], 1.2);
    cout << "dblVec[2] = " << dblVec[2] << endl;
}

TEST_F(GalCompTest, testComparePixel){
    Hammer hammer;
    vector<Pixel> pixels = hammer.getPixels();
    Pixel xyWindow = pixels[1000];
    string keyWord("distance");
    cout << "testComparePixel: xyWindow: xLow = " << xyWindow.xLow << ", xHigh = " << xyWindow.xHigh << ", yLow = " << xyWindow.yLow << ", yHigh = " << xyWindow.yHigh << endl;
    comparePixel(pixels,
                 xyWindow,
                 keyWord,
                 "gaiaTgas");
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
