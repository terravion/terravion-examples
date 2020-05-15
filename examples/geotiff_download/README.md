Cloud Optimized GeoTIFF Download (2019+) [cog_main.py]
====================

In order to leverage cloud optimized geotiff and use this example code, gdal and rasterio must be downloaded.

https://www.gdal.org/


Installing gdal on mac:
http://www.kyngchaos.com/software/frameworks/

Intalling rasterio:
https://rasterio.readthedocs.io/en/stable/installation.html

**Print account summary**

```
python cog_main.py --access_token <access_token> --get_summary
```

**Preview download multiband**

```
python cog_main.py --access_token <access_token> --get_layers
```

**Download multiband to output_dir**

```
python cog_main.py --access_token <access_token> --get_layers --output_dir <output_dir>
```

**Download a specific product within date range**

```
python cog_main.py --log INFO --access_token <access_token> --get_layers --output_dir <output_dir> --block_id_list [block_id1  block_id2 ...] --start_date <YYYY-MM-DD> --end_date <YYYY-MM-DD> --product NDVI
```

- Add `--dynamic` as an argument to output the NDVI or Thermal products with with ranges scaled (as they are shown in TerrAvion Overview)
- Add `--colormap_name "NDVI_2"` to output the NDVI or Thermal images with a specific colormap. (Example used is the `NDVI_2` colormap.)
- The list of available products and colormap names is shown at the bottom of this page.

Run tests to check out example usage


GeoTIFF Download (Pre-2019) [main.py]
====================

Request api@terravion.com for an access_token

## Example Command Lines:

**Retrieve all the blocks:**

```
python main.py --access_token <access_token> --get_block_list
```

**Retrieve download links by block id:**

```
python main.py --access_token <access_token> --block_id_list <bid1> <bid2> <...> --product MULTIBAND
```

Add `--output_dir <output_dir>` to download actual image

**Retrieve download links by block_name:**

```
python main.py --access_token <access_token> --block_name <block_name> --product MULTIBAND
```

Add `--output_dir <output_dir>` to download actual image

### Product Names

`MULTIBAND` [default]

`SYNTHETIC_NC` (aka. SYNTHETIC_COLOR, SYNTHETIC_RGB)

`NC` (aka. COLOR, RGB)

`NDVI` (aka. VIGOR)

`ZONE` (aka. CANOPY_VIGOR, ZONING)

`CIR` (aka. INFRARED)

`THERMAL` (aka. TIRS)

`PANSHARPEN_THERMAL` (aka. PANSHARPEN_TIRS)

### Commonly Used Colormap Names:

Note: "T" is the default used for Thermal products. Please check your colormaps in Overview to see what colormap name you are currently using for NDVI products.

`"N-GREENG"`

`"N-R2"`

`"N-R3"`

`"T"`

`"N-AVHRR"`

`"JG"`

`"BW"`

`"RW-LEGACY"`

`"GRANULAR"`

`"GM-COMP1"`

`"GM-RGB3"`

`"GM-QUAD"`

`"CVC"`

`"CHS_HC2"`

`"CHS_HC1"`

`"SMWE"`

`"CHS-LEGACY"`

`"TRICOLOR"`

`"TWE"`

`"10 Class Agroprecision Grey"`

`"6 Class Agroprecision"`

`"6 Class Agroprecision Grey"`

`"10 Class Agroprecision"`