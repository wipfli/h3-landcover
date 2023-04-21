#!/usr/bin/python3

import json
import h3.api.numpy_int as h3
import os
from multiprocessing import Pool, cpu_count


GEOJSON_FOLDER = "geojson"
if not os.path.exists(GEOJSON_FOLDER):
    os.makedirs(GEOJSON_FOLDER)

# Define the list of target resolutions to use
target_resolutions = [9, 8, 7, 6, 5, 4]

# for filename in os.listdir("classified"):
def process_file(filename):
    # Read the file contents into a dictionary
    print('reading', filename)
    with open(f"classified/{filename}", "r") as f:
        input_resolution_map = json.load(f)

    # Loop through the target resolutions
    for target_resolution in target_resolutions:
        # print('target_resolution', target_resolution)
        # If the target resolution is 9, use the original input map
        if target_resolution == 9:
            target_resolution_map = input_resolution_map
        else:
            # Create an empty dictionary for the target resolution map
            # print('downsample')
            target_resolution_map = {}

            # Loop through the entries in the input map
            # progress = 0
            for input_index, input_value in input_resolution_map.items():
                # progress += 1
                # if progress % 1000000 == 0:
                #     print(progress / len(input_resolution_map))
                # Find the parent H3 index at the target resolution
                target_index = h3.h3_to_parent(int(input_index), target_resolution)

                # Add the input value to the target resolution map
                target_resolution_map[target_index] = target_resolution_map.get(target_index, 0) + input_value

        # Threshold the target resolution map
        activated = []
        # progress = 0
        # print('thresholding')
        for index, value in target_resolution_map.items():
            # progress += 1
            # if progress % 1000000 == 0:
            #     print(progress / len(target_resolution_map))
            if value / h3.cell_area(int(index), unit='m^2') > 0.5:
                activated.append(index)

        #print('polygoning')
        multipolygon = h3.h3_set_to_multi_polygon(activated, True)

        output_filename = f"geojson/{filename}-resolution-{target_resolution}.geojson"
        print('writing', output_filename)
        with open(output_filename, "w") as f:
            json.dump({
                "type": "MultiPolygon",
                "coordinates": multipolygon
            }, f)

if __name__ == '__main__':
    # Get the list of filenames in the source folder
    filenames = os.listdir('classified')

    pool = Pool(processes=cpu_count())

    # Process each image in parallel
    pool.map(process_file, filenames)

    # Close the pool
    pool.close()
    pool.join()
