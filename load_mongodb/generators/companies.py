# generators/companies.py

import random
import logging
from utils import append_jsonl
from paths import COMPANIES_OUTPUT_FILE
from generators.zones import get_num_zones

# logger = logging.getLogger("companies")
# handler = logging.FileHandler("logs/companies.log")
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# handler.setFormatter(formatter)
# logger.addHandler(handler)
# logger.setLevel(logging.INFO)

# Create a logger
logger = logging.getLogger("companies")
logger.setLevel(logging.DEBUG)

# Create file handler
file_handler = logging.FileHandler("logs/companies.log")
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
file_handler.setLevel(logging.DEBUG) # Capture everything to file

# Create console handler (for terminal output)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
console_handler.setLevel(logging.INFO)

# Add both handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Now log something
logger.debug("Companies generation started.")

num_companies = 0

REGIONS = [
    "North-East USA", "Midwest USA", "West Coast USA",
    "South-East USA", "Southwest USA", "Pacific Northwest",
    "Mountain States", "Great Plains", "Mid-Atlantic", "New England"
]

def get_num_companies():
    global num_companies
    return num_companies

def generate_companies(num_new):

    logger.debug(f"Number of zones: {get_num_zones()}")

    logger.info(f"🏢 Adding {num_new} new logistics companies...")

    for i in range(num_new):
        global num_companies
        num_companies += 1
        new_company = generate_company(num_companies, get_num_zones())
        append_jsonl(COMPANIES_OUTPUT_FILE, new_company)
        logger.info(f"  ➤ Created {new_company['_id']}: {new_company['name']} in {new_company['region']}, Zones: {new_company['active_zones']}")
        
    logger.info(f"✅ Saved updated company list to {COMPANIES_OUTPUT_FILE} (Total: {num_companies})")

def generate_company(company_id_num, available_zones):
    company_id = f"company_{company_id_num:03}"
    name = f"Company {company_id_num}"
    region = REGIONS[(company_id_num - 1) % len(REGIONS)]

    num_assigned_zones = random.randint(1, min(5, available_zones))
    assigned_zone_ids = [f"zone_{z:05}" for z in random.sample(range(1, get_num_zones() + 1), k=num_assigned_zones)]


    return {
        "_id": company_id,
        "name": name,
        "region": region,
        "fleet": [],
        "drivers": [],
        "active_zones": assigned_zone_ids
    }