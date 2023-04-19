#!/usr/bin/python3

import os
import json
import h3.api.numpy_int as h3
from osgeo import gdal
from multiprocessing import Pool, cpu_count

# Set the H3 resolution and the pixel size in meters
H3_RESOLUTION = 9
PIXEL_SIZE = 100

# Define the path to the source folder
SOURCE_FOLDER = "sources"

# Create the classified folder if it doesn't exist
CLASSIFIED_FOLDER = "classified"
if not os.path.exists(CLASSIFIED_FOLDER):
    os.makedirs(CLASSIFIED_FOLDER)

def process_image(filename):
    # Skip any files that aren't geotiffs
    if not filename.endswith(".tif"):
        return
    
    # Open the geotiff file
    filepath = os.path.join(SOURCE_FOLDER, filename)
    dataset = gdal.Open(filepath)
    
    # Get the pixel values and the geotransform information
    band = dataset.GetRasterBand(1)
    nodata = band.GetNoDataValue()
    geotransform = dataset.GetGeoTransform()
    pixel_values = band.ReadAsArray().astype(float)
    
    # Create an empty dictionary to store the H3 cell areas
    h3_cells = {}
    
    # Loop through each pixel and calculate the covered area
    for i in range(pixel_values.shape[0]):
        for j in range(pixel_values.shape[1]):
            # Skip nodata pixels
            if pixel_values[i][j] == nodata:
                continue
            
            # Calculate the covered area of the pixel
            pixel_area = (PIXEL_SIZE ** 2) * (pixel_values[i][j] / 100)
            
            # Convert the pixel coordinates to map coordinates
            x = geotransform[0] + (j + 0.5) * geotransform[1] + (i + 0.5) * geotransform[2]
            y = geotransform[3] + (j + 0.5) * geotransform[4] + (i + 0.5) * geotransform[5]
            
            # Get the H3 cell at the current coordinates
            h3_cell = h3.geo_to_h3(y, x, H3_RESOLUTION)
            
            # Add the covered area to the H3 cell
            if h3_cell in h3_cells:
                h3_cells[h3_cell] += pixel_area
            else:
                h3_cells[h3_cell] = pixel_area
                
            # Print the progress
            pixels_processed = (i * pixel_values.shape[1]) + j + 1
            total_pixels = pixel_values.shape[0] * pixel_values.shape[1]
            if pixels_processed % 10000 == 0:
                progress = pixels_processed / total_pixels
                print(f"{filename}: {progress:.2%} complete", end="\r")
    
    # Save the H3 cell areas to a json file
    output_filename = os.path.join(CLASSIFIED_FOLDER, f"{os.path.splitext(filename)[0]}.json")
    with open(output_filename, "w") as output_file:
        json.dump(h3_cells, output_file)
        
    # Close the geotiff dataset
    dataset = None

if __name__ == '__main__':
    # Get the list of filenames in the source folder
    filenames = os.listdir(SOURCE_FOLDER)

    pool = Pool(processes=cpu_count())

    # Process each image in parallel
    pool.map(process_image, filenames)

    # Close the pool
    pool.close()
    pool.join()
