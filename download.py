import os

# Define the base URL and the list of latitudes, longitudes, and kinds
base_url = "https://s3-eu-west-1.amazonaws.com/vito.landcover.global/v3.0.1/2019/"
latitudes = ["S40", "S20", "N00", "N20", "N40", "N60", "N80"]
longitudes = ["W180", "W160", "W140", "W120", "W100", "W080", "W060", "W040", "W020", "E000", "E020", "E040", "E060", "E080", "E100", "E120", "E140", "E160"]
kinds = ["Snow", "Bare", "Grass", "Crops", "Tree", "BuiltUp"]

# Create the sources folder if it doesn't already exist
if not os.path.exists("sources"):
    os.makedirs("sources")

# Loop through the combinations of latitude, longitude, and kind and download each file
for i, latitude in enumerate(latitudes):
    for j, longitude in enumerate(longitudes):
        for k, kind in enumerate(kinds):
            filename = f"{longitude}{latitude}_PROBAV_LC100_global_v3.0.1_2019-nrt_{kind}-CoverFraction-layer_EPSG-4326.tif"
            url = base_url + f"{longitude}{latitude}/{filename}"
            output_path = os.path.join("sources", filename)
            command = f"axel -a -n 10 {url} -o {output_path}"
            print(f"Downloading file {i * len(longitudes) * len(kinds) + j * len(kinds) + k + 1}/{len(latitudes) * len(longitudes) * len(kinds)}: {filename}...")
            os.system(command)

