#include "galaxyMath.h"

void Histogram::makeBinLimits(double startIn, double endIn, unsigned nBinsIn){
    start = startIn;
    end = endIn;
    nBins = nBinsIn;
    double step = (end - start) / double(nBins);
    limits.resize(nBins);

    double binStart = start;
    double binEnd = start + step;
    for (auto itBin=limits.begin(); itBin!=limits.end(); ++itBin, binStart+=step, binEnd+=step){
        itBin->first = binStart;
        itBin->second = binEnd;
    }
}

template< typename T >
void Histogram::make(vector<T> const& vecIn){
    indices.resize(nBins);
    double step = (end - start) / double(nBins);
    unsigned idx = 0;
    for (auto it=vecIn.begin(); it!=vecIn.end(); ++it, ++idx){
        T res = ((*it) - T(start)) / T(step);
        int iStep = stoi(to_string(res));/// required to avoid wrong conversions from double to int
//        cout << "Histogram::make: *it=" << *it << ", start = " << start << ", step = " << step << ": res = " << res << ": iStep = " << iStep << endl;
        if ((iStep >= 0) && (iStep < nBins)){
            indices[unsigned(iStep)].push_back(idx);
//            cout << "Histogram::make: indices[" << iStep << "].size() = " << indices[iStep].size() << endl;
        }
    }
}
template void Histogram::make(vector<double> const&);

template< typename T >
vector< vector< unsigned > > Histogram::fillRandomly(vector< T > const& dataIn, unsigned & seed){
//    cout << "Histogram::fillRandomly: dataIn.size() = " << dataIn.size() << endl;
//    for (T const& x: dataIn) cout << x << ", ";
//    cout << endl;
    vector< vector< unsigned > > out(indices.size());

    /// create Histogram for dataIn
    Histogram allDataHist;
    allDataHist.start = start;
    allDataHist.end = end;
    allDataHist.nBins = nBins;
    allDataHist.limits = limits;
    allDataHist.make(dataIn);
    cout << "Histogram::fillRandomly: allDataHist constructed" << endl;
    unsigned i=0;
    for (auto it=allDataHist.indices.begin(); it!=allDataHist.indices.end(); ++it, ++i)
        cout << "Histogram::fillRandomly: allDataHist.indices[" << i << "].size() = " << it->size() << endl;

    int iBin=0;
    for (auto itAll=allDataHist.indices.begin(), it=indices.begin();
         itAll!=allDataHist.indices.end();
         ++itAll, ++it, ++iBin){
        if (itAll->size() < it->size())
            throw std::runtime_error("Histogram::fillRandomly: ERROR: itAll->size(="+to_string(itAll->size())+") < it->size(="+to_string(it->size())+")");
        cout << "Histogram::fillRandomly: running iBin = " << iBin << ": it->size() = " << it->size() << ", itAll->size() = " << itAll->size() << endl;
        vector<unsigned> tmpVec;
        if (itAll->size() > 0){
            tmpVec = generateRandomSequence(0, itAll->size()-1, it->size(), seed += iBin);

            cout << "Histogram::fillRandomly: tmpVec.size() = " << tmpVec.size() << endl;
            for (auto itTmpVec=tmpVec.begin(); itTmpVec!=tmpVec.end(); ++itTmpVec){
                cout << "Histogram::fillRandomly: iBin=" << iBin << ": allDataHist.indices[" << iBin << "][" << *itTmpVec << "] = " << allDataHist.indices[iBin][*itTmpVec] << endl;
                out[iBin].push_back((*itAll)[*itTmpVec]);
            }
        }
    }
    return out;
}
template vector< vector< unsigned > > Histogram::fillRandomly(vector< double > const&, unsigned &);
/*
vector< vector< pair< double, double > > > Histogram::convolveWithObservationErrors(
    vector<double> const& dataIn,
    Histogram const& errorsObs)
{

}*/

template< typename T >
vector<T> generateSequence(T min, T max, T step){
    if (max < min){
        throw std::runtime_error("generateSequence: ERROR: max(="+to_string(max)+") < min(="+to_string(min)+")");
    }
    if (step < 0){
        throw std::runtime_error("generateSequence: ERROR: step currently needs to be > 0");
    }
    vector<T> vec(0);
//    vec.reserve(max-min+1);
    for (T i=min; i<=max; i+=step)
        vec.push_back(i);
    return vec;
}
template vector<unsigned> generateSequence(unsigned, unsigned, unsigned);
template vector<double> generateSequence(double, double, double);

vector<unsigned> generateRandomSequence(unsigned min, unsigned max, unsigned seed){
    if (max < min){
        throw std::runtime_error("generateRandomSequence: ERROR: max(="+to_string(max)+") < min(="+to_string(min)+")");
    }

    /// create vector and fill with ints from min to max
    vector<unsigned> vec = generateSequence(min, max);

    /// set random generator seed
    if (seed == 0){
        std::random_device rd;//Will be used to obtain a seed for the random number engine
        seed = rd();
    }

    shuffle (vec.begin(), vec.end(), std::default_random_engine(seed));

    return vec;
}

