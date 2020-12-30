#include "parameters.h"

boost::format modelGetFileNameOutRoot(){
    return boost::format("galaxia_%06f-%06f_%06f-%06f.csv");// % (float(minX), float(maxX), float(minY), float(maxY))
}

boost::format obsGetFileNameOutRoot(string const& whichOne){
    if (whichOne.compare("gaia") == 0)
        return gaiaGetFileNameOutRoot();
    else if (whichOne.compare("gaiaDR2") == 0)
        return gaiaGetFileNameOutRoot();
    else if (whichOne.compare("gaiaTgas") == 0)
        return gaiaTgasGetFileNameOutRoot();
    else if (whichOne.compare("gaiaXSimbad") == 0)
        return gaiaXSimbadGetFileNameOutRoot();
    else if (whichOne.compare("gaiaXSimbadI") == 0)
        return gaiaXSimbadIGetFileNameOutRoot();
    else
        throw std::runtime_error("obsGetFileNameOutRoot: ERROR: whichOne = <"+whichOne+"> not recognized");
}

boost::format gaiaGetFileNameOutRoot(){
    return boost::format("GaiaSource_%06f-%06f_%06f-%06f_xyz.csv");// % (float(minX), float(maxX), float(minY), float(maxY))
}

boost::format gaiaTgasGetFileNameOutRoot(){
    return boost::format("TgasSource_%06f-%06f_%06f-%06f.csv");// % (float(minX), float(maxX), float(minY), float(maxY))
}

boost::format gaiaXSimbadGetFileNameOutRoot(){
    return boost::format("GaiaXSimbad_%06f-%06f_%06f-%06f.csv");// % (float(minX), float(maxX), float(minY), float(maxY))
}

boost::format gaiaXSimbadIGetFileNameOutRoot(){
    return boost::format("GaiaXSimbadI_%06f-%06f_%06f-%06f.csv");// % (float(minX), float(maxX), float(minY), float(maxY))
}

boost::format gaiaXSDSSGetFileNameOutRoot(){
    return boost::format("GaiaXSDSS_%06f-%06f_%06f-%06f.csv");// % (float(minX), float(maxX), float(minY), float(maxY))
}

string modelGetDataDirOut(){
//    return "/Volumes/yoda/azuri/data/galaxia/xy_ubv_Vlt13/";
    return "/Volumes/discovery/azuri/data/galaxia/ubv_Vlt21.5_1.0/xy/";
}

string obsGetDataDirOut(string const& whichOne){
    if (whichOne.compare("gaia") == 0)
        return gaiaGetDataDirOut();
    else if (whichOne.compare("gaiaTgas") == 0)
        return gaiaTgasGetDataDirOut();
    else if (whichOne.compare("gaiaXSimbad") == 0)
        return gaiaXSimbadGetDataDirOut();
    else if (whichOne.compare("gaiaXSimbadI") == 0)
        return gaiaXSimbadIGetDataDirOut();
    else
        throw std::runtime_error("obsGetDataDirOut: ERROR: whichOne = <"+whichOne+"> not recognized");
}

string gaiaGetDataDirOut(){
    return "/Volumes/discovery/azuri/data/gaia/dr2/xy/";
}

string gaiaDR2GetDataDirOut(){
    return "/Volumes/discovery/azuri/data/gaia/dr2/xy/";
}

string gaiaTgasGetDataDirOut(){
    return "/Volumes/discovery/azuri/data/gaia-tgas/xy/";
}

string gaiaXSimbadGetDataDirOut(){
    return "/Volumes/work/azuri/data/gaia/x-match/GaiaDR2xSimbad/xy/";
}

string gaiaXSimbadIGetDataDirOut(){
    return "/Volumes/work/azuri/data/gaia/x-match/simbadI/xy/";
}

string gaiaXSDSSGetDataDirOut(){
    return "/Volumes/work/azuri/data/gaia/x-match/GaiaDR2distXSDSS12/xy/";
}

string obsGetFilter(){
    return "G";
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

string obsGetFilterKeyWord(string const& filter, string const& whichOne){
    if (filter.compare("G") == 0)
        return "phot_g_mean_mag";
    else if (filter.compare("G_BP") == 0)
        return "phot_bp_mean_mag";
    else if (filter.compare("G_RP") == 0)
        return "phot_rp_mean_mag";
    else{
        if (whichOne.compare("gaia")){
            throw std::runtime_error("obsGetFilterKeyWord: ERROR: unknown filter <"+filter+">");
        }
        else if (whichOne.compare("gaiaXSimbad")){
            if (filter.compare("U"))
                return "U";
            else if (filter.compare("B"))
                return "B";
            else if (filter.compare("V"))
                return "V";
            else if (filter.compare("R"))
                return "R";
            else if (filter.compare("I"))
                return "I";
            else if (filter.compare("u"))
                return "u";
            else if (filter.compare("g"))
                return "g";
            else if (filter.compare("r"))
                return "r";
            else if (filter.compare("i"))
                return "i";
            else if (filter.compare("z"))
                return "z";
            else
                throw std::runtime_error("obsGetFilterKeyWord: ERROR: unknown filter <"+filter+">");
        }
        else
            throw std::runtime_error("obsGetFilterKeyWord: ERROR: unknown survey <"+whichOne+">");
    }
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
    else if (filter.compare("G") == 0)
        return string("G");
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
