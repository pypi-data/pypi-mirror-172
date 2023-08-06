---
file_format: mystnb
kernelspec:
  name: python3
---

(1d_example_notebook)=
# Using the one dimensional model version

This notebook describes how to use the one dimensional version of the SWE2HS 
model. You can transfer a {py:class}`pandas.Series`
which contains daily snow water equivalent of the snowpack (SWE) to a 
{py:class}`pandas.Series`
of daily snow depth (HS). The series must have a {py:class}`pandas.DatetimeIndex`
as index. Additionally, the layer state varibales can be returned as 
{py:class}`xarray.Dataset` and can be plotted with functions from
the {py:mod}`swe2hs.visualization` module.

First import libraries we need for reading data and plotting...

```{code-cell}
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
```

... and import the SWE2HS package

```{code-cell}
import swe2hs as jopack
```

Let us create some dummy SWE data. For this we create a function which defines an artificial SWE evolution for a single winter an inject it at the first of December repeatedly for a given number of years (`n_years`). 

```{code-cell}
def create_swe(n_years):
    dates = pd.date_range(start='2000-09-01', end=f'{2000+n_years}-08-31', freq='D')
    swe = np.zeros(len(dates))
    swe_winter = np.array([0.01]*10 + [0.02]*5 + [0.1]*10 + [0.15]*10 + np.linspace(
        0.15, 0.1, 10).tolist() + [0.25]*20 + [0.35]*15 + np.linspace(0.35, 0., 50).tolist())
    first_decembers = np.nonzero(dates.strftime('%m-%d') == '12-01')[0]
    for f in first_decembers:
        swe[f:f+len(swe_winter)] = swe_winter
    return pd.Series(swe, index=dates, name='SWE [m]')
```
## Convert one dimensional series
For the first example, we create data of three years.

```{code-cell}
swe = create_swe(n_years=3)
swe.plot(ylabel='SWE [m]')
plt.show()
```

The SWE series can be converted to a HS series with the 
{py:func}`~swe2hs.one_dimensional.convert_1d` function:

```{code-cell}
hs = jopack.convert_1d(swe, swe_input_unit='m', hs_output_unit='m')
hs
```

We can then for example plot the calculated snow depth alongside the input SWE data:

```{code-cell}
fig, ax = plt.subplots()
swe.plot(label='input SWE')
hs.plot(label='calculated HS')
ax.legend()
ax.set_ylabel('HS or SWE [m]')
plt.show()
```

Please see the documentation of {py:func}`~swe2hs.one_dimensional.convert_1d` 
for all available options
regarding filling of small gaps and ignoring date inconsitencies in between zeros.

(layer_plot_example)=
## Plotting layer evolution

This section shows how to display the layer evolution within the modelled 
snowpack. For this we create two years of SWE data:

```{code-cell}
swe_two_years = create_swe(n_years=2)
```

When the {py:func}`~swe2hs.one_dimensional.convert_1d` 
function is called with `return_layers=True`, it will 
return an {py:class}`xarray.Dataset` 
where the layer state variables height, density, and maximum 
density are stored alongside the snow depth.

```{code-cell}
hs_with_layers = jopack.convert_1d(swe_two_years, return_layers=True)
hs_with_layers
```

The modeled layer evolution can then be plotted with the 
{py:func}`~swe2hs.visualization.layer_plot` 
function from the visualization module. Setting the parameter 
`color_variable` to `None` will only draw the layer borders.

```{code-cell}
fig, ax = plt.subplots()
jopack.visualization.layer_plot(
    ax, 
    hs_with_layers, 
    color_variable=None,
)
plt.show()
```

(groupby_hydroyear_example)=
## Plotting layers for each year individually
Often it is useful to plot each hydrological year independently. This can be 
done with the utility function {py:func}`~swe2hs.visualization.groupby_hydroyear`
from the {py:mod}`swe2hs.visualization` module. 
We additionally choose that the layers are colored corresponding to the layer 
density.

```{code-cell}
grouped_hydro_years = jopack.visualization.groupby_hydroyear(
    hs_with_layers,
    split=9,
)

for year, yearly_data in grouped_hydro_years:
    fig, ax = plt.subplots()
    jopack.visualization.layer_plot(
        ax, 
        yearly_data,
        color_variable='layer_densities',
        cbar_label='Density [kg m$^{-3}$]'
    )
    ax.set_ylabel('HS [m]')
    ax.set_title(f'Hydrological year: {year}')
    plt.show()
```