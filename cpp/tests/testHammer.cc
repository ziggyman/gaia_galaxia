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
/*  for (int i=0; i<lonLatXY.size(); ++i)
      cout << "lonLatXY[" << i << "]: lon = " << lonLatXY[i].lonLat.lon
              << ", lat = " << lonLatXY[i].lonLat.lat
              << ", x = " << lonLatXY[i].xy.x
              << ", y = " << lonLatXY[i].xy.y << endl;
 */
//  EXPECT_EQ(0, f.Bar(input_filepath, output_filepath));
}

TEST_F(HammerTest, testXYAndLonLat){
    for (double lon=-179.9; lon<180.0; lon+=0.1){
        for (double lat=-89.9; lat<89.99; lat+=0.1){
            XY xy = lonLatToXY(lon, lat);
            LonLat lonLat = xYToLonLat(xy.x, xy.y);
/*            cout << "lon = " << lon
                 << ", lat = " << lat
                 << ": x = " << xy.x
                 << ", y = " << xy.y
                 << ", lonLat.lon = " << lonLat.lon
                 << ", lonLat.lat = " << lonLat.lat << endl;*/
            ASSERT_LT(fabs(lon - lonLat.lon), 0.0001);
            ASSERT_LT(fabs(lat - lonLat.lat), 0.0001);
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
    for (int iPix=0; iPix<pix.size(); ++iPix){
        Pixel pixel = pix[iPix];
    }
}

}  // namespace

int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
