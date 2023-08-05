# Readme

[![PyPI](https://img.shields.io/pypi/v/gdptools.svg)](https://pypi.org/project/gdptools/)
[![conda](https://anaconda.org/conda-forge/gdptools/badges/version.svg)](https://anaconda.org/conda-forge/gdptools)
[![Latest Release](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/-/badges/release.svg)](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/-/releases)

[![Status](https://img.shields.io/pypi/status/gdptools.svg)](https://pypi.org/project/gdptools/)
[![Python Version](https://img.shields.io/pypi/pyversions/gdptools)](https://pypi.org/project/gdptools)

[![License](https://img.shields.io/pypi/l/gdptools)](https://creativecommons.org/publicdomain/zero/1.0/legalcode)

[![Read the documentation at https://gdptools.readthedocs.io/](https://img.shields.io/readthedocs/gdptools/latest.svg?label=Read%20the%20Docs)](https://gdptools.readthedocs.io/)
[![pipeline status](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/badges/main/pipeline.svg)](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/-/commits/main)
[![coverage report](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/badges/main/coverage.svg)](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/-/commits/main)

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://code.usgs.gov/pre-commit/pre-commit)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://code.usgs.gov/psf/black)
[![Poetry](https://img.shields.io/badge/poetry-enabled-blue)](https://python-poetry.org/)
[![Conda](https://img.shields.io/badge/conda-enabled-green)](https://anaconda.org/)

## Welcome

Welcome to gdptools, a python package for grid- or polyon-to-polygon area-weighted interpolation statistics.

![Welcome figure](./docs/assets/Welcom_fig.png)

<figcaption>Example grid-to-polygon interpolation.  A) Huc12 basins for Delaware River Watershed. B) Gridded monthly water evaporation amount (mm) from TerraClimate dataset. C) Area-weighted-average interpolation of gridded TerraClimate data to Huc12 polygons.</figcaption>

## Documentation

[gdptools documentation](https://gdptools.readthedocs.io/en/latest/)

## Features

- Grid-to-polygon interpolation of area-weighted statistics.
- Use [Mike Johnson's OPeNDAP catalog][1] to access over 1700 unique datasets.
- Use any gridded dataset that can be read by xarray.
- Uses spatial index methods for improving the efficiency of areal-wieght calculation detailed by [Geoff Boeing][2]

[1]: https://mikejohnson51.github.io/opendap.catalog/articles/catalog.html
[2]: https://geoffboeing.com/2016/10/r-tree-spatial-index-python/

## Requirements

### Data - xarray (gridded data) and Geopandas (Polygon data)

- Xarray

  - Any endpoint that can be read by Xarray and contains projected coordinates.
  - Projection: any projection that can be read by proj.CRS (similar to Geopandas)

- Geopandas
  - Any file that can be read by Geopandas
  - Projection: any projection that can be read by proj.CRS

## Installation

You can install _Gdptools_ via [pip](https://pip.pypa.io/) from [PyPI](https://pypi.org/):

        pip install gdptools

or install via [conda](https://anaconda.org/) from [conda-forge](https://anaconda.org/conda-forge/gdptools):

       conda install -c conda-forge gdptools

## Usage

Please see the example notebook for detailed examples.

- [OPeNDAP Catalog Example](./docs/terraclime_et.ipynb)
- [Non-catalog example](./docs/Gridmet_non_catalog.ipynb)

## Contributing

Contributions are very welcome. To learn more, see the Contributor Guide\_.

## License

Distributed under the terms of the [CC0 1.0 Universal license](https://creativecommons.org/publicdomain/zero/1.0/legalcode), _Gdptools_ is free and open source software.

## Issues

If you encounter any problems, please [file an issue](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/issues) along with a detailed description.

## Credits

This project was generated from [@hillc-usgs](https://code.usgs.gov/hillc-usgs)'s [Pygeoapi Plugin Cookiecutter](https://code.usgs.gov/wma/nhgf/pygeoapi-plugin-cookiecutter) template.
