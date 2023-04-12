from osgeo import gdal
import numpy as np
import h3.api.numpy_int as h3
import json

def get_coords(filename):
    image = gdal.Open(filename)

    band = image.GetRasterBand(1)
    pixels = band.ReadAsArray().astype(float)

    (y_index, x_index) = np.nonzero(pixels > 50.0)

    (upper_left_x, x_size, x_rotation, upper_left_y, y_rotation, y_size) = image.GetGeoTransform()

    x_coords = x_index * x_size + upper_left_x + (x_size / 2)
    y_coords = y_index * y_size + upper_left_y + (y_size / 2)

    return x_coords, y_coords

filename = 'E000N60_PROBAV_LC100_global_v3.0.1_2019-nrt_Tree-CoverFraction-layer_EPSG-4326.tif'

x_coords, y_coords =  get_coords(filename)


def counts_at_resolution(x_coords, y_coords, resolution):
    counts = {}
    progress = 0
    for x_coord, y_coord in zip(x_coords, y_coords):
        h = h3.geo_to_h3(y_coord, x_coord, resolution)
        counts[h] = counts.get(h, 0) + 1
        progress += 1
        if progress % 1000 == 0:
            print(float(progress)/len(x_coords))
    return counts

resolution = 6

counts = counts_at_resolution(x_coords, y_coords, resolution)

with open('counts.json', 'w') as f:
    json.dump(counts, f)
