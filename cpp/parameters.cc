#include "parameters.h"

boost::format modelGetFileNameOutRoot(){
    return boost::format("galaxia_%06f-%06f_%06f-%06f.csv");// % (float(minX), float(maxX), float(minY), float(maxY))
}

boost::format obsGetFileNameOutRoot(string const& whichOne){
    if (whichOne.compare("gaia") == 0)
        return gaiaGetFileNameOutRoot();
    else if (whichOne.compare("gaiaTgas") == 0)
        return gaiaTgasGetFileNameOutRoot();
    else
        throw std::runtime_error("obsGetFileNameOutRoot: ERROR: whichOne = <"+whichOne+"> not recognized");
}

boost::format gaiaGetFileNameOutRoot(){
    return boost::format("GaiaSource_%06f-%06f_%06f-%06f.csv");// % (float(minX), float(maxX), float(minY), float(maxY))
}

boost::format gaiaTgasGetFileNameOutRoot(){
    return boost::format("TgasSource_%06f-%06f_%06f-%06f.csv");// % (float(minX), float(maxX), float(minY), float(maxY))
}

string modelGetDataDirOut(){
//    return "/Volumes/yoda/azuri/data/galaxia/xy_ubv_Vlt13/";
    return "/Volumes/yoda/azuri/data/galaxia/xy_ubv_Vlt21_5/";
}

string obsGetDataDirOut(string const& whichOne){
    if (whichOne.compare("gaia") == 0)
        return gaiaGetDataDirOut();
    else if (whichOne.compare("gaiaTgas") == 0)
        return gaiaTgasGetDataDirOut();
    else
        throw std::runtime_error("obsGetDataDirOut: ERROR: whichOne = <"+whichOne+"> not recognized");
}

string gaiaGetDataDirOut(){
    return "/Volumes/external/azuri/data/gaia/xy/";
}

string gaiaTgasGetDataDirOut(){
    return "/Volumes/yoda/azuri/data/gaia-tgas/xy/";
}

string obsGetFilter(){
    return "g";
}

string modelGetFilters(){
    string photometricSystem = getPhotometricSystem();
    if (photometricSystem.compare("UBV") == 0)
        return("B,V,I,log_g");
    else if (photometricSystem.compare("SDSS") == 0)
        return("g,r,i");
    else
        throw std::runtime_error("modelGetFilters: ERROR: photometric system <"+photometricSystem+">");
}

string obsGetFilterKeyWord(string const& filter){
    if (filter.compare("g") == 0)
        return "phot_g_mean_mag";
    else
        throw std::runtime_error("obsGetFilterKeyWord: ERROR: unknown filter <"+filter+">");
}

string modelGetFilterKeyWord(string const& filter){
    if (filter.compare("g") == 0)
        return "sdss_g_app";
    else if (filter.compare("r") == 0)
        return "sdss_r_app";
    else if (filter.compare("i") == 0)
        return "sdss_i_app";
    else if (filter.compare("I") == 0)
        return "ubv_i_app";
    else if (filter.compare("U") == 0)
        return "ubv_u_app";
    else if (filter.compare("B") == 0)
        return "ubv_b_app";
    else if (filter.compare("V") == 0)
        return "ubv_v_app";
    else if (filter.compare("J") == 0)
        return "ubv_j_app";
    else if (filter.compare("H") == 0)
        return "ubv_h_app";
    else if (filter.compare("K") == 0)
        return "ubv_k_app";
    else if (filter.compare("R") == 0)
        return "ubv_r_app";
    else if (filter.compare("log_g") == 0)
        return modelGetHeaderKeyWord("log_g");
    else
        throw std::runtime_error("modelGetFilterKeyWord: ERROR: unknown filter <"+filter+">");
}

string modelGetHeaderKeyWord(string const& keyWord){
    if (keyWord.compare("distance"))///[kpc]
        return "rad";
    else if (keyWord.compare("log_Teff"))
        return "teff";
    else if (keyWord.compare("mu_b"))
        return "mub";
    else if (keyWord.compare("mu_l"))
        return "mul";
    else if (keyWord.compare("FeH"))
        return "feh";
    else if (keyWord.compare("v_rad"))
        return "vrad";
    else if (keyWord.compare("log_g"))
        return "grav";
/*    else if (keyWord.compare(""))
        return "";
    else if (keyWord.compare(""))
        return "";
    else if (keyWord.compare(""))
        return "";
    else if (keyWord.compare(""))
        return "";*/
    else
        throw std::runtime_error("modelGetHeaderKeyWord: ERROR: unknow keyWord <"+keyWord+">");
}

string obsGetHeaderKeyWord(string const& keyWord){
    if (keyWord.compare("mu_ra"))
        return "pmra";
    else if (keyWord.compare("error_mu_ra"))
        return "pmra_error";
    else if (keyWord.compare("mu_dec"))
        return "pmdec";
    else if (keyWord.compare("error_mu_dec"))
        return "pmdec_error";
    else if (keyWord.compare("parallax"))
        return "parallax";
    else if (keyWord.compare("error_parallax"))
        return "parallax_error";
/*    else if (keyWord.compare(""))
        return "";
    else if (keyWord.compare(""))
        return "";
    else if (keyWord.compare(""))
        return "";*/
    else
        throw std::runtime_error("obsGetHeaderKeyWord: ERROR: unknown keyWord <"+keyWord+">");
}

unsigned getNStepsMagnitude(){
    return 10;
}

unsigned getNSims(){
    return 2;
}

string getPhotometricSystem(){
    return "UBV";//"SDSS"
}
