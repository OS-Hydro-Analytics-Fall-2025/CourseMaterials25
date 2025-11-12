import numpy as np
import pandas as pd
import xarray as xr
import sys
import os

num_args = len(sys.argv)
if num_args < 4:
    print("Too few arguments!")
    print("The total number of arguments is %s"%(num_args-1))
    print("python 1_prep_met_forcing.from_era5.py <site_id> <input_dir>")
    print("                                       <output_dir>")
    sys.exit()

# site id
site_id    = sys.argv[1] # "01205500"
input_dir  = sys.argv[2] # inpur directory
odir       = sys.argv[3] # output directory
# transfer start_year and end_year to integer
start_year = 2011
end_year   = 2024

# read in data
fname = f"ERA5.{site_id}.regrid.2011_2024.nc"
met_ay_ds = xr.open_dataset(os.path.join(input_dir,fname))

# meteorological forcing data
for year in range(start_year,end_year+1):
    print("Start processing Year %s"%year)
    fname = os.path.join(input_dir,"ERA5.%s.%s.nc"%(site_id,year))
    # met_ds = xr.open_dataset(fname)
    met_ds = met_ay_ds.sel(time=slice(f"{year}-01-01",f"{year}-12-31"))
    # calculate the variables
    # 1. calculate wind speed from U and V
    WIND = np.sqrt(met_ds.VAR_10U**2 + met_ds.VAR_10V**2)
    # 2. calculate vapor pressure
    VAR_2D_C = met_ds.VAR_2D - 273.15
    VP = 6.11 * 10 **((7.5 * VAR_2D_C)/(237.3 + VAR_2D_C))
    # convert the units
    # 1. surface pressure (Pa to KPa)
    SP_kPa = met_ds.SP/1000
    # 2. air temperature (K to C)
    VAR_2T_C = met_ds.VAR_2T - 273.15
    # 3. precipitation
    MTPR_mm = met_ds.MTPR * 3600
    # 4. vapor pressure (hPa to kPa)
    VP_kPa = VP * 0.1

    # add the units to the bars
    SP_kPa.attrs['units'] = 'kPa'
    VAR_2T_C.attrs['units'] = 'deg C'
    MTPR_mm.attrs['units'] = 'mm/timestep'
    VP_kPa.attrs['units'] = 'kPa'
    WIND.attrs['units'] = 'm s**-1'
    ds_met_data = xr.Dataset({'SP':SP_kPa,
                              'VAR_2T':VAR_2T_C,
                              'MTPR':MTPR_mm,
                              'VP':VP_kPa,
                              'WIND':WIND,
                              'MSDWLWRF':met_ds.MSDWLWRF,
                              'MSDWSWRF':met_ds.MSDWSWRF})

    #
    ofile = os.path.join(odir,"ERA5.%s.regrid.%s.nc"%(site_id,year))
    ds_met_data.to_netcdf(ofile)

