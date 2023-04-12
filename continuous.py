from osgeo import gdal
import numpy as np
import h3.api.numpy_int as h3
import json


filename = 'E000N60_PROBAV_LC100_global_v3.0.1_2019-nrt_Tree-CoverFraction-layer_EPSG-4326.tif'

image = gdal.Open(filename)

band = image.GetRasterBand(1)
pixels = band.ReadAsArray().astype(float)

(upper_left_x, x_size, x_rotation, upper_left_y, y_rotation, y_size) = image.GetGeoTransform()


resolution = 9

progress = 0
covered_area = {} # h3 cell id -> covered area in km2
for y_index in range(pixels.shape[0]):
    for x_index in range(pixels.shape[1]):
        progress += 1
        if progress % 10000 == 0:
            print(progress / float(pixels.size))

        x_coord = x_index * x_size + upper_left_x + (x_size / 2)
        y_coord = y_index * y_size + upper_left_y + (y_size / 2)

        if pixels[y_index][x_index] != band.GetNoDataValue():
            h = h3.geo_to_h3(y_coord, x_coord, resolution)
            covered_area[h] = covered_area.get(h, 0.0) + 0.1 * 0.1 * pixels[y_index][x_index] / 100 # pixel size is 0.1 km, pixel value is coverage in percent

with open(f'covered_area-{resolution}.json', 'w') as f:
    json.dump(covered_area, f)
