#include "../galaxia.h"
#include "gtest/gtest.h"

using namespace std;

namespace {

// The fixture for testing class Galcomp.
class GalaxiaTest : public ::testing::Test {
 protected:
  // You can remove any or all of the following functions if its body
  // is empty.

  GalaxiaTest() {
    // You can do set-up work for each test here.
  }

  virtual ~GalaxiaTest() {
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
TEST_F(GalaxiaTest, testGetAEbfFactor) {
    string band("sdss_u");
    EXPECT_EQ(getAEbfFactor(band), 5.155);
    band = "sdss_g";
    EXPECT_EQ(getAEbfFactor(band), 3.793);
    band = "sdss_r";
    EXPECT_EQ(getAEbfFactor(band), 2.751);
    band = "sdss_i";
    EXPECT_EQ(getAEbfFactor(band), 2.086);
    band = "sdss_z";
    EXPECT_EQ(getAEbfFactor(band), 1.479);
    band = "sdss_a";
    try{
        getAEbfFactor(band);
    }
    catch (const std::exception& e) {
        EXPECT_EQ(e.what(), "getAEbfFactor: unknown band <" + band + ">");
    }
}

}  // namespace

int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
