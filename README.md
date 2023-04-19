# h3-landcover
Make low resolution landcover vector tiles from high resolution raster landcover data with h3 downsampling

```
python3 continuous.py
python3 analyze.py
./filter.sh
```

# Design (Promts for ChatGPT)

## Download

Download raster landcover data from https://lcviewer.vito.be/download. The data is split into 20 by 20 degree tiles. Use 2019 version, 100 m resolution.

Attribution landcover data: https://lcviewer.vito.be/about

The download URLs look like:

```
https://s3-eu-west-1.amazonaws.com/vito.landcover.global/v3.0.1/2019/E000N60/E000N60_PROBAV_LC100_global_v3.0.1_2019-nrt_Bare-CoverFraction-layer_EPSG-4326.tif
```

template:

```
https://s3-eu-west-1.amazonaws.com/vito.landcover.global/v3.0.1/2019/{longitude}{latitude}/{longitude}{latitude}_PROBAV_LC100_global_v3.0.1_2019-nrt_{kind}-CoverFraction-layer_EPSG-4326.tif
```

latitudes: S40, S20, N00, N20, N40, N60, N80
longitudes: W180, W160, W140, W120, W100, W080, W060, W040, W020, E000, E020, E040, E060, E080, E100, E120, E140, E160
kinds: Snow, Bare, Grass, Crops, Tree, BuiltUp

Download all files into a `sources` folder.

Write a python script which loops through the filenames and downloads them to the `sources` folder with system calls using the cli tool `axel` which has parallel downloads with the `-a -n 10` option.

### ChatGPT Result

[download.py](download.py)

The total landcover raster data is 26 GB in 564 files.

## Raster to H3 Classification

For every image in the `sources` folder: 

* Open the image
* Loop through the pixels
* The pixel value is landcover in percent, the pixel size is 100 m by 100 m
* Call `ReadAsArray` only once per image
* Make sure to ignore nodata pixels
* Print fractional progress after every 10000th pixel
* Multiply pixel area by pixel value divided by 100 to the the covered area of the pixel
* Hold a hash map H3 index to covered area
* Add the area to the H3 cell in the hash map in which the pixel is located, use H3 resolution 9
* Save the hashmap as a json file. Save it at `classified/{original_filename}-resolution-9.json` and create the folder if needed.
* Use the osgeo gdal library
* Use `h3.api.numpy_int` otherwise it is too slow

Write a python script for this.

Second promt: Using the above script, write a version which runs on a 12 core CPU. The images are independent and can be treated in parallel.

[classify.py](classify.py)

## Combine Grass, Bare, Snow

The kinds Grass, Bare, Snow are plotted on top of eachother. In mountains, we first have Grass landcover, then with higher altitude, Bare landcover, and above this we have Snow. To not have any gaps between Snow and Bare landcover, lets combine the following layers:

* Grass-Bare-Snow
* Bare-Snow
* Snow

The Snow layer we have already. Bare-Snow, and Grass-Bare-Snow have to be generated.

The folder `classified` contains files with template filename `{longitude}{latitude}_PROBAV_LC100_global_v3.0.1_2019-nrt_{kind}-CoverFraction-layer_EPSG-4326.tif-resolution-9.json`.

With

latitudes: S40, S20, N00, N20, N40, N60, N80
longitudes: W180, W160, W140, W120, W100, W080, W060, W040, W020, E000, E020, E040, E060, E080, E100, E120, E140, E160

Loop through all latitude, longitude combinations. If the file exists, loop through the kinds [Bare, Snow] and [Grass, Bare, Snow] and sum up the coverages.

Store the resulting H3 map in a file called `classified/{longitude}{latitude}_PROBAV_LC100_global_v3.0.1_2019-nrt_{new_kind}-CoverFraction-layer_EPSG-4326.tif-resolution-9.json` where `new_kind` is `Bare-Snow` or `Grass-Bare-Snow`.

## Downsample

The resolution 9 data in the `classified` folder can be downsampled to lower H3 resolutions including 8, 7, 6, 5, and 4. For this, open every json file in the `classified` folder ending in `*-resolution-9.json`. The file contains a map of H3 cell index to covered area.

* Loop through the `classified/*-resolution-9.json` files
* Load the maps to `data_in`
* For the output_resolutions 8,7,6,5,4 do
  * Create an empty `data_out` map
  * Loop through the `input_resolution` keys
  * Convert the resolution 9 key to the lower resolution key (find parent cell)
  * Add at the value to the output resolution map
  * Save the output reolution json file at `classified/*-resolution-{output_resolution}.json`
