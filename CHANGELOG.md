# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [1.3.0] - 2020-05-06

### Added
- `--colormap_name` and `--colormap_id` flags added to `cog_main.py`. This output any product that supports a colormap from the name or id used as an input.
- All products that support products also support singleband flags in `product_lib.py` since applying a colormap with `write_colormap()` in `rasterio` requires a single band.
- `./examples/geotiff_download/lib/api2/ta_colormap.py`. Used for downloading colormap objects by name or colormap_id.

### Removed
- `./examples/geotiff_download/lib/colormap_sample.py` because it was out of date. The list of given example colormap names was moved to `ta_colormap.py` as the list object `color_map_list`.


## [1.2.0] - 2020-04-29

### Added
- `--dynamic` flag added to `cog_main.py`. This will trigger layer stats to be grabbed from the terravion API and used to generate a dynamic NDVI or THERMAL or PANSHARPEN_THERMAL product.
- `ta_layer_stats.py` module added to grab layer stats from terravion API.


## [1.1.0] - 2020-04-27

### Added
- `product_args` variable in `ProductLib()`. This input is a dictionary of all product arguments needed to replicate a specific product.

### Deprecated
- `contract_bounds` variable in `ProductLib()`. The bounds from this dictionary object have been moved to the keys `nc_lower_bound` and `nc_upper_bound` and `nir_lower_bound` and `nir_upper_bound` inside of the new `product_args` argument detailed above in the Added section. This argument still exists in `ProductLib()` but will be removed in the next major release.

### Fixed
- `output_dir` directory is automatically created upon running `cog_main.py`
- `download_cog_from_s3()` no longer tries to attempt a redownload and error out when file already exists. It now just checks to see if file is there and then moves on.

### Changed
- `ProductLib()` is updated to reflect backend codebase. Band 8 is no longer an alpha channel so those lines of code have been removed in favor of a nodata=0 setting.
- Zoning and Pansharpen Thermal have been added as products


## [1.0.0] - 2019-11-18

### Added
- Starting a changelog with proper versioning practices, as of today the version will begin as 1.0.0

### Changed
- Changed all instances of `working_dir` to `output_dir` for clarity and to synchronize with the backend codebase.