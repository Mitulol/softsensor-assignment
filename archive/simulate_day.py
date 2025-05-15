import json
import random
import os
from datetime import datetime, timedelta
import argparse
import sys

# sys.stdout = open('logs.txt', 'w')
# sys.stderr = sys.stdout  # Optional: send errors to same file


# Paths to JSON files
VEHICLES_FILE = "vehicles.json"
STOPS_FILE = "stops.json"
INSPECTIONS_FILE = "inspections.json"
DRIVERS_FILE = "drivers.json"
COMPANIES_FILE = "logistics_companies.json"
ZONES_FILE = "zones.json"


# Output file paths
VEHICLES_OUTPUT_FILE = "data/vehicles_simulated.jsonl"
STOPS_OUTPUT_FILE = "data/stops_simulated.jsonl"
INSPECTIONS_OUTPUT_FILE = "data/inspections_simulated.jsonl"
ZONES_OUTPUT_FILE = "data/zones_simulated.jsonl"
DRIVERS_OUTPUT_FILE = "data/drivers_simulated.jsonl"
COMPANIES_OUTPUT_FILE = "data/logistics_companies_simulated.jsonl"

BASE_LAT = 40.7
BASE_LNG = -74.0

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

REGIONS = [
    "North-East USA", "Midwest USA", "West Coast USA",
    "South-East USA", "Southwest USA", "Pacific Northwest",
    "Mountain States", "Great Plains", "Mid-Atlantic", "New England"
]

num_zones = 0
num_companies = 0
num_vehicles = 0
num_stops = 0
num_inspections = 0
num_drivers = 0
num_packages = 0

# Load existing JSON data
def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, 'r') as f:
        return json.load(f)

# Save updated JSON data
def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def append_jsonl(path, obj):
    with open(path, 'a') as f:
        json.dump(obj, f)
        f.write('\n')

def convert_jsonl_to_json_streaming(jsonl_path, json_path):
    with open(jsonl_path, 'r') as infile, open(json_path, 'w') as outfile:
        outfile.write('[')

        first = True
        for line in infile:
            line = line.strip()
            if not line:
                continue  # skip empty lines

            if not first:
                outfile.write(',')
            else:
                first = False

            obj = json.loads(line)
            json.dump(obj, outfile)

        outfile.write(']')

    print(f"✅ Successfully converted {jsonl_path} to {json_path} without memory overflow.")

def get_last_km_reading(vehicle):
    logs = vehicle.get("maintenance_logs", [])
    if not logs:
        return random.randint(10000, 30000)
    
    try:
        return logs[-1]["details"]["km_reading"]
    except:
        return random.randint(10000, 30000)

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


def generate_new_vehicle():
    # Extract numeric parts of all vehicle IDs like veh_1001
    # existing_ids = [v["_id"] for v in existing_vehicles if v["_id"].startswith("veh_")]
    # max_id_num = 1000  # default starting point

    # for vid in existing_ids:
    #     try:
    #         num = int(vid.split("_")[1])
    #         max_id_num = max(max_id_num, num)
    #     except:
    #         continue
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

