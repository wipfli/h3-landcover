import json
import h3.api.numpy_int as h3
import numpy as np

resolution = 9
covered_area = {}
with open(f'covered_area-{resolution}.json') as f:
    covered_area = json.load(f)


threshold = 0.5

activated = []
progress = 0
for h, num_pixels in covered_area.items():
    progress += 1
    if progress % 1000 == 0:
        print(progress / len(covered_area.keys()))
    total_area = h3.cell_area(int(h))  # km2
    covered_fraction = covered_area[h] / total_area
    if covered_fraction > threshold:
        activated.append(int(h))

multipolygon = h3.h3_set_to_multi_polygon(activated, True)

with open(f'multipolygon-{resolution}.geojson', 'w') as f:
    json.dump({
        "type": "MultiPolygon",
        "coordinates": multipolygon
    }, f)
