# main.py

import argparse
import paths
from datetime import datetime
from generators.vehicles import simulate_days_vehicles_only, get_num_vehicles
from generators.stops import simulate_stops, get_num_stops
from generators.inspections import simulate_inspections, get_num_inspections
from generators.zones import generate_zones, get_num_zones
from generators.companies import generate_companies, get_num_companies
from generators.drivers import generate_drivers, get_num_drivers
from utils import convert_jsonl_to_json_streaming


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate logistics data generation.")
    parser.add_argument("--scale", type=int, default=1, help="Scaling factor for all entities. Default = 1.")
    parser.add_argument("--days", type=int, default=20, help="Number of days to simulate. Default = 20.")
    args = parser.parse_args()

    print("🧹 Overwriting all output files (default behavior).")
    for path in [
        paths.VEHICLES_OUTPUT_FILE,
        paths.STOPS_OUTPUT_FILE,
        paths.INSPECTIONS_OUTPUT_FILE,
        paths.ZONES_OUTPUT_FILE,
        paths.DRIVERS_OUTPUT_FILE,
        paths.COMPANIES_OUTPUT_FILE
    ]:
        open(path, 'w').close()  # Empty valid JSON array

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
    print("✅ Finished generating zones.")
    generate_companies(scaling_factor * sim_num_companies)
    print("✅ Finished generating companies.")
    simulate_days_vehicles_only(today, num_days, scaling_factor * sim_num_vehicles)
    print("✅ Finished generating vehicles.")
    simulate_stops(today, num_days, sim_num_stops_per_day_per_vehicle)
    print("✅ Finished generating stops.")
    simulate_inspections(today, num_days)
    print("✅ Finished generating inspections.")
    generate_drivers(scaling_factor * sim_num_drivers)
    print("✅ Finished generating drivers.")

    convert_jsonl_to_json_streaming(paths.ZONES_OUTPUT_FILE, paths.ZONES_FILE)
    convert_jsonl_to_json_streaming(paths.COMPANIES_OUTPUT_FILE, paths.COMPANIES_FILE)
    convert_jsonl_to_json_streaming(paths.VEHICLES_OUTPUT_FILE, paths.VEHICLES_FILE)
    convert_jsonl_to_json_streaming(paths.STOPS_OUTPUT_FILE, paths.STOPS_FILE)
    convert_jsonl_to_json_streaming(paths.INSPECTIONS_OUTPUT_FILE, paths.INSPECTIONS_FILE)
    convert_jsonl_to_json_streaming(paths.DRIVERS_OUTPUT_FILE, paths.DRIVERS_FILE)
    print("✅ All data generation and conversion completed successfully.")
    print("🚨 Summary of generated data:")
    print(f"  - Zones: {get_num_zones()}")
    print(f"  - Companies: {get_num_companies()}")
    print(f"  - Vehicles: {get_num_vehicles()}")
    print(f"  - Stops: {get_num_stops()}")
    print(f"  - Inspections: {get_num_inspections()}")
    print(f"  - Drivers: {get_num_drivers()}")
    print("🚨 All data has been saved to the respective JSON files.")
