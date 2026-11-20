import os
import random
from typing import List, Dict, Any
from dotenv import load_dotenv
from faker import Faker
import psycopg2
from psycopg2.extras import execute_values

# Load environment variables from .env file into memory before opening connections
load_dotenv() 
fake = Faker("en_US")

STATUSES = ["CREATED", "IN_TRANSIT", "DELIVERED", "RETURNED"]

VALID_WAREHOUSE_IDS = [1, 2, 3, 4]

def generate_shipment_batch(batch_size: int = 100) -> List[Dict[str, Any]]:
    """
    Generate a batch of synthetic shipment records matching the target schema.
    
    Args:
        batch_size: Number of dictionary records to create.
        
    Returns:
        List of dictionaries where each dictionary represents a single row.
    """
    batch =[]
    for _ in range(batch_size):
        record = {
            "warehouse_id": random.choice(VALID_WAREHOUSE_IDS),
            "recipient_name": fake.name(),
            # Clamping delivery package weight to typical courier limits (0.5 to 35.0 kg)
            "weight_kg": round(random.uniform(0.5, 35.0), 2),
            "cost": round(random.uniform(10.0, 300.0), 2),
            "status": random.choice(STATUSES),
        }
        batch.append(record)
    return batch

def insert_shipments(shipments: List[Dict[str, Any]]) -> None:
    """
    Bulk-insert generated shipment dictionaries into the PostgreSQL database.
    
    Args:
        shipments: List of shipment records to be persisted.
    """
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL variable is missing from the environment.")

    records_to_insert = [
        (
            item["warehouse_id"],
            item["recipient_name"],
            item["weight_kg"],
            item["cost"],
            item["status"],
        )
        for item in shipments
    ]

    query = """
        INSERT INTO shipments (warehouse_id, recipient_name, weight_kg, cost, status)
        VALUES %s;
    """
    with psycopg2.connect(db_url) as conn:
        with conn.cursor() as cur:
            execute_values(cur, query, records_to_insert)

    print(f"Successfully loaded {len(records_to_insert)} records into NeonDB.")

if __name__=="__main__":
    test_batch = generate_shipment_batch(batch_size = 100)
    insert_shipments(test_batch)
    