# === Main Simulation Function ===
def simulate_days_vehicles_only(start_date, num_days, sim_num_vehicles_in=10):
    # vehicles = load_json(VEHICLES_OUTPUT_FILE)
    # companies = load_json(COMPANIES_OUTPUT_FILE)

    # Generate vehicles first
    for _ in range(sim_num_vehicles_in):
        global num_vehicles
        # num_vehicles += 1
        new_vehicle = generate_new_vehicle()
        if new_vehicle:
            # vehicles.append(new_vehicle)
            append_jsonl(VEHICLES_OUTPUT_FILE, new_vehicle)
            assigned_company_id = f"company_{random.choice(range(1, num_companies + 1))}"
            # assigned_company["fleet"].append(new_vehicle["_id"])
            append_vehicle_to_company(COMPANIES_OUTPUT_FILE, assigned_company_id, new_vehicle["_id"])
            print(f"🚚 Added new vehicle {new_vehicle['_id']} ({new_vehicle['type']}) with capacity {new_vehicle['capacity_packages']} to {assigned_company_id}")

    for i in range(num_days):
        day = start_date + timedelta(days=i)
        # print(f"Simulating vehicle updates for day: {day.date()}")
        print(f"\n🛠 Simulating vehicle updates for day: {day.strftime('%Y-%m-%d')}")

        # assigned_company = random.choice(companies)

        # Deprecated: Add new vehicle periodically
        # # Add new vehicle periodically
        # new_vehicle = generate_new_vehicle(i, vehicles)
        # if new_vehicle:
        #     vehicles.append(new_vehicle)
        #     assigned_company["fleet"].append(new_vehicle["_id"])
        #     print(f"🚚 Added new vehicle {new_vehicle['_id']} ({new_vehicle['type']}) with capacity {new_vehicle['capacity_packages']} to {assigned_company['_id']}")
        #     # print(f"🚚 Added new vehicle {new_vehicle['_id']} to {assigned_company['_id']}")

        temp_path = VEHICLES_OUTPUT_FILE + '.tmp'

        with open(VEHICLES_OUTPUT_FILE, 'r') as infile, open(temp_path, 'w') as outfile:
            for line in infile:
                vehicle = json.loads(line)
                print(f"  - Updating vehicle {vehicle['_id']}")

                # Add maintenance log if needed
                maintenance = generate_maintenance_log_if_needed(day, vehicle)
                if maintenance:
                    vehicle.setdefault("maintenance_logs", []).append(maintenance)
                    print(f"    ➤ Added maintenance log with {len(maintenance['details']['tasks'])} tasks")

            # Add daily fuel sensor stream
            # vehicle.setdefault("sensor_streams", []).append(generate_gps_stream(day))
            # vehicle.setdefault("sensor_streams", []).append(generate_fuel_stream(day))

            # Append GPS points to existing gps stream
                gps_stream = next((s for s in vehicle.setdefault("sensor_streams", []) if s["stream_type"] == "gps"), None)
                if not gps_stream:
                    gps_stream = {"stream_type": "gps", "points": []}
                    vehicle["sensor_streams"].append(gps_stream)
                gps_stream["points"].append(generate_gps_stream(day)["points"][0])
                print(f"    ➤ Added GPS points")

                # Append fuel readings to existing fuel stream
                fuel_stream = next((s for s in vehicle["sensor_streams"] if s["stream_type"] == "fuel"), None)
                if not fuel_stream:
                    fuel_stream = {"stream_type": "fuel", "readings": []}
                    vehicle["sensor_streams"].append(fuel_stream)
                fuel_data = generate_fuel_stream(day)["readings"]
                fuel_stream["readings"].extend(fuel_data)
                print(f"    ➤ Added fuel readings: {len(fuel_data)}")

                # Write back the updated vehicle to temp file
                json.dump(vehicle, outfile)
                outfile.write('\n')
        
        os.replace(temp_path, VEHICLES_OUTPUT_FILE)
        print(f"\n💾 Saved updated vehicles for {day.strftime('%Y-%m-%d')} to {VEHICLES_OUTPUT_FILE}")


    # save_json(VEHICLES_OUTPUT_FILE, vehicles)
    print(f"\n💾 Saved updated vehicles to {VEHICLES_OUTPUT_FILE}")
    # save_json(COMPANIES_OUTPUT_FILE, companies)
    print(f"💾 Updated companies with new fleet data in {COMPANIES_OUTPUT_FILE}")

def get_next_stop_index(existing_stops):
    stop_ids = [s["_id"] for s in existing_stops if s["_id"].startswith("stop_")]
    nums = []

    for sid in stop_ids:
        try:
            suffix = sid.split("_")[1]
            nums.append(int(suffix))
        except:
            continue

    return max(nums, default=2) + 1  # default=2 since stop_1 and stop_2 exist



def generate_stop_entry(stop_id, date):
    # stop_id = f"stop_sim_{date.strftime('%Y%m%d')}_{index}"
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

def get_next_insp_index(existing_inspections):
    nums = []
    for ins in existing_inspections:
        if ins["_id"].startswith("insp_"):
            try:
                nums.append(int(ins["_id"].split("_")[1]))
            except:
                continue
    return max(nums, default=1000) + 1

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
# Deprecated: Simulate stops and inspections
# def simulate_stops_and_inspections(start_date, num_days):
#     stops = load_json(STOPS_OUTPUT_FILE)
#     inspections = load_json(INSPECTIONS_OUTPUT_FILE)
#     vehicles = load_json(VEHICLES_OUTPUT_FILE)

#     stop_index = get_next_stop_index(stops)

#     for i in range(num_days):
#         day = start_date + timedelta(days=i)
#         print(f"\n📦 Simulating stops and inspections for day: {day.strftime('%Y-%m-%d')}")

#         # Add 2 simulated stops per day
#         for j in range(2):
#             stop_id = f"stop_{stop_index}"

