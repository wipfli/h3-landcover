import os
import json

# Define the latitudes and longitudes
latitudes = ['S40', 'S20', 'N00', 'N20', 'N40', 'N60', 'N80']
longitudes = ['W180', 'W160', 'W140', 'W120', 'W100', 'W080', 'W060', 'W040', 'W020', 'E000', 'E020', 'E040', 'E060', 'E080', 'E100', 'E120', 'E140', 'E160']

# Define the kinds
kinds = {'Bare-Snow': ['Bare', 'Snow'], 'Grass-Bare-Snow': ['Grass', 'Bare', 'Snow']}

progress = 0

# Loop through all latitude, longitude combinations
for latitude in latitudes:
    for longitude in longitudes:
        # Define the input and output filenames
        input_filename = f'classified/{longitude}{latitude}_PROBAV_LC100_global_v3.0.1_2019-nrt_{{}}-CoverFraction-layer_EPSG-4326.json'
        output_filenames = {new_kind: f'classified/{longitude}{latitude}_PROBAV_LC100_global_v3.0.1_2019-nrt_{new_kind}-CoverFraction-layer_EPSG-4326.json' for new_kind in kinds}
        
        # Loop through the kinds
        for new_kind, old_kinds in kinds.items():
            # Create a new dictionary
            new_dict = {}
            quadrant_exists = False
            for old_kind in old_kinds:
                # Check if the input file exists
                if os.path.exists(input_filename.format(old_kind)):
                    # Load the input dictionary
                    quadrant_exists = True
                    with open(input_filename.format(old_kind), 'r') as f:
                        old_dict = json.load(f)
                    # Loop through the cells of the input dictionary and add them to the cells of the new output dictionary
                    for cell_id, area in old_dict.items():
                        if cell_id in new_dict:
                            new_dict[cell_id] += area
                        else:
                            new_dict[cell_id] = area

            # Write the new dictionary to the output file
            progress += 1
            if quadrant_exists:
                with open(output_filenames[new_kind], 'w') as f:
                    print('writing', output_filenames[new_kind], progress, '/', len(latitudes) * len(longitudes) * len(kinds))
                    json.dump(new_dict, f)
