"""Check product availability across all stores."""
import os
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()

def check_product_availability(product_name: str) -> str:
    """
    Check product availability across all stores.
    
    Args:
        product_name: Product name to check availability for
        
    Returns:
        String with availability information across all stores
    """
    project_id = os.getenv("BIGQUERY_PROJECT", "adk-demo-469711")
    dataset = os.getenv("BIGQUERY_DATASET", "mobilis")
    
    client = bigquery.Client(project=project_id)
    
    query = f"""
    SELECT 
        st.store_name,
        st.store_id,
        st.address,
        st.city,
        st.state,
        st.zip_code,
        st.phone,
        p.product_name,
        p.category,
        p.base_price,
        s.color,
        s.available_quantity,
        s.location_in_store
    FROM `{project_id}.{dataset}.stock` s
    JOIN `{project_id}.{dataset}.stores` st ON s.store_id = st.store_id
    JOIN `{project_id}.{dataset}.products` p ON s.product_id = p.product_id
    WHERE LOWER(p.product_name) LIKE LOWER(@product_name)
        AND s.available_quantity > 0
    ORDER BY st.store_name, p.product_name
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("product_name", "STRING", f"%{product_name}%"),
        ]
    )
    
    try:
        results = client.query(query, job_config=job_config).result()
        
        if not results.total_rows:
            return f"No available stock found for products matching '{product_name}'"
        
        availability_list = []
        for row in results:
            availability_list.append(
                f"• {row.store_name} (Store {row.store_id}): {row.product_name} - {row.available_quantity} available, ${row.base_price:.2f}"
                + (f" - {row.color}" if row.color else "")
            )
        
        return f"Product availability for '{product_name}':\n" + "\n".join(availability_list)
        
    except Exception as e:
        return f"Error checking product availability: {str(e)}"
