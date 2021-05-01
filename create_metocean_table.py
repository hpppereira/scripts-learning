import numpy as np
import pandas as pd
import xarray as xr

def calculate_gamma(hs, tp):
    """
    Calculate Peak Enhacment Factor
    Input:
    hs - significant wave height time series
    tp - peak period time series
    """

    gam = []
    for i in range(len(hs)):

        # relation between tp and hs
        rel = tp[i]/(np.sqrt(hs[i]))

        if rel <= 3.6:
            gam.append(5.0)
        elif rel > 3.6 and rel < 5.0:
            gam.append(np.exp(5.75 - (1.15 * rel)))
        elif rel >= 5:
            gam.append(1.0)

    return np.array(gam)

def calculate_tz_from_tp(gam, tp):

    a = 0.6673 + (0.05037 * gam) - (0.006230 * gam**2) + (0.0003341 * gam**3)

    tz = a * tp

    return tz

def calculate_vel_dir_from_uv(u, v):

    cvel = (u**2 + v**2)**0.5
    cdir = np.arctan2(u, v) * 180 / np.pi
    cdir[cdir<0] = cdir[cdir<0] + 360

    return cvel, cdir

def create_xls_table(d):

    xls = pd.DataFrame(d)
    xls.set_index('datetime', inplace=True)
    xls.to_excel('tabela_metocean_coppetec.xls')

    return xls
	

if __name__ == '__main__':

    # read mercator
    ds_merc = xr.open_dataset('mercator_coppetec_1999_2018.nc', decode_cf=False)
    df_merc = ds_merc.isel(depth=0).to_dataframe()

    # open era5
    ds = xr.open_dataset('era5_coppetec_1999_2018.nc')

    # converto to dataframe
    df = ds.to_dataframe()

    # create index with datetime
    df['datetime']=df.index

    # create index for mercator with the same date of the er5
    df_merc['datetime'] = df.index
    df_merc.set_index('datetime', inplace=True)

    # calculate gamma for wind sea
    gam_sea = calculate_gamma(hs=df.shww.values, tp=df.mpww.values)

    # calculate gamma for swell
    gam_swl = calculate_gamma(hs=df.shts.values, tp=df.mpts.values)

    # calculate gamma for combined sea and swell
    gam_ss = calculate_gamma(df.swh.values, df.mwp.values)

    # calculate tz for wind sea
    tz_sea = calculate_tz_from_tp(gam=gam_sea, tp=df.mpww.values)

    # calculate tz for wind sea
    tz_swl = calculate_tz_from_tp(gam=gam_swl, tp=df.mpts.values)

    # calculate tz for wind sea
    tz_ss = calculate_tz_from_tp(gam=gam_ss, tp=df.mwp.values)

    # calculate current vel e dir from u and v
    cvel, cdir = calculate_vel_dir_from_uv(df_merc.uo.values, df_merc.vo.values)

    # create dictionary with variables
    d = {
         'datetime': df.index, 
         'hs_sea': df.shww.values,
         'tp_sea': df.mpww.values,
         'tz_sea': tz_sea,
         'gam_sea': gam_sea,
         'dir_sea': df.mdww.values,
         'hs_swl': df.shts.values,
         'tp_swl': df.mpts.values,
         'tz_swl': tz_swl,
         'gam_swl': gam_swl,
         'dir_swl': df.mdts.values,
         'hs_ss': df.swh.values,
         'tp_ss': df.mwp.values,
         'tz_ss': tz_ss,
         'gam_ss': gam_ss,
         'dir_ss': df.mwd.values,
         'wind_vel': df.wind.values,
         'wind_dir': df.dwi.values,
         'curr_vel': cvel,
         'curr_dir': cdir
        }

    # create excel table
    xls = create_xls_table(d)
