"""Check inventory for our specific store."""
import os
from typing import Optional
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()

def check_our_store_inventory(product_name: Optional[str] = None, color: Optional[str] = None, material: Optional[str] = None) -> str:
    """
    Check inventory for our specific store.
    
    Args:
        product_name: Optional product name to filter by
        color: Optional color to filter by
        material: Optional material to filter by
        
    Returns:
        String with inventory information for our store
    """
    project_id = os.getenv("BIGQUERY_PROJECT", "adk-demo-469711")
    dataset = os.getenv("BIGQUERY_DATASET", "mobilis")
    store_id = os.getenv("STORE_ID", "STORE_001")
    
    client = bigquery.Client(project=project_id)
    
    query_parameters = [
        bigquery.ScalarQueryParameter("store_id", "STRING", store_id),
    ]
    
    conditions = [
        f"s.store_id = @store_id",
        "s.available_quantity > 0",
    ]
    
    if product_name:
        query_parameters.append(bigquery.ScalarQueryParameter("product_name", "STRING", f"%{product_name}%"))
        conditions.append(f"LOWER(p.product_name) LIKE LOWER(@product_name)")
    
    if color:
        query_parameters.append(bigquery.ScalarQueryParameter("color", "STRING", f"%{color}%"))
        conditions.append(f"s.color LIKE @color")
    
    if material:
        query_parameters.append(bigquery.ScalarQueryParameter("material", "STRING", f"%{material}%"))
        conditions.append(f"p.materials LIKE @material")
    
    query = f"""
    SELECT 
        st.store_name,
        st.store_id,
        p.product_name,
        p.category,
        p.subcategory,
        p.brand,
        p.description,
        p.base_price,
        p.materials,
        p.colors_available,
        p.warranty_months,
        s.color,
        s.available_quantity,
        s.location_in_store
    FROM `{project_id}.{dataset}.stock` s
    JOIN `{project_id}.{dataset}.stores` st ON s.store_id = st.store_id
    JOIN `{project_id}.{dataset}.products` p ON s.product_id = p.product_id
    WHERE {" AND ".join(conditions)}
    ORDER BY p.category, p.product_name
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=query_parameters
    )
    
    try:
        results = client.query(query, job_config=job_config).result()
        
        if not results.total_rows:
            # If no items found in our store, check other stores
            if product_name or color or material:
                # Build WHERE conditions for other stores search
                other_where_conditions = ["s.store_id != @store_id", "s.available_quantity > 0"]
                other_query_params = [bigquery.ScalarQueryParameter("store_id", "STRING", store_id)]
                
                if product_name:
                    other_where_conditions.append("LOWER(p.product_name) LIKE LOWER(@product_name)")
                    other_query_params.append(bigquery.ScalarQueryParameter("product_name", "STRING", f"%{product_name}%"))
                
                if color:
                    other_where_conditions.append("(LOWER(s.color) LIKE LOWER(@color) OR LOWER(p.colors_available) LIKE LOWER(@color))")
                    other_query_params.append(bigquery.ScalarQueryParameter("color", "STRING", f"%{color}%"))
                
                if material:
                    other_where_conditions.append("LOWER(p.materials) LIKE LOWER(@material)")
                    other_query_params.append(bigquery.ScalarQueryParameter("material", "STRING", f"%{material}%"))
                
                other_where_clause = " AND ".join(other_where_conditions)
                
                # Search for the product in other stores
                other_stores_query = f"""
                SELECT 
                    st.store_name,
                    st.store_id,
                    st.address,
                    st.city,
                    st.state,
                    st.zip_code,
                    st.phone
                FROM `{project_id}.{dataset}.stock` s
                JOIN `{project_id}.{dataset}.stores` st ON s.store_id = st.store_id
                JOIN `{project_id}.{dataset}.products` p ON s.product_id = p.product_id
                WHERE {other_where_clause}
                ORDER BY st.store_name
                LIMIT 5
                """
                
                other_stores_config = bigquery.QueryJobConfig(query_parameters=other_query_params)
                
                other_results = client.query(other_stores_query, other_stores_config).result()
                
                if other_results.total_rows > 0:
                    suggestions = []
                    for row in other_results:
                        store_info = f"• {row.store_name} (Store {row.store_id}): {row.address}, {row.city}, {row.state} {row.zip_code}, Phone: {row.phone}"
                        suggestions.append(store_info)
                    
                    search_criteria = []
                    if product_name:
                        search_criteria.append(f"'{product_name}'")
                    if color:
                        search_criteria.append(f"color '{color}'")
                    if material:
                        search_criteria.append(f"material '{material}'")
                    
                    criteria_text = " with " + " and ".join(search_criteria) if search_criteria else ""
                    
                    return f"Sorry, we don't have items{criteria_text} in stock at our store (Downtown Kitchen Gallery).\n\nHowever, I found these options at other locations:\n\n" + "\n\n".join(suggestions)
                else:
                    search_criteria = []
                    if product_name:
                        search_criteria.append(f"'{product_name}'")
                    if color:
                        search_criteria.append(f"color '{color}'")
                    if material:
                        search_criteria.append(f"material '{material}'")
                    
                    criteria_text = " with " + " and ".join(search_criteria) if search_criteria else ""
                    return f"Sorry, we don't have items{criteria_text} in stock at our store, and they're not available at other locations either."
            else:
                return f"No inventory found for store {store_id}"
        
        inventory_list = []
        store_name = None
        for row in results:
            if store_name is None:
                store_name = row.store_name
            inventory_list.append(
                f"• {row.product_name} ({row.category} - {row.subcategory}): {row.description}\n"
                + f"  - Brand: {row.brand}\n"
                + f"  - Materials: {row.materials}\n"
                + f"  - Colors Available: {row.colors_available}\n"
                + f"  - Color: {row.color}\n"
                + f"  - Available Quantity: {row.available_quantity}\n"
                + f"  - Location in Store: {row.location_in_store}\n"
                + f"  - Base Price: ${row.base_price:.2f}"
            )
        
        return f"Inventory for {store_name} (Store {store_id}):\n" + "\n".join(inventory_list)
        
    except Exception as e:
        return f"Error checking inventory: {str(e)}"
