#include "parameters.h"

boost::format galaxiaGetFileNameOutRoot(){
    return boost::format("galaxia_%06f-%06f_%06f-%06f.csv");// % (float(minX), float(maxX), float(minY), float(maxY))
}

boost::format gaiaGetFileNameOutRoot(){
    return boost::format("GaiaSource_%06f-%06f_%06f-%06f.csv");// % (float(minX), float(maxX), float(minY), float(maxY))
}

boost::format gaiaTgasGetFileNameOutRoot(){
    return boost::format("TgasSource_%06f-%06f_%06f-%06f.csv");// % (float(minX), float(maxX), float(minY), float(maxY))
}

string galaxiaGetDataDirOut(){
    return "/Volumes/yoda/azuri/data/galaxia/xy/";
//    return "/Volumes/yoda/azuri/data/galaxia/xy1/";
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
string gaiaGetFilterKeyWord(string const& filter){
    if (filter.compare("g") == 0)
        return "phot_g_mean_mag";
    else
        throw std::runtime_error("gaiaGetFilterKeyWord: ERROR: unknown filter <"+filter+">");
}

string galaxiaGetFilterKeyWord(string const& filter){
    if (filter.compare("g") == 0)
        return "sdss_g";
    else
        throw std::runtime_error("galaxiaGetFilterKeyWord: ERROR: unknown filter <"+filter+">");
}

string galaxiaGetHeaderKeyWord(string const& keyWord){
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
/*    else if (keyWord.compare(""))
        return "";
    else if (keyWord.compare(""))
        return "";
    else if (keyWord.compare(""))
        return "";
    else if (keyWord.compare(""))
        return "";
    else if (keyWord.compare(""))
        return "";*/
    else
        throw std::runtime_error("galaxiaGetHeaderKeyWord: ERROR: unknow keyWord <"+keyWord+">");
}

string gaiaGetHeaderKeyWord(string const& keyWord){
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
        throw std::runtime_error("gaiaGetHeaderKeyWord: ERROR: unknown keyWord <"+keyWord+">");
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
