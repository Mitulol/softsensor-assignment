# generators/vehicles.py

import random
import json
import os
import logging
from utils import append_jsonl
from paths import VEHICLES_OUTPUT_FILE, COMPANIES_OUTPUT_FILE
from datetime import timedelta
from generators.companies import get_num_companies

# logger = logging.getLogger("vehicles")
# handler = logging.FileHandler("logs/vehicles.log")
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# handler.setFormatter(formatter)
# logger.addHandler(handler)
# logger.setLevel(logging.INFO)

# Create the logger
logger = logging.getLogger("vehicles")
logger.setLevel(logging.INFO)

# Create file handler (writes to logs/vehicles.log)
file_handler = logging.FileHandler("logs/vehicles.log")
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
file_handler.setLevel(logging.DEBUG)

# Create console handler (prints to terminal)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
console_handler.setLevel(logging.INFO)

# Add both handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Example usage
logger.debug("Starting vehicle generation...")

num_vehicles = 0

def get_num_vehicles():
    global num_vehicles
    return num_vehicles

# === Main Simulation Function ===
def simulate_days_vehicles_only(start_date, num_days, sim_num_vehicles_in=10):
    # Generate vehicles first
    for _ in range(sim_num_vehicles_in):
        global num_vehicles
        # num_vehicles incremented in generate_new_vehicle
        new_vehicle = generate_new_vehicle()
        if new_vehicle:
            append_jsonl(VEHICLES_OUTPUT_FILE, new_vehicle)
            assigned_company_id = f"company_{random.choice(range(1, get_num_companies() + 1))}"
            append_vehicle_to_company(COMPANIES_OUTPUT_FILE, assigned_company_id, new_vehicle["_id"])
            logger.info(f"🚚 Added new vehicle {new_vehicle['_id']} ({new_vehicle['type']}) with capacity {new_vehicle['capacity_packages']} to {assigned_company_id}")

    for i in range(num_days):
        day = start_date + timedelta(days=i)
        logger.info(f"\n🛠 Simulating vehicle updates for day: {day.strftime('%Y-%m-%d')}")

        temp_path = VEHICLES_OUTPUT_FILE + '.tmp'

        with open(VEHICLES_OUTPUT_FILE, 'r') as infile, open(temp_path, 'w') as outfile:
            for line in infile:
                vehicle = json.loads(line)
                logger.debug(f"  - Updating vehicle {vehicle['_id']}")

                # Add maintenance log if needed
                maintenance = generate_maintenance_log_if_needed(day, vehicle)
                if maintenance:
                    vehicle.setdefault("maintenance_logs", []).append(maintenance)
                    logger.debug(f"    ➤ Added maintenance log with {len(maintenance['details']['tasks'])} tasks")

            # Append GPS points to existing gps stream
                gps_stream = next((s for s in vehicle.setdefault("sensor_streams", []) if s["stream_type"] == "gps"), None)
                if not gps_stream:
                    gps_stream = {"stream_type": "gps", "points": []}
                    vehicle["sensor_streams"].append(gps_stream)
                gps_stream["points"].append(generate_gps_stream(day)["points"][0])
                logger.debug(f"    ➤ Added GPS points")

                # Append fuel readings to existing fuel stream
                fuel_stream = next((s for s in vehicle["sensor_streams"] if s["stream_type"] == "fuel"), None)
                if not fuel_stream:
                    fuel_stream = {"stream_type": "fuel", "readings": []}
                    vehicle["sensor_streams"].append(fuel_stream)
                fuel_data = generate_fuel_stream(day)["readings"]
                fuel_stream["readings"].extend(fuel_data)
                logger.debug(f"    ➤ Added fuel readings: {len(fuel_data)}")

                # Write back the updated vehicle to temp file
                json.dump(vehicle, outfile)
                outfile.write('\n')
        
        os.replace(temp_path, VEHICLES_OUTPUT_FILE)
        logger.info(f"\n💾 Saved updated vehicles for {day.strftime('%Y-%m-%d')} to {VEHICLES_OUTPUT_FILE}")


    logger.debug(f"\n💾 Saved updated vehicles to {VEHICLES_OUTPUT_FILE}")
    logger.debug(f"💾 Updated companies with new fleet data in {COMPANIES_OUTPUT_FILE}")


def generate_new_vehicle():
    global num_vehicles
    new_id = f"veh_{num_vehicles + 1}"
    num_vehicles += 1

    vehicle_types = ["Van", "Truck", "Electric Van"]
    return {
        "_id": new_id,
        "type": random.choice(vehicle_types),
        "capacity_packages": random.randint(150, 600),
        "maintenance_logs": [],
        "sensor_streams": [],
        "current_assignments": []
    }

def append_vehicle_to_company(company_file_path, company_id, vehicle_id):
    temp_path = company_file_path + '.tmp'

    with open(company_file_path, 'r') as infile, open(temp_path, 'w') as outfile:
        for line in infile:
            company = json.loads(line)

            if company["_id"] == company_id:
                company.setdefault("fleet", []).append(vehicle_id)

            json.dump(company, outfile)
            outfile.write('\n')

    os.replace(temp_path, company_file_path)

# === Maintenance Log Generator ===
def generate_maintenance_log_if_needed(date, vehicle):
    if random.random() > 0.9:
        return None  # skip 10% of the time

    last_km = get_last_km_reading(vehicle)
    new_km = last_km + random.randint(40, 200)  # realistic daily increment

    task_pool = ["Oil Change", "Brake Inspection", "Tire Rotation", "Engine Tune-Up", "Filter Replacement"]
    tasks = [{"task": random.choice(task_pool), "cost": random.randint(8, 30) * 10} for _ in range(random.randint(1, 3))]

    return {
        "service_date": date.strftime("%Y-%m-%d"),
        "details": {
            "km_reading": new_km,
            "tasks": tasks
        }
    }

# === GPS Sensor Stream Generator ===
def generate_gps_stream(date):
    return {
        "stream_type": "gps",
        "points": [[
            {
                "ts": date.isoformat(),
                "lat": round(40.5 + random.uniform(-0.1, 0.1), 6),
                "lng": round(-74.0 + random.uniform(-0.1, 0.1), 6)
            },
            {
                "ts": (date + timedelta(minutes=10)).isoformat(),
                "lat": round(40.5 + random.uniform(-0.1, 0.1), 6),
                "lng": round(-74.0 + random.uniform(-0.1, 0.1), 6)
            }
        ]]
    }

# === Fuel Sensor Stream Generator ===
def generate_fuel_stream(date):
    return {
        "stream_type": "fuel",
        "readings": [
            {
                "ts": date.isoformat(),
                "liters": round(random.uniform(2.5, 5.0), 1)
            },
            {
                "ts": (date + timedelta(hours=3)).isoformat(),
                "liters": round(random.uniform(2.5, 5.0), 1)
            }
        ]
    }

def get_last_km_reading(vehicle):
    logs = vehicle.get("maintenance_logs", [])
    if not logs:
        return random.randint(10000, 30000)
    
    try:
        return logs[-1]["details"]["km_reading"]
    except:
        return random.randint(10000, 30000)




