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
TEST_F(GalCompTest, testGetGaiaObject) {
    cout << "running testReadCSVFile" << endl;
    string fileName("/Volumes/external/azuri/data/gaia/xy/GaiaSource_0.017678-0.035355_-0.583363--0.565685.csv");
    CSVData csvData = readCSVFile(fileName);
    cout << "csvData.header.size() = " << csvData.header.size() << ", csvData.data.size() = "
            << csvData.data.size() << ", csvData.data[0].size() = " << csvData.data[0].size() << endl;
    ASSERT_GT(csvData.header.size(), 1);
    ASSERT_GT(csvData.data.size(), 1);
    ASSERT_EQ(csvData.data[0].size(), csvData.header.size());
    vector<string> ids = csvData.getData("source_id");
    for (int iRow=0; iRow<csvData.header.size(); ++iRow){
        string id = csvData.getData("source_id", iRow);
        int nTimes = existsHowManyTimes(ids, id);
        cout << "id=<" << id << "> exists " << nTimes << endl;
        EXPECT_EQ(nTimes, 1);
    }
}


}  // namespace

int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
