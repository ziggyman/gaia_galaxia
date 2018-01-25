#include "../galaxyMath.h"
#include "gtest/gtest.h"

namespace {

// The fixture for testing class Math.
class MathTest : public ::testing::Test {
 protected:
  // You can remove any or all of the following functions if its body
  // is empty.

  MathTest() {
    // You can do set-up work for each test here.
  }

  virtual ~MathTest() {
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

  // Objects declared here can be used by all tests in the test case for Math.
};

// Tests that the Math::Bar() method does Abc.
TEST_F(MathTest, testGenerateSequence) {
    unsigned start=0;
    unsigned stop=10;
    vector<unsigned> sequence = generateSequence(start,stop);
    for (unsigned i=start; i<=stop; ++i){
        EXPECT_EQ(i, sequence[i]);
    }
}

// Tests that the Math::Bar() method does Abc.
TEST_F(MathTest, testGenerateRandomSequence) {
    unsigned start=0;
    unsigned stop=10;
    vector<unsigned> sequence = generateSequence(start, stop);
    vector<unsigned> randomSequence = generateRandomSequence(start, stop, 0);
    vector<unsigned> randomSequenceA = generateRandomSequence(start, stop, 1);
    vector<unsigned> randomSequenceB = generateRandomSequence(start, stop, 1);
    unsigned nEq = 0;
    for (unsigned i=0; i<=(stop-start); ++i){
        cout << "testGenerateRandomSequence: i=" << i << ": sequence[" << i << "] = " << sequence[i]
                << ", randomSequence[" << i << "] = " << randomSequence[i]
                << ", randomSequenceA[" << i << "] = " << randomSequenceA[i]
                << ", randomSequenceB[" << i << "] = " << randomSequenceB[i]
                << endl;
        EXPECT_NE(find(sequence.begin(), sequence.end(), randomSequence[i]), sequence.end());
        EXPECT_NE(find(randomSequence.begin(), randomSequence.end(), sequence[i]), randomSequence.end());
        EXPECT_NE(find(sequence.begin(), sequence.end(), randomSequenceA[i]), sequence.end());
        EXPECT_NE(find(randomSequenceA.begin(), randomSequenceA.end(), sequence[i]), randomSequenceA.end());
        EXPECT_NE(find(sequence.begin(), sequence.end(), randomSequenceB[i]), sequence.end());
        EXPECT_NE(find(randomSequenceB.begin(), randomSequenceB.end(), sequence[i]), randomSequenceB.end());
        EXPECT_EQ(randomSequenceB[i], randomSequenceA[i]);
        if (randomSequence[i] == randomSequenceA[i]){
            ++nEq;
        }
    }
    cout << "testGenerateRandomSequence: nEq = " << nEq << endl;
    EXPECT_NE(nEq, stop-start+1);

    /// test with stop==start
    stop=0;
    sequence = generateSequence(start, stop);
    randomSequence = generateRandomSequence(start, stop, 0);
    randomSequenceA = generateRandomSequence(start, stop, 1);
    randomSequenceB = generateRandomSequence(start, stop, 1);
    nEq = 0;
    for (unsigned i=0; i<=(stop-start); ++i){
        cout << "testGenerateRandomSequence: i=" << i << ": sequence[" << i << "] = " << sequence[i]
                << ", randomSequence[" << i << "] = " << randomSequence[i]
                << ", randomSequenceA[" << i << "] = " << randomSequenceA[i]
                << ", randomSequenceB[" << i << "] = " << randomSequenceB[i]
                << endl;
        EXPECT_NE(find(sequence.begin(), sequence.end(), randomSequence[i]), sequence.end());
        EXPECT_NE(find(randomSequence.begin(), randomSequence.end(), sequence[i]), randomSequence.end());
        EXPECT_NE(find(sequence.begin(), sequence.end(), randomSequenceA[i]), sequence.end());
        EXPECT_NE(find(randomSequenceA.begin(), randomSequenceA.end(), sequence[i]), randomSequenceA.end());
        EXPECT_NE(find(sequence.begin(), sequence.end(), randomSequenceB[i]), sequence.end());
        EXPECT_NE(find(randomSequenceB.begin(), randomSequenceB.end(), sequence[i]), randomSequenceB.end());
        EXPECT_EQ(randomSequenceB[i], randomSequenceA[i]);
    }

    /// test with start > stop
    start=1;
    stop=0;
    try{
        sequence = generateSequence(start, stop);
    }
    catch(std::runtime_error &e){
        string message="generateSequence: ERROR: max(="+to_string(stop)+") < min(="+to_string(start)+")";
        EXPECT_EQ(message, e.what());
    }
    try{
        randomSequence = generateRandomSequence(start, stop, 0);
    }
    catch(std::runtime_error &e){
        string message="generateRandomSequence: ERROR: max(="+to_string(stop)+") < min(="+to_string(start)+")";
        EXPECT_EQ(message, e.what());
    }
}

// Tests that the Math::Bar() method does Abc.
TEST_F(MathTest, testGenerateRandomSequenceN) {
    unsigned start=0;
    unsigned stop=10;

    ///test with n == stop-start+1
    unsigned n=11;
    vector<unsigned> sequence = generateSequence(start, stop);
    vector<unsigned> randomSequence = generateRandomSequence(start, stop, n, 0);
    vector<unsigned> randomSequenceA = generateRandomSequence(start, stop, n, 1);
    vector<unsigned> randomSequenceB = generateRandomSequence(start, stop, n, 1);
    unsigned nEq = 0;
    for (unsigned i=0; i<n; ++i){
        cout << "testGenerateRandomSequenceN: i=" << i << ": sequence[" << i << "] = " << sequence[i]
                << ", randomSequence[" << i << "] = " << randomSequence[i]
                << ", randomSequenceA[" << i << "] = " << randomSequenceA[i]
                << ", randomSequenceB[" << i << "] = " << randomSequenceB[i]
                << endl;
        EXPECT_NE(find(sequence.begin(), sequence.end(), randomSequence[i]), sequence.end());
        EXPECT_NE(find(randomSequence.begin(), randomSequence.end(), sequence[i]), randomSequence.end());
        EXPECT_NE(find(sequence.begin(), sequence.end(), randomSequenceA[i]), sequence.end());
        EXPECT_NE(find(randomSequenceA.begin(), randomSequenceA.end(), sequence[i]), randomSequenceA.end());
        EXPECT_NE(find(sequence.begin(), sequence.end(), randomSequenceB[i]), sequence.end());
        EXPECT_NE(find(randomSequenceB.begin(), randomSequenceB.end(), sequence[i]), randomSequenceB.end());
        EXPECT_EQ(randomSequenceB[i], randomSequenceA[i]);
        if (randomSequence[i] == randomSequenceA[i]){
            ++nEq;
        }
    }
    cout << "testGenerateRandomSequenceN: nEq = " << nEq << endl;
    EXPECT_NE(nEq, n);

    ///test with n < stop-start+1
    n=9;
    randomSequence = generateRandomSequence(start, stop, n, 0);
    EXPECT_EQ(randomSequence.size(), n);
    randomSequenceA = generateRandomSequence(start, stop, n, 1);
    EXPECT_EQ(randomSequenceA.size(), n);
    randomSequenceB = generateRandomSequence(start, stop, n, 1);
    EXPECT_EQ(randomSequenceB.size(), n);
    cout << "testGenerateRandomSequenceN: randomSequence.size() = " << randomSequence.size() << endl;
    nEq = 0;
    for (unsigned i=0; i<n; ++i){
        cout << "testGenerateRandomSequenceN: i=" << i << ": sequence[" << i << "] = " << sequence[i]
                << ", randomSequence[" << i << "] = " << randomSequence[i]
                << ", randomSequenceA[" << i << "] = " << randomSequenceA[i]
                << ", randomSequenceB[" << i << "] = " << randomSequenceB[i]
                << endl;
        EXPECT_NE(find(sequence.begin(), sequence.end(), randomSequence[i]), sequence.end());
        EXPECT_NE(find(sequence.begin(), sequence.end(), randomSequenceA[i]), sequence.end());
        EXPECT_NE(find(sequence.begin(), sequence.end(), randomSequenceB[i]), sequence.end());
        EXPECT_EQ(randomSequenceB[i], randomSequenceA[i]);
        if (randomSequence[i] == randomSequenceA[i]){
            ++nEq;
        }
    }
    cout << "testGenerateRandomSequenceN: nEq = " << nEq << endl;
    EXPECT_NE(nEq, n);

    ///test with n > stop - start + 1
    start = 1;
    stop = 7;
    n=9;
    try{
        randomSequence = generateRandomSequence(start, stop, n, 0);
    }
    catch(std::runtime_error &e){
        string message="generateRandomSequence: ERROR: n="+to_string(n)+" > (max-min+1)(="+to_string(stop-start+1)+")";
        EXPECT_EQ(message, e.what());
    }

    ///test with start > stop
    start = 3;
    stop = 2;
    n=0;
    try{
        randomSequence = generateRandomSequence(start, stop, n, 0);
    }
    catch(std::runtime_error &e){
        string message="generateRandomSequence: ERROR: max(="+to_string(stop)+") < min(="+to_string(start)+")";
        EXPECT_EQ(message, e.what());
    }

    /// test with start == stop
    start = 1;
    stop = 1;
    n=1;
    randomSequence = generateRandomSequence(start, stop, n, 0);
    EXPECT_EQ(randomSequence.size(), n);
    randomSequenceA = generateRandomSequence(start, stop, n, 1);
    EXPECT_EQ(randomSequenceA.size(), n);
    randomSequenceB = generateRandomSequence(start, stop, n, 1);
    EXPECT_EQ(randomSequenceB.size(), n);
    cout << "testGenerateRandomSequenceN: randomSequence.size() = " << randomSequence.size() << endl;
    for (unsigned i=0; i<n; ++i){
        cout << "testGenerateRandomSequenceN: i=" << i << ": sequence[" << i << "] = " << sequence[i]
                << ", randomSequence[" << i << "] = " << randomSequence[i]
                << ", randomSequenceA[" << i << "] = " << randomSequenceA[i]
                << ", randomSequenceB[" << i << "] = " << randomSequenceB[i]
                << endl;
        EXPECT_NE(find(sequence.begin(), sequence.end(), randomSequence[i]), sequence.end());
        EXPECT_NE(find(sequence.begin(), sequence.end(), randomSequenceA[i]), sequence.end());
        EXPECT_NE(find(sequence.begin(), sequence.end(), randomSequenceB[i]), sequence.end());
        EXPECT_EQ(randomSequenceB[i], randomSequenceA[i]);
    }

    ///test with n==0
    n=0;
    randomSequence = generateRandomSequence(start, stop, n, 0);
    EXPECT_EQ(randomSequence.size(), n);
}

// Tests that the Math::Bar() method does Abc.
TEST_F(MathTest, testHistogramMakeBinLimits) {
    Histogram hist;
    double start = 0;
    double end = 10;
    unsigned nSteps=10;
    hist.makeBinLimits(start, end, nSteps);
    for (unsigned i=0; i<10; ++i){
        EXPECT_EQ(i, hist.limits[i].first);
        EXPECT_EQ(i+1, hist.limits[i].second);
    }
}

TEST_F(MathTest, testHistogramMake) {
    Histogram hist;
    double start = 0;
    double end = 10;
    unsigned nSteps=10;
    hist.makeBinLimits(start, end, nSteps);
//    for (unsigned i=0; i<hist.limits.size(); ++i){
//        cout << "testHistogramMake: hist.limits[" << i << "] = [" << hist.limits[i].first << ", " << hist.limits[i].second << "]" << endl;
//    }

    vector<double> dblVec = generateSequence(0.0, 10.0, 0.1);
    hist.make(dblVec);
//    for (unsigned i=0; i<hist.indices.size(); ++i){
//        for (unsigned j=0; j<hist.indices[i].size(); ++j)
//            cout << "testHistogramMake: hist.indices[" << i << "][" << j << "] = " << hist.indices[i][j] << ": dblVec[" << hist.indices[i][j] << "] = " << dblVec[hist.indices[i][j]] << endl;
//    }

    for (unsigned i=0; i<10; ++i){
        EXPECT_EQ(hist.indices[i].size(), 10);
        for (unsigned j=0; j<hist.indices[i].size(); ++j)
            EXPECT_EQ(hist.indices[i][j], i*10+j);
    }
}

TEST_F(MathTest, testHistogramFillRandomly) {
    Histogram hist;
    double start = 0;
    double end = 10;
    unsigned nSteps=10;
    hist.makeBinLimits(start, end, nSteps);

    vector<double> dblVec = generateSequence(0.0, 10.0, 0.1);
    hist.make(dblVec);

    unsigned seed = 1;
    vector< vector< unsigned > > rndInd = hist.fillRandomly(dblVec, seed);
    cout << "testHistogramFillRandomly: seed = " << seed << endl;

    for (unsigned i=0; i<10; ++i){
        for (unsigned j=0; j<hist.indices[i].size(); ++j){
            cout << "testHistogramFillRandomly: hist.indices[" << i << "][" << j << "] = " << hist.indices[i][j] << endl;
            cout << "testHistogramFillRandomly: rndInd[" << i << "][" << j << "] = " << rndInd[i][j] << endl;
            EXPECT_NE(find(hist.indices[i].begin(), hist.indices[i].end(), rndInd[i][j]), hist.indices[i].end());
        }
    }
}

TEST_F(MathTest, testDegToRad) {
    double deg = 0.0;
    double rad = degToRad(deg);
    EXPECT_EQ(rad, deg);
    EXPECT_EQ(radToDeg(rad), deg);

    deg = 180.0;
    rad = degToRad(deg);
    EXPECT_EQ(rad, M_PI);
    EXPECT_EQ(radToDeg(rad), deg);

    deg = 360.0;
    rad = degToRad(deg);
    EXPECT_EQ(rad, 2.0 * M_PI);
    EXPECT_EQ(radToDeg(rad), deg);

    deg = 90.0;
    rad = degToRad(deg);
    EXPECT_EQ(rad, M_PI / 2.0);
    EXPECT_EQ(radToDeg(rad), deg);

    deg = -90.0;
    rad = degToRad(deg);
    EXPECT_EQ(rad, 0.0 - (M_PI / 2.0));
    EXPECT_EQ(radToDeg(rad), deg);
}

TEST_F(MathTest, testMuRaDecToMuLB) {
    double ra = 0.0;
    double dec = 0.0;
    double muRa = 0.0;
    double muDec = 0.0;
    pair<double, double> res = muRaDecToMuLB(muRa, muDec, ra, dec);
    cout << "testRaDecToLB: ra = " << ra << ", dec = " << dec << ": l = " << radToDeg(res.first) << " deg, b = " << radToDeg(res.second) << " deg" << endl;
}

}  // namespace

int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
