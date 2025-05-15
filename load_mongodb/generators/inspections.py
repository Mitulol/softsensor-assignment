# generator/inspections.py

import random
import logging
from datetime import timedelta
from utils import append_jsonl
from paths import INSPECTIONS_OUTPUT_FILE
from generators.vehicles import get_num_vehicles

# logger = logging.getLogger("inspections")
# handler = logging.FileHandler("inspections.log")
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# handler.setFormatter(formatter)
# logger.addHandler(handler)
# logger.setLevel(logging.INFO)

# Create the logger
logger = logging.getLogger("inspections")
logger.setLevel(logging.INFO)

# Create file handler (writes to logs/inspections.log)
file_handler = logging.FileHandler("logs/inspections.log")
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
file_handler.setLevel(logging.DEBUG)

# Create console handler (prints to terminal)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
console_handler.setLevel(logging.INFO)

# Add both handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Now you can log
logger.debug("Starting inspection generation...")

num_inspections = 0

def get_num_inspections():
    global num_inspections
    return num_inspections

def simulate_inspections(start_date, num_days):
    for i in range(num_days):
        day = start_date + timedelta(days=i)
        logger.info(f"\n🧪 Simulating inspections for day: {day.strftime('%Y-%m-%d')}")

        for vehicle_id in range(1, get_num_vehicles() + 1):
            global num_inspections
            num_inspections += 1
            insp_id = f"insp_{num_inspections}"
            new_inspection = generate_inspection_entry(day, insp_id, vehicle_id)
            append_jsonl(INSPECTIONS_OUTPUT_FILE, new_inspection)
            logger.debug(f"  🧪 Generated inspection {insp_id} for vehicle " f"veh_{vehicle_id}")

    # save_json(INSPECTIONS_OUTPUT_FILE, inspections)
    logger.info(f"💾 Saved inspections to {INSPECTIONS_OUTPUT_FILE}")

def generate_inspection_entry(date, insp_id, vehicle_id):
    INSPECTORS = {
        "Emily Davis": "emp_201",
        "Carlos Nguyen": "emp_202",
        "Riya Sharma": "emp_203",
        "Mark Patel": "emp_204"
    }

    inspector_name = random.choice(list(INSPECTORS.keys()))
    inspector = {
        "id": INSPECTORS[inspector_name],
        "name": inspector_name
    }

    checklist_items = ["Brakes", "Lights", "Tires", "Horn", "Mirrors"]
    checklist = []
    issues = []

    for item in checklist_items:
        status = "Pass" if random.random() > 0.25 else "Fail"
        entry = {"item": item, "status": status}

        if status == "Fail":
            entry["notes"] = random.choice([
                "Needs replacement", "Cracked", "Not responsive", "Low pressure", "Flickering"
            ])
            issues.append({
                "code": f"{item[:3].upper()}{random.randint(1, 99):02}",
                "description": f"{item} issue detected"
            })

        checklist.append(entry)

    return {
        "_id": insp_id,
        "date": date.strftime("%Y-%m-%d"),
        "inspector": inspector,
        "vehicle_id": f"veh_{vehicle_id}",
        "checklist": checklist,
        "issues_found": issues
    }