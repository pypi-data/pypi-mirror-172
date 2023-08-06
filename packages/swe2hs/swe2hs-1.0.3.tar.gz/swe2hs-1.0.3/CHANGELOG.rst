=========
Changelog
=========

Version 1.0.3 (2022-10-19)
==========================

Minor patch which fixes typos and broken links in the documentation.

Version 1.0.2 (2022-10-19)
==========================

Breaking changes
----------------

- Changes to the ``sigma_max`` model parameter:
  
  - Changed unit for the ``sigma_max`` model parameter from [m w.e.] 
    to [mm w.e.]. The default value is now 226.9148577394744.
  
  - Renamed from ``max_sigma`` to ``sigma_max`` in order to be consitent
    with the model description paper manuscript.

- New namespaces for two dimensional and stepwise model version:
  
  - ``vectorized`` module -> :mod:`~swe2hs.two_dimensional` module
  - ``operational`` module -> :mod:`~swe2hs.stepwise` module

- New names for the 1d and 2d main functions:

  - ``one_dimensional.swe2hs_1d`` function -> 
    :func:`swe2hs.one_dimensional.convert_1d` function
  - ``vectorized.apply_swe2hs`` function -> 
    :func:`swe2hs.two_dimensional.convert_2d` function

- :func:`~swe2hs.one_dimensional.convert_1d` and
  :func:`~swe2hs.two_dimensional.convert_2d` functions as well 
  as the modules :mod:`~swe2hs.visualization` and 
  :mod:`~swe2hs.utils` are now added to the package namespace.

- The ``core`` module has been made private.

New Features
------------

- input and output units can now be assigned in the
  :func:`~swe2hs.two_dimensional.convert_2d` function.
- the :func:`~swe2hs.two_dimensional.convert_2d` function returns 
  an :class:`xarray.DataArray` with attributes of the data 
  unit, model reference and version of the ``swe2hs`` Python package. 

Other
-----

- Various documentation improvements, e.g. examples for 
  :func:`~swe2hs.two_dimensional.convert_2d`, 
  :func:`~swe2hs.visualization.layer_plot` and 
  :func:`~swe2hs.visualization.groupby_hydroyear`.

Version 0.0.3 (2022-09-13)
==========================

- Initial published version


