## Upgrading

To upgrade to the latest version of `up42-blockutils` use `pip`:

```bash
pip install -U up42-blockutils
```

You can determine your currently installed version using this command:

```bash
pip show up42-blockutils
```

## Versions
### [1.0.2](https://pypi.org/project/up42-blockutils/1.0.2/) (2021-04-28)
- Add `tiles_to_geom` method in `blockutils.geometry`

### [1.0.1](https://pypi.org/project/up42-blockutils/1.0.1/) (2021-03-02)
- Add optional `ignore_missing_geometry` flag to `aoi_size_check` in `blockutils.geometry`.

### [1.0.0](https://pypi.org/project/up42-blockutils/1.0.0/) (2021-02-18)
- Upgrade to Stable/Production development status.

### [0.5.4](https://pypi.org/project/up42-blockutils/0.5.4/) (2021-02-03)
- Add `add_files` method to `E2ETest` class.
- Remove z coordinate from geometry of an input query.

### [0.5.3](https://pypi.org/project/up42-blockutils/0.5.3/) (2021-02-03)
- Fix incompatability with python 3.6.
- Ensure suppport for python versions 3.6 to 3.9.

### [0.5.2](https://pypi.org/project/up42-blockutils/0.5.2/) (2021-01-14)
- Add `add_local_files` method to `E2ETest` class.
- Add `interactive_mode` option to `E2ETest` class.
- Add `mercantile` and `requests as requirements for package.
### [0.5.0](https://pypi.org/project/up42-blockutils/0.5.0/) (2020-12-17)
- Add `E2ETest` class in `e2e` module.
### [0.4.2](https://pypi.org/project/up42-blockutils/0.4.2/) (2020-11-09)
- `TileMergeHelper` and `MultiTileMergeHelper` object raises `UP42Error` upon api connection error for unfetched tiles.

### [0.4.1](https://pypi.org/project/up42-blockutils/0.4.1/) (2020-11-09)
- Add `apply_to_cog` parameter to `create_multiband_tif` method in raster module.

### [0.4.0](https://pypi.org/project/up42-blockutils/0.4.0/) (2020-11-09)
- Add `drop_nodata` and `use_colorinterp` parameters to create_multiband_tif method in raster module.

### [0.3.0](https://pypi.org/project/up42-blockutils/0.3.0/) (2020-10-07)
- Add `MultiTileMergeHelper` class in WMTS module for handling tiles for datasets with multiple layers.
- Add `create_multiband_tif` method in raster module for creating a multi-band geotiff.

### [0.2.0](https://pypi.org/project/up42-blockutils/0.2.0/) (2020-10-01)
- Add new WMTS module with `TileMergeHelper` to support tile based data sources.
- Overhaul `STACQuery` object into a data class and add `get_param_if_exists` method.

### [0.1.2](https://pypi.org/project/up42-blockutils/0.1.2/) (2020-09-07)
- Add geometry validity check in Datablock base class.
- Remove AWS and GCS utils & documentation, UP42 now provides "Import Data" and "Export Data" processing blocks on the marketplace.

### [0.0.15](https://pypi.org/project/up42-blockutils/0.0.15/) (2020-07-31)
- Add AWS utilities module.
- Add AWS and GCS utilities documentation.
- Ensure `import blockutils` loads all submodules.

### [0.0.14](https://pypi.org/project/up42-blockutils/0.0.14/) (2020-07-10)
- Update package description to "Block development toolkit for UP42".

### [0.0.13](https://pypi.org/project/up42-blockutils/0.0.13/) (2020-07-06)
- Add `raster.is_empty` and `update_extents` functions.

### [0.0.12](https://pypi.org/project/up42-blockutils/0.0.12/) (2020-06-30)
- Add `gcs_utils` as a new module for handling Google Cloud Storage.

### [0.0.11](https://pypi.org/project/up42-blockutils/0.0.11/) (2020-06-29)
- Add `count_vertices` method in geometry module.

### [0.0.10](https://pypi.org/project/up42-blockutils/0.0.10/) (2020-06-15)
- `STACQuery` object raises `UP42Error` instead of `ValueError` upon wrong inputs.

### [0.0.9](https://pypi.org/project/up42-blockutils/0.0.9/) (2020-06-10)
- Add `check_dtype` and `open_xml_file_with_rasterio` to `DimapFile` class.

### [0.0.8](https://pypi.org/project/up42-blockutils/0.0.8/) (2020-05-22)
- Add `kwargs` to `run` method of base `DataBlock` class.

### [0.0.7](https://pypi.org/project/up42-blockutils/0.0.7/) (2020-05-07)
- Add template repositories to PyPi page.

### [0.0.6](https://pypi.org/project/up42-blockutils/0.0.6/) (2020-05-04)
- Support for python 3.6 to 3.7.
