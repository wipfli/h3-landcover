import os
import zipfile
import glob

if not os.path.exists("zips"):
    os.makedirs("zips")

kinds = ["Snow", "Bare-Snow", "Grass-Bare-Snow", "Crops", "Tree", "BuiltUp"]
resolutions = [4, 5, 6, 7, 8, 9]

for kind in kinds:
    for resolution in resolutions:
        zip_filename = f"zips/{kind}-resolution-{resolution}.zip"
        print('writing', zip_filename)
        file_count = 0
        with zipfile.ZipFile(zip_filename, "w") as zip_file:
            # Create the zip folder if needed
            
            pattern = f"geojson/*_PROBAV_LC100_global_v3.0.1_2019-nrt_{kind}-CoverFraction-layer_EPSG-4326.json-resolution-{resolution}.geojson"
            for filename in glob.glob(pattern):
                # Convert the file from GeoJSON to GPKG
                gpkg_filename = os.path.splitext(filename.split('/')[1])[0] + ".gpkg"
                if os.stat(filename).st_size == 43:
                    # file is empty
                    continue
                file_count += 1
                print(gpkg_filename)
                os.system(f"ogr2ogr -f 'GPKG' {gpkg_filename} {filename}")
                # Add the file to the zip folder
                zip_file.write(gpkg_filename)
                # Remove the temporary GPKG file
                os.remove(gpkg_filename)
        
        if file_count == 0:
            os.remove(zip_filename)