vector<unsigned> generateRandomSequence(unsigned min, unsigned max, unsigned n, unsigned seed){
    if (n > (max-min+1)){
        throw std::runtime_error("generateRandomSequence: ERROR: n="+to_string(n)
                +" > (max(="+to_string(max)+")-min(="+to_string(min)+")+1)(="
                +to_string(max-min+1)+")");
    }
    else if (n == (max-min+1)){
        return generateRandomSequence(min, max, seed);
    }
    if (max < min){
        throw std::runtime_error("generateRandomSequence: ERROR: max(="+to_string(max)+") < min(="+to_string(min)+")");
    }

    /// set random generator seed
    if (seed == 0){
        std::random_device rd;//Will be used to obtain a seed for the random number engine
        seed = rd();
    }

    //Standard mersenne_twister_engine seeded with seed
    std::mt19937 gen(seed);

    /// Initialize Uniform int distribution
    std::uniform_int_distribution<> dis(min, max);

    /// create vector and fill with ints from min to max
    vector<unsigned> vec(n);

    for (unsigned i=0; i<n; ++i){
        vec[i] = dis(gen);
        if (i > 0){
            while (find(vec.begin(), vec.begin()+i, vec[i]) != vec.begin()+i){
                vec[i] = dis(gen);
            }
        }
    }

//    std::cout << "shuffled elements:";
//    for (int& x: vec) std::cout << ' ' << x;
//    std::cout << '\n';

    return vec;
}

double degToRad(double rad){
    return rad * 2.0 * M_PI / 360.0;
}

double radToDeg(double deg){
    return deg * 360.0 / (2.0 * M_PI);
}

pair<double, double> muRaDecToMuLB(double muRa, double muDec, double ra, double dec){
//    double b = asin((sin(dec) * cos(degToRad(62.6))) - (cos(dec) * sin(ra - degToRad(282.25)) * sin(degToRad(62.6))));
//    double l = acos(cos(dec) * cos(ra - degToRad(282.25)) / cos(b)) + degToRad(33.0);
    double alphaG = degToRad(192.85948);
    double deltaG = degToRad(27.12825);
//    double lOmega = degToRad(32.93192);

    double muRaStar = muRa * cos(dec);

    double cA = (sin(deltaG) * cos(dec)) - (cos(deltaG) * sin(dec) * cos(ra - alphaG));
    double cB = cos(deltaG) * sin(ra - alphaG);

    double oneOverCosB = sqrt((cA * cA) + (cB * cB));

    double muLStar = oneOverCosB * ((cA * muRaStar) + (cB * muDec));
    double muB = oneOverCosB * ((cA * muDec) - (cB * muRaStar));

    double muL = muLStar * oneOverCosB;

    return pair<double, double>(muL, muB);
}

double parallaxToDistance(double par){
    return 1.0 / par / 1000.0;
}
/*int random(int min, int max, unsigned seed){
    std::mt19937 gen;

    if (seed==0){
        std::random_device rd;//Will be used to obtain a seed for the random number engine
        gen.seed(rd())
    }
    else{
        gen.seed(seed);//Standard mersenne_twister_engine seeded with rd()
    }

}*/

double calcGaiaGFromgri(double const& sdss_g, double const& sdss_r, double const& sdss_i){
    double rMinusI = sdss_r - sdss_i;
    double gMinusR = sdss_g - sdss_r;
    return 0.0 - 0.0992
               - (0.5749 * rMinusI)
               - (0.2427 * rMinusI * rMinusI)
               + (0.0365 * rMinusI * rMinusI * rMinusI)
               - (0.5277 * gMinusR)
               - (0.1158 * gMinusR * gMinusR)
               + (0.0086 * gMinusR * gMinusR * gMinusR)
               - (0.0337 * gMinusR * rMinusI)
               + sdss_g;
}

double calcIcFromBVg(double const& ubv_b, double const& ubv_v, double const& g){
    double c1, c2, c3, c4, c5, c6, c7, c8, fm, to, shfx, shfy, ord;
    if (g < 3.5){/// giants
        c1 = -0.008879586;
        c2 = 0.7390707;
        c3 = 0.3271480;
        c4 = 1.140169;
        c5 = -0.1908637;
        c6 = -0.7898824;
        c7 = 0.5190744;
        c8 = -0.5358868;
        fm = -0.25;
        to = 1.75;
        shfx = 1.0;
        shfy = 1.0;
        ord = 7.0;
    }
    else{/// dwarfs
        c1 = 0.0890659;
        c2 = 1.319675;
        c3 = 0.4461807;
        c4 = -1.188127;
        c5 = 0.2465572;
        c6 = 8.478627;
        c7 = 10.46599;
        c8 = 3.641226;
        fm = -0.23;
        to = 1.40;
        shfx = 1.0;
        shfy = 1.0;
        ord = 7.0;
    }
    double x = ubv_b - ubv_v - shfx;
    double y =
}

double calcGaiaGFromBV(double const& ubv_b, double const& ubv_v){

}
