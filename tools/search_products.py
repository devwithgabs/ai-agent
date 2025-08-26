"""Search for products across all stores."""
import os
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()

def search_products(product_name: str) -> str:
    """
    Search for products across all stores.
    
    Args:
        product_name: Product name to search for
        
    Returns:
        String with product information across all stores
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
        p.subcategory,
        p.brand,
        p.base_price,
        s.available_quantity,
        s.color,
        s.location_in_store
    FROM `{project_id}.{dataset}.stock` s
    JOIN `{project_id}.{dataset}.stores` st ON s.store_id = st.store_id
    JOIN `{project_id}.{dataset}.products` p ON s.product_id = p.product_id
    WHERE LOWER(p.product_name) LIKE LOWER(@product_name)
        AND s.available_quantity > 0
    ORDER BY p.product_name, st.store_name
    LIMIT 50
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("product_name", "STRING", f"%{product_name}%"),
        ]
    )
    
    try:
        results = client.query(query, job_config=job_config).result()
        
        if not results.total_rows:
            return f"No products found matching '{product_name}'"
        
        products_list = []
        for row in results:
            products_list.append(
                f"• Store: {row.store_name} ({row.store_id})\n"
                f"  Address: {row.address}, {row.city}, {row.state} {row.zip_code}\n"
                f"  Phone: {row.phone}\n"
                f"  Product: {row.product_name} ({row.category}, {row.subcategory}, {row.brand})\n"
                f"  Price: ${row.base_price:.2f}\n"
                f"  Available Quantity: {row.available_quantity}\n"
                f"  Color: {row.color}\n"
                f"  Location in Store: {row.location_in_store}\n"
            )
        
        return f"Products matching '{product_name}':\n" + "\n\n".join(products_list)
        
    except Exception as e:
        return f"Error searching products: {str(e)}"