# generators/stops.py

import random
import json
import os
import logging
from datetime import timedelta
from utils import append_jsonl
from paths import STOPS_OUTPUT_FILE, VEHICLES_OUTPUT_FILE

# logger = logging.getLogger("stops")
# handler = logging.FileHandler("logs/stops.log")
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# handler.setFormatter(formatter)
# logger.addHandler(handler)
# logger.setLevel(logging.INFO)

# Create the logger
logger = logging.getLogger("stops")
logger.setLevel(logging.INFO)

# Create file handler (writes to logs/stops.log)
file_handler = logging.FileHandler("logs/stops.log")
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
logger.debug("Starting stop generation...")

num_stops = 0
num_packages = 0

def get_num_stops():
    global num_stops
    return num_stops

def get_num_packages():
    global num_packages
    return num_packages

def simulate_stops(start_date, num_days, stops_per_day_per_vehicle):
    for i in range(num_days):
        day = start_date + timedelta(days=i)
        logger.info(f"\n📦 Simulating stops for day: {day.strftime('%Y-%m-%d')}")

        # for vehicle in vehicles:
        temp_vehicles_path = VEHICLES_OUTPUT_FILE + '.tmp'
        with open(VEHICLES_OUTPUT_FILE, 'r') as vehicles_infile, open(temp_vehicles_path, 'w') as vehicles_outfile:
            for line in vehicles_infile:
                vehicle = json.loads(line)

                for _ in range(stops_per_day_per_vehicle):
                    global num_stops
                    num_stops += 1
                    stop_id = f"stop_{num_stops}"
                    new_stop = generate_stop_entry(stop_id, day)
                    append_jsonl(STOPS_OUTPUT_FILE, new_stop)
                    logger.debug(f"  ➤ Created stop {stop_id} at {new_stop['address']}")

                    assignment = next(
                        (a for a in vehicle.get("current_assignments", [])
                        if a["start_date"] == day.strftime("%Y-%m-%d")),
                        None
                    )

                    if not assignment:
                        assignment = {
                            "route_id": f"rte_sim_{day.strftime('%Y%m%d')}",
                            "start_date": day.strftime("%Y-%m-%d"),
                            "details": {
                                "planned_stops": [],
                                "backup_vehicles": []
                            }
                        }
                        vehicle.setdefault("current_assignments", []).append(assignment)
                        logger.debug(f"    ➕ Created new route {assignment['route_id']} for vehicle {vehicle['_id']}")

                    assignment["details"]["planned_stops"].append(stop_id)
                    logger.debug(f"    🔗 Assigned stop {stop_id} to vehicle {vehicle['_id']} on route {assignment['route_id']}")

                json.dump(vehicle, vehicles_outfile)
                vehicles_outfile.write('\n')
        
        os.replace(temp_vehicles_path, VEHICLES_OUTPUT_FILE)

    logger.info(f"\n💾 Finished simulating stops across {num_days} days")
    logger.debug(f"\n💾 Saved stops to {STOPS_OUTPUT_FILE}")
    logger.debug(f"💾 Updated vehicle assignments in {VEHICLES_OUTPUT_FILE}")


def generate_stop_entry(stop_id, date):
    global num_packages
    num_packages += 1
    pkg_id = f"pkg_{num_packages}"
    address = f"{random.randint(100, 999)} Simulated Blvd, Newark, NJ"

    # Randomly decide how many failed attempts (0 to 2)
    num_exceptions = random.randint(0, 2)

    attempts = []
    for i in range(num_exceptions):
        attempts.append({
            "ts": (date + timedelta(minutes=30 * i)).isoformat(),
            "status": "Exception",
            "exception": {
                "code": random.choice(["NO_ACCESS", "CUSTOMER_NOT_HOME"]),
                "reason": random.choice(["Gate locked", "No response at door"])
            }
        })

    # Always end with a successful delivery
    attempts.append({
        "ts": (date + timedelta(minutes=30 * (num_exceptions + 1))).isoformat(),
        "status": "Delivered"
    })

    # 30% chance of a callback issue
    callbacks = []
    if random.random() < 0.3:
        callbacks.append({
            "callback_ts": (date + timedelta(days=1)).isoformat(),
            "issues": [
                {
                    "type": random.choice(["missing_item", "damaged_item"]),
                    "detail": random.choice(["Wrong SKU", "Crushed packaging", "Broken seal"])
                }
            ]
        })

    return {
        "_id": stop_id,
        "package_id": pkg_id,
        "address": address,
        "events": [
            {"type": "arrival", "ts": date.isoformat()},
            {"type": "delivery_attempts", "attempts": attempts}
        ],
        "customer_callbacks": callbacks
    }