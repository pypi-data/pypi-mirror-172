# ngff-zarr

[![PyPI - Version](https://img.shields.io/pypi/v/ngff-zarr.svg)](https://pypi.org/project/ngff-zarr)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ngff-zarr.svg)](https://pypi.org/project/ngff-zarr)
[![Test](https://github.com/thewtex/ngff-zarr/actions/workflows/test.yml/badge.svg)](https://github.com/thewtex/ngff-zarr/actions/workflows/test.yml)

-----

A lean and kind Open Microscopy Environment (OME) Next Generation File Format (NGFF) Zarr implementation.

**Table of Contents**

- [Installation](#installation)
- [Features](#features)
- [See also](#see-also)
- [License](#license)

## Installation

```console
pip install 'ngff-zarr[dask-image]'
```

## Features

- Minimal dependencies
- Work with arbitrary Zarr store types
- Lazy, parallel, and web ready -- no local filesystem required
- Process extremely large datasets
- Multiple downscaling methods
- Supports Python>=3.7

## See also

- [ome-zarr-py](https://github.com/ome/ome-zarr-py)
- [multiscale-spatial-image](https://github.com/spatial-image/multiscale-spatial-image)

## License

`ngff-zarr` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