#             # Generate the stop
#             stop = generate_stop_entry(stop_id, day)
#             stops.append(stop)
#             print(f"  ➤ Created stop {stop_id} at {stop['address']}")

#             # Assign to a random vehicle
#             assigned_vehicle = random.choice(vehicles)

#             # Ensure current_assignments[] exists and has a route for today
#             assignment = next(
#                 (a for a in assigned_vehicle.get("current_assignments", [])
#                 if a["start_date"] == day.strftime("%Y-%m-%d")),
#                 None
#             )

#             if not assignment:
#                 assignment = {
#                     "route_id": f"rte_sim_{day.strftime('%Y%m%d')}",
#                     "start_date": day.strftime("%Y-%m-%d"),
#                     "details": {
#                         "planned_stops": [],
#                         "backup_vehicles": []
#                     }
#                 }
#                 assigned_vehicle.setdefault("current_assignments", []).append(assignment)
#                 print(f"    ➕ Created new route {assignment['route_id']} for vehicle {assigned_vehicle['_id']}")


#             # Append stop ID to planned_stops
#             assignment["details"]["planned_stops"].append(stop_id)
#             print(f"    🔗 Assigned stop {stop_id} to vehicle {assigned_vehicle['_id']} on route {assignment['route_id']}")

#             stop_index += 1

#         # Add 1 inspection per vehicle per day
#         # for j, vehicle in enumerate(vehicles):
#         #     # inspections.append(generate_inspection_entry(day, j, vehicle["_id"]))
#         #     inspection = generate_inspection_entry(day, j, vehicle["_id"])
#         #     inspections.append(inspection)
#         #     print(f"  🧪 Generated inspection for vehicle {vehicle['_id']}")

#         insp_index = get_next_insp_index(inspections)

#         for vehicle in vehicles:
#             insp_id = f"insp_{insp_index}"
#             inspections.append(generate_inspection_entry(day, insp_id, vehicle["_id"]))
#             print(f"  🧪 Generated inspection {insp_id} for vehicle {vehicle['_id']}")
#             insp_index += 1

#     save_json(STOPS_OUTPUT_FILE, stops)
#     save_json(INSPECTIONS_OUTPUT_FILE, inspections)
#     save_json(VEHICLES_OUTPUT_FILE, vehicles)
#     print(f"\n💾 Saved stops to {STOPS_OUTPUT_FILE}")
#     print(f"💾 Saved inspections to {INSPECTIONS_OUTPUT_FILE}")
#     print(f"💾 Saved vehicle assignments to {VEHICLES_OUTPUT_FILE}")

def simulate_stops(start_date, num_days, stops_per_day_per_vehicle):
    # stops = load_json(STOPS_OUTPUT_FILE)
    # vehicles = load_json(VEHICLES_OUTPUT_FILE)
    # stop_index = get_next_stop_index(stops)

    for i in range(num_days):
        day = start_date + timedelta(days=i)
        print(f"\n📦 Simulating stops for day: {day.strftime('%Y-%m-%d')}")

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
                    # stops.append(stop)
                    append_jsonl(STOPS_OUTPUT_FILE, new_stop)
                    print(f"  ➤ Created stop {stop_id} at {new_stop['address']}")

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
                        print(f"    ➕ Created new route {assignment['route_id']} for vehicle {vehicle['_id']}")

                    assignment["details"]["planned_stops"].append(stop_id)
                    print(f"    🔗 Assigned stop {stop_id} to vehicle {vehicle['_id']} on route {assignment['route_id']}")

                json.dump(vehicle, vehicles_outfile)
                vehicles_outfile.write('\n')
        
        os.replace(temp_vehicles_path, VEHICLES_OUTPUT_FILE)

    # save_json(STOPS_OUTPUT_FILE, stops)
    # save_json(VEHICLES_OUTPUT_FILE, vehicles)
    print(f"\n💾 Finished simulating stops across {num_days} days")
    print(f"\n💾 Saved stops to {STOPS_OUTPUT_FILE}")
    print(f"💾 Updated vehicle assignments in {VEHICLES_OUTPUT_FILE}")

