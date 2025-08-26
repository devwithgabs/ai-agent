"""List all available store IDs."""
import os
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()

def list_store_ids() -> str:
    """
    List all available store IDs.
    
    Returns:
        String with all available store IDs and their information
    """
    project_id = os.getenv("BIGQUERY_PROJECT", "adk-demo-469711")
    dataset = os.getenv("BIGQUERY_DATASET", "mobilis")
    
    client = bigquery.Client(project=project_id)
    
    query = f"""
    SELECT 
        store_id,
        store_name,
        address,
        city,
        state,
        zip_code,
        phone,
        manager,
        store_type
    FROM `{project_id}.{dataset}.stores`
    ORDER BY store_id
    """
    
    try:
        results = client.query(query).result()
        
        if not results.total_rows:
            return "No stores found in the database"
        
        store_list = []
        for row in results:
            store_list.append(f"• {row.store_id}: {row.store_name} - {row.city}\n"
                              f"  Address: {row.address}\n"
                              f"  State: {row.state}\n"
                              f"  Zip Code: {row.zip_code}\n"
                              f"  Phone: {row.phone}\n"
                              f"  Manager: {row.manager}\n"
                              f"  Store Type: {row.store_type}\n")
        
        return f"Available stores:\n" + "\n".join(store_list)
        
    except Exception as e:
        return f"Error listing store IDs: {str(e)}"