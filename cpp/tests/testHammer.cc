#include "../hammer.h"
#include "gtest/gtest.h"

namespace {

// The fixture for testing class Hammer.
class HammerTest : public ::testing::Test {
 protected:
  // You can remove any or all of the following functions if its body
  // is empty.

  HammerTest() {
    // You can do set-up work for each test here.
  }

  virtual ~HammerTest() {
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

  // Objects declared here can be used by all tests in the test case for Hammer.
};

// Tests that the Hammer::Bar() method does Abc.
TEST_F(HammerTest, testCalcOuterLimits) {
  calcOuterLimits();
  double xMinExpected = -2.82843;
  double xMaxExpected = 2.82843;
  double yMinExpected = -1.41421;
  double yMaxExpected = 1.41421;
  EXPECT_LT(fabs(xMinExpected - _OuterLimitsXY[0].x), 0.00001);
  EXPECT_LT(fabs(xMaxExpected - _OuterLimitsXY[1].x), 0.00001);
  EXPECT_LT(fabs(yMinExpected - _OuterLimitsXY[0].y), 0.00001);
  EXPECT_LT(fabs(yMaxExpected - _OuterLimitsXY[1].y), 0.00001);
}

TEST_F(HammerTest, testXYAndLonLat){
    vector<double> lonLowLimit(2);
    lonLowLimit[0] = -179.999;
    lonLowLimit[1] = 0.00001;
    vector<double> lonHighLimit(2);
    lonHighLimit[0] = 180.0;
    lonHighLimit[1] = 360.0;

    for (int iRun = 0; iRun < 2; ++iRun){
        for (double lon=lonLowLimit[iRun]; lon<lonHighLimit[iRun]; lon+=0.1){
            for (double lat=-89.9; lat<89.99; lat+=0.1){
                XY xy = lonLatToXY(lon, lat);
                LonLat lonLat = xYToLonLat(xy.x, xy.y);
    /*            cout << "lon = " << lon
                     << ", lat = " << lat
                     << ": x = " << xy.x
                     << ", y = " << xy.y
                     << ", lonLat.lon = " << lonLat.lon
                     << ", lonLat.lat = " << lonLat.lat << endl;*/
                if ((iRun == 0) || (lon <= 180.0)){
                    ASSERT_LT(fabs(lon - lonLat.lon), 0.0001);
                }
                else{
                    ASSERT_LT(fabs(lon - 360.0 - lonLat.lon), 0.0001);
                }
                ASSERT_LT(fabs(lat - lonLat.lat), 0.0001);
            }
        }
    }
    XY xyA = lonLatToXY(-179.0, 89.9);
    XY xyB = lonLatToXY(181.0, 89.9);
    EXPECT_EQ(xyA.x, xyB.x);
    EXPECT_EQ(xyA.y, xyB.y);

    xyA = lonLatToXY(-179.0, -89.9);
    xyB = lonLatToXY(181.0, -89.9);
    EXPECT_EQ(xyA.x, xyB.x);
    EXPECT_EQ(xyA.y, xyB.y);

    xyA = lonLatToXY(-1.0, 89.9);
    xyB = lonLatToXY(359.0, 89.9);
    EXPECT_EQ(xyA.x, xyB.x);
    EXPECT_EQ(xyA.y, xyB.y);

    xyA = lonLatToXY(-1.0, -89.9);
    xyB = lonLatToXY(359.0, -89.9);
    EXPECT_EQ(xyA.x, xyB.x);
    EXPECT_EQ(xyA.y, xyB.y);
}

// Tests plotGrid.
TEST_F(HammerTest, testPlotGrid) {
    string plotName("/Volumes/external/azuri/data/grid.png");
    plotGrid(plotName);
}

// Tests isInside
TEST_F(HammerTest, testIsInside) {
    double x = 0.0;
    double y = 0.0;
    ASSERT_TRUE(isInside(x,y));

    x = _OuterLimitsXY[0].x + 0.1;
    y = _OuterLimitsXY[0].y + 0.1;
    ASSERT_FALSE(isInside(x,y));

    x = _OuterLimitsXY[0].x + 0.1;
    y = _OuterLimitsXY[1].y - 0.1;
    ASSERT_FALSE(isInside(x,y));

    x = _OuterLimitsXY[1].x - 0.1;
    y = _OuterLimitsXY[0].y + 0.1;
    ASSERT_FALSE(isInside(x,y));

    x = _OuterLimitsXY[1].x - 0.1;
    y = _OuterLimitsXY[1].y - 0.1;
    ASSERT_FALSE(isInside(x,y));

    LonLat lonLat(99.9492, -88.0949);
    XY xy = lonLatToXY(lonLat);
    Debug_isInside = true;
    ASSERT_TRUE(isInside(xy.x,xy.y));
    Debug_isInside = false;
}

// Tests isInPixel
TEST_F(HammerTest, testIsInPixel) {
    Pixel pixel;
    pixel.xLow = 1.0;
    pixel.xHigh = 1.5;
    pixel.yLow = 1.0;
    pixel.yHigh = 1.5;
    XY xy;
    xy.x = 0.0;
    xy.y = 0.0;
    ASSERT_FALSE(isInPixel(pixel,xy));
    xy.x = 1.1;
    ASSERT_FALSE(isInPixel(pixel,xy));
    xy.y = 1.1;
    ASSERT_TRUE(isInPixel(pixel,xy));
}

TEST_F(HammerTest, testGetPixels){
    vector<Pixel> pix = getPixels();
    double lon = 0.00555304;
    double lat = -80.8856;
    LonLat lonLat;
    lonLat.lon = lon;
    lonLat.lat = lat;
    XY xy = lonLatToXY(lonLat);
    cout << "lon = " << lon << ", lat = " << lat << ": x = " << xy.x << ", y = " << xy.y << endl;
    if (isInside(xy))
        cout << "lonLat is inside" << endl;
    else{
        cout << "lonLat is NOT inside" << endl;
        exit(EXIT_FAILURE);
    }
    bool lonLatFound = false;
    for (int iPix=0; iPix<pix.size(); ++iPix){
        Pixel pixel = pix[iPix];
        if (isInPixel(pixel, xy)){
            cout << "lonLat found in pixel[" << pixel.xLow << ", " << pixel.xHigh << ", " << pixel.yLow << ", " << pixel.yHigh << "]" << endl;
            lonLatFound = true;
        }
    }
    if (!lonLatFound){
        cout << "ERROR: lonLat not found in any pixel" << endl;
        exit(EXIT_FAILURE);
    }
}

}  // namespace

int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
