# generators/drivers.py

import random
import json
import os
import logging
from datetime import datetime, timedelta
from utils import append_jsonl
from paths import DRIVERS_OUTPUT_FILE, COMPANIES_OUTPUT_FILE
from generators.companies import get_num_companies

# logger = logging.getLogger("drivers")
# handler = logging.FileHandler("logs/drivers.log")
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# handler.setFormatter(formatter)
# logger.addHandler(handler)
# logger.setLevel(logging.INFO)

# Create the logger
logger = logging.getLogger("drivers")
logger.setLevel(logging.DEBUG)

# Create file handler (writes to logs/drivers.log)
file_handler = logging.FileHandler("logs/drivers.log")
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
logger.debug("Driver generation started.")

num_drivers = 0

CERTIFICATION_TYPES = [
    "Safety", "Hazmat", "First Aid", "Heavy Load", "Cold Chain", "Forklift"
]

SHIFT_WINDOWS = [
    ("06:00", "14:00"),
    ("08:00", "12:00"),
    ("14:00", "22:00"),
    ("16:00", "20:00")
]

DAYS_OF_WEEK = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

def get_num_drivers():
    global num_drivers
    return num_drivers

def generate_drivers(drivers_per_run, num_runs=1):

    logger.info(f"\n🧍 Generating {drivers_per_run * num_runs} drivers across {num_runs} run(s)...")

    for run in range(num_runs):
        logger.debug(f"  ▶ Run {run + 1}/{num_runs}")
        for _ in range(drivers_per_run):
            global num_drivers
            num_drivers += 1
            driver_id = f"drv_{num_drivers}"
            new_driver = generate_driver(driver_id)
            append_jsonl(DRIVERS_OUTPUT_FILE, new_driver)


            assigned_company_id = f"company_{random.choice(range(1, get_num_companies() + 1))}"
            append_driver_to_company(COMPANIES_OUTPUT_FILE, assigned_company_id, driver_id)
            logger.info(f"    ➤ Assigned {driver_id} to {assigned_company_id}")

    logger.info(f"✅ Drivers written to {DRIVERS_OUTPUT_FILE} (Total: {num_drivers})")

def generate_driver(driver_id):
    return {
        "_id": driver_id,
        "name": f"Driver {driver_id[-4:]}",
        "license": generate_license(),
        "certifications": generate_certifications(),
        "weekly_schedule": generate_weekly_schedule()
    }

def generate_license():
    return {
        "class": random.choice(["Class A", "Class B", "Class C"]),
        "expiry": (datetime.today() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d")
    }

def generate_certifications():
    selected = random.sample(CERTIFICATION_TYPES, k=random.randint(1, 3))
    certs = []
    for cert in selected:
        levels = ["Basic"] if random.random() < 0.5 else ["Basic", "Advanced"]
        certs.append({"type": cert, "levels": levels})
    return certs

def generate_weekly_schedule():
    days = random.sample(DAYS_OF_WEEK, k=random.randint(2, 5))
    schedule = []
    for day in sorted(days, key=DAYS_OF_WEEK.index):  # preserve Mon–Sun order
        schedule.append({
            "day": day,
            "shifts": generate_shifts_for_day()
        })
    return schedule

def generate_shifts_for_day():
    shift_count = random.choice([1, 2])
    available = SHIFT_WINDOWS.copy()
    random.shuffle(available)

    first = available.pop()
    shifts = [first]

    if shift_count == 2:
        non_overlapping = [s for s in available if not shifts_overlap(first, s)]
        if non_overlapping:
            second = random.choice(non_overlapping)
            shifts.append(second)

    # Sort by start time before returning
    shifts.sort(key=lambda x: parse_time(x[0]))
    return [{"start": start, "end": end} for start, end in shifts]

def shifts_overlap(s1, s2):
    s1_start, s1_end = map(parse_time, s1)
    s2_start, s2_end = map(parse_time, s2)
    return not (s1_end <= s2_start or s2_end <= s1_start)

def parse_time(t): return datetime.strptime(t, "%H:%M")

def append_driver_to_company(company_file_path, company_id, driver_id):
    temp_path = company_file_path + '.tmp'

    with open(company_file_path, 'r') as infile, open(temp_path, 'w') as outfile:
        for line in infile:
            company = json.loads(line)

            if company["_id"] == company_id:
                company.setdefault("drivers", []).append(driver_id)

            json.dump(company, outfile)
            outfile.write('\n')

    os.replace(temp_path, company_file_path)

