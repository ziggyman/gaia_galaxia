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
    Hammer hammer;
    hammer.calcOuterLimits();
    double xMinExpected = -2.82843;
    double xMaxExpected = 2.82843;
    double yMinExpected = -1.41421;
    double yMaxExpected = 1.41421;
    EXPECT_LT(fabs(xMinExpected - hammer.getOuterLimitsXY()[0].x), 0.00001);
    EXPECT_LT(fabs(xMaxExpected - hammer.getOuterLimitsXY()[1].x), 0.00001);
    EXPECT_LT(fabs(yMinExpected - hammer.getOuterLimitsXY()[0].y), 0.00001);
    EXPECT_LT(fabs(yMaxExpected - hammer.getOuterLimitsXY()[1].y), 0.00001);
}

TEST_F(HammerTest, testXYAndLonLat){
    vector<double> lonLowLimit(2);
    lonLowLimit[0] = -179.999;
    lonLowLimit[1] = 0.00001;
    vector<double> lonHighLimit(2);
    lonHighLimit[0] = 180.0;
    lonHighLimit[1] = 360.0;
    Hammer hammer;

    for (int iRun = 0; iRun < 2; ++iRun){
        for (double lon=lonLowLimit[iRun]; lon<lonHighLimit[iRun]; lon+=0.1){
            for (double lat=-89.9; lat<89.99; lat+=0.1){
                XY xy = hammer.lonLatToXY(lon, lat);
                LonLat lonLat = hammer.xYToLonLat(xy.x, xy.y);
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
    XY xyA = hammer.lonLatToXY(-179.0, 89.9);
    XY xyB = hammer.lonLatToXY(181.0, 89.9);
    EXPECT_EQ(xyA.x, xyB.x);
    EXPECT_EQ(xyA.y, xyB.y);

    xyA = hammer.lonLatToXY(-179.0, -89.9);
    xyB = hammer.lonLatToXY(181.0, -89.9);
    EXPECT_EQ(xyA.x, xyB.x);
    EXPECT_EQ(xyA.y, xyB.y);

    xyA = hammer.lonLatToXY(-1.0, 89.9);
    xyB = hammer.lonLatToXY(359.0, 89.9);
    EXPECT_EQ(xyA.x, xyB.x);
    EXPECT_EQ(xyA.y, xyB.y);

    xyA = hammer.lonLatToXY(-1.0, -89.9);
    xyB = hammer.lonLatToXY(359.0, -89.9);
    EXPECT_EQ(xyA.x, xyB.x);
    EXPECT_EQ(xyA.y, xyB.y);
}

// Tests plotGrid.
TEST_F(HammerTest, testPlotGrid) {
    string plotName("/Volumes/external/azuri/data/grid.png");
    Hammer hammer;
    hammer.plotGrid(plotName);
}

// Tests isInside
TEST_F(HammerTest, testIsInside) {
    double x = 0.0;
    double y = 0.0;
    Hammer hammer;
    vector<XY> outerLimitsXY = hammer.getOuterLimitsXY();
    EXPECT_TRUE(hammer.isInside(x,y));

    x = outerLimitsXY[0].x + 0.1;
    y = outerLimitsXY[0].y + 0.1;
    EXPECT_FALSE(hammer.isInside(x,y));

    x = outerLimitsXY[0].x + 0.1;
    y = outerLimitsXY[1].y - 0.1;
    EXPECT_FALSE(hammer.isInside(x,y));

    x = outerLimitsXY[1].x - 0.1;
    y = outerLimitsXY[0].y + 0.1;
    EXPECT_FALSE(hammer.isInside(x,y));

    x = outerLimitsXY[1].x - 0.1;
    y = outerLimitsXY[1].y - 0.1;
    EXPECT_FALSE(hammer.isInside(x,y));

    LonLat lonLat(99.9492, -88.0949);
    XY xy = hammer.lonLatToXY(lonLat);
    hammer.setDebug_isInside(true);
    EXPECT_TRUE(hammer.isInside(xy.x,xy.y));
    hammer.setDebug_isInside(false);

    lonLat.lon = 180.716;
    lonLat.lat = 71.9804;
    xy = hammer.lonLatToXY(lonLat);
    cout << "xy.x = " << xy.x << ", xy.y = " << xy.y << endl;
    cout << "_OuterLimitsXY[0]: x=" << outerLimitsXY[0].x << ", y=" << outerLimitsXY[0].y << endl;;
    cout << "_OuterLimitsXY[1]: x=" << outerLimitsXY[1].x << ", y=" << outerLimitsXY[1].y << endl;;
    hammer.setDebug_isInside(true);
    EXPECT_TRUE(hammer.isInside(xy.x,xy.y));
    hammer.setDebug_isInside(false);

}

// Tests isInPixel
TEST_F(HammerTest, testPixelIsInside) {
    Pixel pixel;
    pixel.xLow = 1.0;
    pixel.xHigh = 1.5;
    pixel.yLow = 1.0;
    pixel.yHigh = 1.5;
    XY xy;
    xy.x = 0.0;
    xy.y = 0.0;
    ASSERT_FALSE(pixel.isInside(xy));
    xy.x = 1.1;
    ASSERT_FALSE(pixel.isInside(xy));
    xy.y = 1.1;
    ASSERT_TRUE(pixel.isInside(xy));
}

TEST_F(HammerTest, testGetPixels){
    Hammer hammer;
    vector<Pixel> pix = hammer.getPixels();
    double lon = 180.716;
    double lat = 71.9804;
    LonLat lonLat;
    lonLat.lon = lon;
    lonLat.lat = lat;
    XY xy = hammer.lonLatToXY(lonLat);
    cout << "lon = " << lon << ", lat = " << lat << ": x = " << xy.x << ", y = " << xy.y << endl;
    if (hammer.isInside(xy))
        cout << "lonLat is inside" << endl;
    else{
        cout << "lonLat is NOT inside" << endl;
        exit(EXIT_FAILURE);
    }
    bool lonLatFound = false;
    hammer.setDebug_isInside(true);
    for (auto itPix=pix.begin(); itPix!=pix.end(); ++itPix){
        if (itPix->isInside(xy)){
            cout << "lonLat found in pixel[" << itPix->xLow << ", " << itPix->xHigh << ", " << itPix->yLow << ", " << itPix->yHigh << "]" << endl;
            lonLatFound = true;
        }
        else{
            cout << "lonLat NOT found in pixel[" << itPix->xLow << ", " << itPix->xHigh << ", " << itPix->yLow << ", " << itPix->yHigh << "]" << endl;
        }
    }
    hammer.setDebug_isInside(false);
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
