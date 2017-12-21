#include "galaxia.h"

double getAEbfFactor(string const& band){
    if (band.compare("sdss_u") == 0)
        return 5.155;
    else if (band.compare("sdss_g") == 0)
        return 3.793;
    else if (band.compare("sdss_r") == 0)
        return 2.751;
    else if (band.compare("sdss_i") == 0)
        return 2.086;
    else if (band.compare("sdss_z") == 0)
        return 1.479;
    else
        throw std::out_of_range("getAEbfFactor: unknown band <" + band + ">");
}

vector< vector< double > > vxyz2lbr(vector<double> const& px,
                                    vector<double> const& py,
                                    vector<double> const& pz,
                                    vector<double> const& vx,
                                    vector<double> const& vy,
                                    vector<double> const& vz){
    int size=px.size();
    vector<double> r(size);
    for (auto itR=r.begin(),
              itPx=px.begin(),
              itPy=py.begin(),
              itPz=pz.begin(),
              itVx=vx.begin(),
              itVy=vy.begin(),
              itVz=vz.begin();
         itR!=r.end();
         ++itR,
         ++itPx,
         ++itPy,
         ++itPz,
         ++itVx,
         ++itVy,
         ++itVz){
        *itR=sqrt(((*itPx)*(*itPx))+((*itPy)*(*itPy))+((*itPz)*(*itPz)));
        if (*itR == 0.0)
            *itR=1.0;
    }

    vector<double> pxTemp(size);
    vector<double> pyTemp(size);
    vector<double> pzTemp(size);
    for (auto itR=r.begin(),
              itPx=px.begin(),
              itPy=py.begin(),
              itPz=pz.begin(),
              itPxTemp=pxTemp.begin(),
              itPyTemp=pyTemp.begin(),
              itPzTemp=pzTemp.begin();
         itR!=r.end();
         ++itR,
         ++itPx,
         ++itPy,
         ++itPz,
         ++itPxTemp,
         ++itPyTemp,
         ++itPzTemp){
        *itPxTemp=(*itPx)/(*itR);
        *itPyTemp=(*itPy)/(*itR);
        *itPzTemp=(*itPz)/(*itR);
    }

    vector<double> rc(size);
    for (auto itRc=rc.begin(),
              itPx=px.begin(),
              itPy=py.begin();
         itRc!=rc.end();
         ++itRc,
         ++itPx,
         ++itPy){
        *itRc=sqrt(((*itPx)*(*itPx))+((*itPy)*(*itPy)));
        if (*itRc == 0.0)
            *itRc = 1.0;
    }

    vector<double> tm_00(size);
    vector<double> tm_01(size);
    vector<double> tm_02(size);
    vector<double> tm_10(size);
    vector<double> tm_11(size);
    vector<double> tm_12(size);
    vector<double> tm_20(size);
    vector<double> tm_21(size);
    vector<double> tm_22(size);
    for (auto itTm_00=tm_00.begin(),
              itTm_01=tm_01.begin(),
              itTm_02=tm_02.begin(),
              itTm_10=tm_10.begin(),
              itTm_11=tm_11.begin(),
              itTm_12=tm_12.begin(),
              itTm_20=tm_20.begin(),
              itTm_21=tm_21.begin(),
              itTm_22=tm_22.begin(),
              itRc=rc.begin(),
              itPx=px.begin(),
              itPy=py.begin(),
              itPz=pz.begin();
         itTm_00!=tm_00.end();
         ++itTm_00,
         ++itTm_01,
         ++itTm_02,
         ++itTm_10,
         ++itTm_11,
         ++itTm_12,
         ++itTm_20,
         ++itTm_21,
         ++itTm_22,
         ++itRc,
         ++itPx,
         ++itPy,
         ++itPz){
        *itTm_00=-(*itPy)/(*itRc);
        *itTm_01=-(*itPz)*(*itPx)/(*itRc);
        *itTm_02= (*itRc)*(*itPx)/(*itRc);
        *itTm_10= (*itPx)/(*itRc);
        *itTm_11=-(*itPz)*(*itPy)/(*itRc);
        *itTm_12= (*itRc)*(*itPy)/(*itRc);
        *itTm_20= 0.0;
        *itTm_21= *itRc;
        *itTm_22= *itPz;
    }

    vl=(vx*tm_00+vy*tm_10+vz*tm_20)
    vb=(vx*tm_01+vy*tm_11+vz*tm_21)
    vr=(vx*tm_02+vy*tm_12+vz*tm_22)
    return vl,vb,vr
}

void appendPM(CSVData & data){
    [vl,vb,vr]=_vxyz2lbr(data['px'],data['py'],data['pz'],data['vx'],data['vy'],data['vz'])
    r=np.sqrt(data['px']*data['px']+data['py']*data['py']+data['pz']*data['pz'])
#    data['pm']=np.sqrt(vl*vl+vb*vb)/(4.74e3*r)
    data['vr']=vr
    data['mul']=vl/(4.74e3*r)
    data['mub']=vb/(4.74e3*r)

/*

def abs2app(data,noext=False,dered=False,corr=False):
    """
    Apply extinction and computes the apparent magntiude.
    All magnitude related keys in data are modified.
    It is advisabe to run it with option corr=True to enable
    low latitude correction to Schlegel maps.
    Args:
        data: galaxia data
    """
    dmod=5.0*np.log10(100.0*data['rad'])
    if dered:
        ebv=data['exbv_schlegel']-data['exbv_schlegel_inf']
    else:
        ebv=data['exbv_schlegel']*1.0
    if corr:
        ebv=ebv*_extcorr(data['exbv_schlegel_inf'])

    aebv=_aebv_factor()
    j=0L
    for temp in data.keys():
        temp1=temp.lower()
        if temp1 in aebv:
            print temp
            if noext==1:
                data[temp]=data[temp]+dmod
            else:
                data[temp]=data[temp]+dmod+aebv[temp1]*ebv
            j+=1

    if  j == 0:
        raise RuntimeError('No quantity to add extinction')

def _extcorr(ebv):
    return (1-np.tanh((ebv-0.15)/0.075))*0.5*(1-0.6)+0.6


def _vlbr2xyz(l,b,r,vl,vb,vr):
    l=np.radians(l)
    b=np.radians(b)
    tm_00=-np.sin(l) ; tm_01=-np.sin(b)*np.cos(l) ; tm_02= np.cos(b)*np.cos(l)
    tm_10= np.cos(l) ; tm_11=-np.sin(b)*np.sin(l) ; tm_12= np.cos(b)*np.sin(l)
    tm_20= 0.0       ; tm_21= np.cos(b)           ; tm_22= np.sin(b)
    vx=vl*tm_00+vb*tm_01+vr*tm_02
    vy=vl*tm_10+vb*tm_11+vr*tm_12
    vz=vl*tm_20+vb*tm_21+vr*tm_22
    # px=r*np.cos(b)*np.cos(l)
    # py=r*np.cos(b)*np.sin(l)
    # pz=r*np.sin(b)
    return vx,vy,vz

def xyz2lbr(x,y,z):
    rc2=x*x+y*y
    return [np.degrees(np.arctan2(y,x)),np.degrees(np.arctan(z/np.sqrt(rc2))),np.sqrt(rc2+z*z)]
*/