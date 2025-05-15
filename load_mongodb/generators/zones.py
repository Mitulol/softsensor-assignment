# generator/zones.py

import random
import logging
from utils import append_jsonl
from paths import ZONES_OUTPUT_FILE

# logger = logging.getLogger("zones")
# handler = logging.FileHandler("logs/zones.log")
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# handler.setFormatter(formatter)
# logger.addHandler(handler)
# logger.setLevel(logging.INFO)

# Create the logger
logger = logging.getLogger("zones")
logger.setLevel(logging.INFO)

# Create file handler (writes to logs/zones.log)
file_handler = logging.FileHandler("logs/zones.log")
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
file_handler.setLevel(logging.DEBUG)  # Capture everything to file

# Create console handler (prints to terminal)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
console_handler.setLevel(logging.INFO)  # Show only INFO and above in console

# Add both handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Example usage
logger.debug("Starting zone generation...")

num_zones = 0

BASE_LAT = 40.7
BASE_LNG = -74.0

def get_num_zones():
    global num_zones
    return num_zones

def generate_zones(zones_per_run, num_runs=1):

    logger.debug(f"\n🌐 Generating {zones_per_run * num_runs} zones across {num_runs} run(s)...")

    for run in range(num_runs):
        logger.debug(f"  ▶ Run {run + 1}/{num_runs}")
        for i in range(zones_per_run):
            global num_zones
            num_zones += 1
            new_zone = generate_zone(num_zones)
            append_jsonl(ZONES_OUTPUT_FILE, new_zone)

            logger.info(f"    ➤ Created {new_zone['_id']}")

            

    # save_json(ZONES_OUTPUT_FILE, zones)
    logger.info(f"✅ Zones written to {ZONES_OUTPUT_FILE} (Total: {num_zones})")

def generate_zone(zone_index):
    zone_id = f"zone_{zone_index:05}"
    zone_name = f"Zone {zone_index}"
    
    boundary_count = random.randint(1, 3)
    boundaries = [generate_boundary_ring() for _ in range(boundary_count)]

    subzones = []
    subzone_count = random.randint(1, 5)
    for i in range(subzone_count):
        subzones.append({
            "id": f"{zone_id}_{i+1}",
            "name": f"{zone_name} - Subzone {i+1}"
        })

    return {
        "_id": zone_id,
        "name": zone_name,
        "boundaries": boundaries,
        "subzones": subzones
    }

def generate_boundary_ring():
    points = []
    count = random.randint(3, 6)
    for _ in range(count):
        lat = round(BASE_LAT + random.uniform(-0.5, 0.5), 6)
        lng = round(BASE_LNG + random.uniform(-0.5, 0.5), 6)
        points.append({ "lat": lat, "lng": lng })
    return points

