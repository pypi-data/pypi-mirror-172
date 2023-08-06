---
file_format: mystnb
kernelspec:
  name: python3
---

(2d_example_notebook)=
# Using the two dimensional model version

This notebook describes how to use the two dimensional version of the SWE2HS 
model. The two dimensional model version can be used to run the model in a 
distributed version on e.g. data from a netCDF file with dimensions in latitude, 
longitude and time. The data should be read with [xarray](https://xarray.dev/)
and the function {py:func}`~swe2hs.two_dimensional.convert_2d` accepts the data as 
{py:class}`xarray.DataArray`.

In the two dimensional version, each pixel is treated independently and 
no communication is done in between pixels. Therefore, calculations can be 
easily parallelized using [Dask](https://www.dask.org/). 

First import libraries we need for reading data and plotting...

```{code-cell}
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cbook
import xarray as xr
%matplotlib inline
```

... and import the SWE2HS package

```{code-cell}
import swe2hs as jopack
```

We again create some sample toy data as in the 
[one dimensional example notebook](1d_example_notebook). 
This time, we create an {py:class}`xarray.DataArray` instead 
of a {py:class}`pandas.Series`. The dataarray has the dimensions
`(time, lon, lat)`. In order to look a bit more realistic, we shift
the SWE sample evolution with help of a digital elevation model from
{py:func}`matplotlib.cbook.get_sample_data`.

```{code-cell}
def create_swe(n_years, n_lon, n_lat):
    assert n_lon <= 344, 'DEM has shape (344, 403)'
    assert n_lon <= 403, 'DEM has shape (344, 403)'
    dates = pd.date_range(start='2000-09-01', end=f'{2000+n_years}-08-31', freq='D')
    # create a sample swe evolution 
    swe_winter = np.array([0.02]*5 + np.linspace(0.02, 0, 5).tolist() +\
        [0]*10 + [0.01]*10 + [0.02]*5 + [0.1]*10 + [0.15]*10 +\
        np.linspace(0.15, 0.1, 10).tolist() + [0.25]*20 +\
        [0.35]*15 + np.linspace(0.35, 0., 50).tolist())*1000
    first_decembers = np.nonzero(dates.strftime('%m-%d') == '12-01')[0]
    swe_1d = np.zeros(len(dates))
    for f in first_decembers:
        swe_1d[f:f+len(swe_winter)] = swe_winter

    lon = list(range(n_lon))
    lat = list(range(n_lat))

    swe_2d = np.tile(swe_1d, (n_lon, n_lat, 1))

    # get sample DEM data from matplotlib cbook and scale the 
    # SWE sample data according to the elevation from the DEM 
    dem = cbook.get_sample_data('jacksboro_fault_dem.npz', np_load=True)
    z = dem['elevation'][:n_lon, :n_lat]
    z_scale = (z - np.mean(z)) / np.std(z)
    swe_2d_scaled = (swe_2d 
        + (z_scale * np.max(swe_winter)*0.5).reshape(n_lon, n_lat, 1)) 
    # enforce zeros at same position as in swe_2d.
    swe_2d_scaled = np.where(swe_2d==0, 0, swe_2d_scaled)
    # enforce no negative SWE values
    swe_2d_scaled = np.clip(swe_2d_scaled, 0, None)  
    return xr.DataArray(
        data=swe_2d_scaled,
        coords={
            'lon': lon,
            'lat': lat,
            'time': dates.to_numpy()
        },
        name='SWE',
        attrs={'unit': 'mm'},
    )
```

(convert_2d_gridded_example)=
## Convert two dimensional gridded data
For this example we create three years of data in a 40x30 gridded domain. 

```{code-cell}
swe = create_swe(n_years=3, n_lon=40, n_lat=30)
swe
```

We plot the pixel `lon=20` and `lat=15` of the created sample SWE data:

```{code-cell}
swe.sel(lon=20, lat=15).plot()
plt.show()
```

And plot the whole SWE map at the first of February:

```{code-cell}
swe.sel(time='2001-02-01').plot()
plt.show()
```

With the {py:func}`~swe2hs.two_dimensional.convert_2d` function, we can convert 
the SWE data to HS. 

```{code-cell}
hs = jopack.convert_2d(
    swe, 
    swe_input_unit='mm', 
    hs_output_unit='cm'
)
hs
```

We plot the calculated HS data for the pixel `lon=20` and `lat=15` alongside the 
input SWE data from the same pixel

```{code-cell}
fig, ax = plt.subplots()
swe.isel(lon=20, lat=15).plot(ax=ax, label='input SWE')
hs.isel(lon=20, lat=15).plot(ax=ax,label='calculated HS')
ax.legend(loc='upper right')
ax.set_ylabel('HS [cm] or SWE [mm]')
plt.show()
```

And again plot the resulting map of HS from the first of February:

```{code-cell}
hs.sel(time='2001-02-01').plot()
plt.show()
```

(convert_2d_data_from_files)=
## Convert data from large netCDF files

Often gridded data is stored in [netCDF](https://www.unidata.ucar.edu/software/netcdf/) 
files. If the SWE data file is too large to fit into memory of your machine, 
you can read, write and process chunks of the file in parallel
with {py:mod}`xarray`, {py:mod}`dask` and the {py:func}`~swe2hs.two_dimensional.convert_2d` function.

Again, we create sample data and this time save it as netCDF file on disk.

```{code-cell}
swe = create_swe(n_years=2, n_lon=100, n_lat=120)
swe.to_netcdf(
    'swe_sample_data.nc',
    format='NETCDF4',
    engine='netcdf4',
)
```

If you load the data from disk with {py:func}`xarray.open_dataarray` and supply
the `chunks` argument, the data is loaded lazily as Dask array. Please see
{ref}`this notebook <xarray:dask>` for more information on xarray and Dask.
The {py:func}`~swe2hs.two_dimensional.convert_2d` function does not allow
chunking in the time dimension, therefore we do not assign any chunking to
the `time` dimension in the chunks dictionary passed to
{py:func}`~xarray.open_dataarray`.

```{note}
When working with Dask arrays, 
[choose appropriate chunk sizes](https://blog.dask.org/2021/11/02/choosing-dask-chunk-sizes) 
in your x (`lon`) and y (`lat`) dimensions in order to be efficient. 

On a desktop PC with 8 cores (Intel Core i7-4790 CPU @ 3.60 GHz, 24 GB RAM),
the following chunk size was most efficient for processing 23 years of the 
Swiss 1 x 1 km domain of shape `(8401, 365, 272)`: `chunks = {'lon': 35, 'lat': 35}`.

If you process less years, increase the chunk size, if you process 
more years, reduce the chunk size but do not create too small chunks. 
Staying above a chunk size of 10 in `lon`and `lat` may be a good rough guide. 
```

```{code-cell}
swe_from_disk = xr.open_dataarray(
    'swe_sample_data.nc', 
    chunks={
        'lon': 20,
        'lat': 20,
        },
    engine='netcdf4'
    )
swe_from_disk
```

Then we can run the SWE2HS model in parallel. Note that no calculations are
performed before the data is actually needed. We can see this by the elapsed time
of the convert_2d call: 

```{code-cell}
t0 = datetime.now()
hs_out = jopack.convert_2d(
    swe_from_disk,
    swe_input_unit='mm', 
    hs_output_unit='cm',
)
t1 = datetime.now()
print(f"Elapsed time for convert_2d call: {(t1-t0).total_seconds()} s")
hs_out
```

Calculations are in this example case triggered when we store the data to disk.

```{code-cell}
t0 = datetime.now()
hs_out.to_netcdf(
    'calculated_hs.nc',
    format='NETCDF4',
    engine='netcdf4',
)
t1 = datetime.now()
print(f"Elapsed time for calculation and storing to disk: {(t1-t0).total_seconds()} s")
```
