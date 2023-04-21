import json

# Define the coordinates for the Arctic polygon
arctic_coords = [[-180, 77], [180, 77], [180, 86], [-180, 86], [-180, 77]]

# Define the coordinates for the Antarctic polygon
antarctic_coords = [[-180, -86], [180, -86], [180, -59], [-180, -59], [-180, -86]]

# Define a function to generate the GeoJSON polygon for a given resolution
def generate_polygon(coords):
    polygon = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [coords]
                },
                "properties": {}
            }
        ]
    }
    return polygon

# Generate and save the polygons for each resolution
for resolution in range(4, 10):
    arctic_polygon = generate_polygon(arctic_coords)
    antarctic_polygon = generate_polygon(antarctic_coords)

    with open(f"geojson/ARCTIC_PROBAV_LC100_global_v3.0.1_2019-nrt_Snow-CoverFraction-layer_EPSG-4326.json-resolution-{resolution}.geojson", "w") as arctic_file:
        json.dump(arctic_polygon, arctic_file)
        
    with open(f"geojson/ANTARCTIC_PROBAV_LC100_global_v3.0.1_2019-nrt_Snow-CoverFraction-layer_EPSG-4326.json-resolution-{resolution}.geojson", "w") as antarctic_file:
        json.dump(antarctic_polygon, antarctic_file)