def simulate_inspections(start_date, num_days):
    # inspections = load_json(INSPECTIONS_OUTPUT_FILE)
    # vehicles = load_json(VEHICLES_OUTPUT_FILE)
    # insp_index = get_next_insp_index(inspections)

    for i in range(num_days):
        day = start_date + timedelta(days=i)
        print(f"\n🧪 Simulating inspections for day: {day.strftime('%Y-%m-%d')}")

        for vehicle_id in range(1, num_vehicles + 1):
            global num_inspections
            num_inspections += 1
            insp_id = f"insp_{num_inspections}"
            # inspections.append(generate_inspection_entry(day, insp_id, vehicle["_id"]))
            new_inspection = generate_inspection_entry(day, insp_id, vehicle_id)
            append_jsonl(INSPECTIONS_OUTPUT_FILE, new_inspection)
            print(f"  🧪 Generated inspection {insp_id} for vehicle " f"veh_{vehicle_id}")

    # save_json(INSPECTIONS_OUTPUT_FILE, inspections)
    print(f"💾 Saved inspections to {INSPECTIONS_OUTPUT_FILE}")




def get_next_zone_index(existing_zones):
    nums = []
    for z in existing_zones:
        if z["_id"].startswith("zone_"):
            try:
                n = int(z["_id"].split("_")[1])
                nums.append(n)
            except:
                continue
    return max(nums, default=0) + 1

def generate_boundary_ring():
    points = []
    count = random.randint(3, 6)
    for _ in range(count):
        lat = round(BASE_LAT + random.uniform(-0.5, 0.5), 6)
        lng = round(BASE_LNG + random.uniform(-0.5, 0.5), 6)
        points.append({ "lat": lat, "lng": lng })
    return points

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

def generate_zones(zones_per_run, num_runs=1):
    # zones = load_json(ZONES_OUTPUT_FILE)
    # companies = load_json(COMPANIES_OUTPUT_FILE)
    # next_index = get_next_zone_index(zones)

    print(f"\n🌐 Generating {zones_per_run * num_runs} zones across {num_runs} run(s)...")

    for run in range(num_runs):
        print(f"  ▶ Run {run + 1}/{num_runs}")
        for i in range(zones_per_run):
            global num_zones
            num_zones += 1
            new_zone = generate_zone(num_zones)
            append_jsonl(ZONES_OUTPUT_FILE, new_zone)

            # deprecated: Assign to a random company
            # assigned_company = random.choice(companies)
            # assigned_company["active_zones"].append(zone["_id"])

            print(f"    ➤ Created {new_zone['_id']}")

            

    # save_json(ZONES_OUTPUT_FILE, zones)
    print(f"✅ Zones written to {ZONES_OUTPUT_FILE} (Total: {num_zones})")

def get_next_driver_index(existing_drivers):
    nums = []
    for d in existing_drivers:
        if d["_id"].startswith("drv_"):
            try:
                nums.append(int(d["_id"].split("_")[1]))
            except:
                continue
    return max(nums, default=5002) + 1

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

def parse_time(t): return datetime.strptime(t, "%H:%M")

def shifts_overlap(s1, s2):
    s1_start, s1_end = map(parse_time, s1)
    s2_start, s2_end = map(parse_time, s2)
    return not (s1_end <= s2_start or s2_end <= s1_start)

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

def generate_weekly_schedule():
    days = random.sample(DAYS_OF_WEEK, k=random.randint(2, 5))
    schedule = []
    for day in sorted(days, key=DAYS_OF_WEEK.index):  # preserve Mon–Sun order
        schedule.append({
            "day": day,
            "shifts": generate_shifts_for_day()
        })
    return schedule

def generate_driver(driver_id):
    return {
        "_id": driver_id,
        "name": f"Driver {driver_id[-4:]}",
        "license": generate_license(),
        "certifications": generate_certifications(),
        "weekly_schedule": generate_weekly_schedule()
    }

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

def generate_drivers(drivers_per_run, num_runs=1):
    # drivers = load_json(DRIVERS_OUTPUT_FILE)
    # next_index = get_next_driver_index(drivers)
    # companies = load_json(COMPANIES_OUTPUT_FILE)


    print(f"\n🧍 Generating {drivers_per_run * num_runs} drivers across {num_runs} run(s)...")

    for run in range(num_runs):
        print(f"  ▶ Run {run + 1}/{num_runs}")
        for _ in range(drivers_per_run):
            global num_drivers
            num_drivers += 1
            driver_id = f"drv_{num_drivers}"
            new_driver = generate_driver(driver_id)
            # drivers.append(driver)
            append_jsonl(DRIVERS_OUTPUT_FILE, new_driver)


            assigned_company_id = f"company_{random.choice(range(1, num_companies + 1))}"
            # assigned_company["drivers"].append(driver_id)
            append_driver_to_company(COMPANIES_OUTPUT_FILE, assigned_company_id, driver_id)
            print(f"    ➤ Assigned {driver_id} to {assigned_company_id}")


    # save_json(DRIVERS_OUTPUT_FILE, drivers)
    # save_json(COMPANIES_OUTPUT_FILE, companies)
    print(f"✅ Drivers written to {DRIVERS_OUTPUT_FILE} (Total: {num_drivers})")

