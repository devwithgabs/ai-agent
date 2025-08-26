"""Get information about our specific store."""
import os
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()

def test_store_exists() -> str:
    """Test if our store ID exists in the database."""
    project_id = os.getenv("BIGQUERY_PROJECT", "adk-demo-469711")
    dataset = os.getenv("BIGQUERY_DATASET", "mobilis")
    store_id = os.getenv("STORE_ID", "STORE_001")
    
    client = bigquery.Client(project=project_id)
    
    try:
        # Test 1: Check if any stores exist
        query1 = f"SELECT COUNT(*) as total FROM `{project_id}.{dataset}.stores`"
        results1 = client.query(query1).result()
        total_stores = list(results1)[0].total
        
        # Test 2: List first 5 store IDs
        query2 = f"SELECT store_id FROM `{project_id}.{dataset}.stores` LIMIT 5"
        results2 = client.query(query2).result()
        existing_stores = [row.store_id for row in results2]
        
        # Test 3: Check if our specific store exists
        query3 = f"SELECT COUNT(*) as found FROM `{project_id}.{dataset}.stores` WHERE store_id = '{store_id}'"
        results3 = client.query(query3).result()
        store_found = list(results3)[0].found
        
        return f"""Store Test Results:
• Total stores in database: {total_stores}
• Sample store IDs: {existing_stores}
• Looking for store: {store_id}
• Store found: {'YES' if store_found > 0 else 'NO'}"""
        
    except Exception as e:
        return f"Error testing store: {str(e)}"


def get_our_store_info() -> str:
    """
    Get information about our specific store.
    
    Returns:
        String with store information
    """
    project_id = os.getenv("BIGQUERY_PROJECT", "adk-demo-469711")
    dataset = os.getenv("BIGQUERY_DATASET", "mobilis")
    store_id = os.getenv("STORE_ID", "STORE_001")
    
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
    WHERE store_id = @store_id
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("store_id", "STRING", store_id),
        ]
    )
    
    try:
        results = client.query(query, job_config=job_config).result()
        
        for row in results:
            return f"""Store {row.store_id} Information:
• Store Name: {row.store_name}
• Address: {row.address}
• City: {row.city}
• State: {row.state}
• Zip Code: {row.zip_code}
• Phone: {row.phone or 'N/A'}
• Manager: {row.manager or 'N/A'}
• Store Type: {row.store_type or 'N/A'}"""
        
        return f"No store found with ID {store_id}"
        
    except Exception as e:
        return f"Error getting store info: {str(e)}"