def get_next_company_index(existing):
    ids = []
    for company in existing:
        if company["_id"].startswith("company_"):
            try:
                ids.append(int(company["_id"].split("_")[1]))
            except:
                continue
    return max(ids, default=2) + 1

def generate_company(company_id_num, available_zones):
    company_id = f"company_{company_id_num:03}"
    name = f"Company {company_id_num}"
    region = REGIONS[(company_id_num - 1) % len(REGIONS)]

    num_assigned_zones = random.randint(1, min(5, available_zones))
    # assigned_zone_ids = [z["_id"] for z in random.sample(available_zones, k=num_assigned_zones)]
    assigned_zone_ids = [f"zone_{z:05}" for z in random.sample(range(1, num_zones + 1), k=num_assigned_zones)]


    return {
        "_id": company_id,
        "name": name,
        "region": region,
        "fleet": [],
        "drivers": [],
        "active_zones": assigned_zone_ids
    }

def generate_companies(num_new):
    # companies = load_json(COMPANIES_OUTPUT_FILE)
    # zones = load_json(ZONES_OUTPUT_FILE)
    # next_index = get_next_company_index(companies)

    print(f"🏢 Adding {num_new} new logistics companies...")

    for i in range(num_new):
        global num_companies
        num_companies += 1
        new_company = generate_company(num_companies, num_zones)
        # companies.append(company)
        append_jsonl(COMPANIES_OUTPUT_FILE, new_company)
        # print(f"  ➤ Created {company['_id']}: {company['name']} in {company['region']}")
        print(f"  ➤ Created {new_company['_id']}: {new_company['name']} in {new_company['region']}, Zones: {new_company['active_zones']}")
        

    # save_json(COMPANIES_OUTPUT_FILE, companies)
    print(f"✅ Saved updated company list to {COMPANIES_OUTPUT_FILE} (Total: {num_companies})")
















if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate logistics data generation.")
    parser.add_argument("--append", action="store_true", help="Append to existing output files instead of overwriting.")
    parser.add_argument("--scale", type=int, default=1, help="Scaling factor for all entities. Default = 1.")
    parser.add_argument("--days", type=int, default=20, help="Number of days to simulate. Default = 20.")
    args = parser.parse_args()

    if not args.append:
        print("🧹 Overwriting all output files (default behavior).")
        for path in [
            VEHICLES_OUTPUT_FILE,
            STOPS_OUTPUT_FILE,
            INSPECTIONS_OUTPUT_FILE,
            ZONES_OUTPUT_FILE,
            DRIVERS_OUTPUT_FILE,
            COMPANIES_OUTPUT_FILE
        ]:
            open(path, 'w').close()  # Empty valid JSON array
    else:
        print("➕ Appending to existing output files.")

    today = datetime.today()

    scaling_factor = args.scale
    num_days = args.days

    sim_num_companies = 100
    sim_num_vehicles = 500
    sim_num_stops_per_day_per_vehicle = 5
    sim_num_inspections_per_day_per_vehicle = 1
    sim_num_zones = 80
    sim_num_drivers = 600

    generate_zones(scaling_factor * sim_num_zones)
    generate_companies(scaling_factor * sim_num_companies)
    simulate_days_vehicles_only(today, num_days, scaling_factor * sim_num_vehicles)
    simulate_stops(today, num_days, sim_num_stops_per_day_per_vehicle)
    simulate_inspections(today, num_days)
    generate_drivers(scaling_factor * sim_num_drivers)

    convert_jsonl_to_json_streaming(VEHICLES_OUTPUT_FILE, VEHICLES_FILE)
    convert_jsonl_to_json_streaming(STOPS_OUTPUT_FILE, STOPS_FILE)
    convert_jsonl_to_json_streaming(INSPECTIONS_OUTPUT_FILE, INSPECTIONS_FILE)
    convert_jsonl_to_json_streaming(ZONES_OUTPUT_FILE, ZONES_FILE)
    convert_jsonl_to_json_streaming(DRIVERS_OUTPUT_FILE, DRIVERS_FILE)
    convert_jsonl_to_json_streaming(COMPANIES_OUTPUT_FILE, COMPANIES_FILE)
    print("✅ All data generation and conversion completed successfully.")