import os
from google.cloud import bigquery
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

def get_brands_and_products() -> str:
    """
    Get all brands and their associated products from the database.
    
    Returns:
        String with all brands and their products grouped by brand
    """
    project_id = os.getenv("PROJECT_ID", "adk-demo-469711")
    dataset = os.getenv("DATASET", "mobilis")
    
    client = bigquery.Client(project=project_id)
    
    query = f"""
    SELECT 
        brand,
        product_name,
        category,
        subcategory,
        base_price
    FROM `{project_id}.{dataset}.products`
    WHERE brand IS NOT NULL
    ORDER BY brand, product_name
    """
    
    try:
        results = client.query(query).result()
        
        if not results.total_rows:
            return "No brands found in the database."
        
        # Group products by brand
        brands = {}
        for row in results:
            brand = row.brand
            product_info = {
                'name': row.product_name,
                'category': row.category,
                'subcategory': row.subcategory,
                'price': row.base_price
            }
            
            if brand not in brands:
                brands[brand] = []
            brands[brand].append(product_info)
        
        # Format output
        brand_list = []
        for brand, products in brands.items():
            brand_list.append(f"**{brand}** ({len(products)} products)")
            
            for product in products:
                product_line = f"  • {product['name']} ({product['category']}"
                if product['subcategory']:
                    product_line += f" - {product['subcategory']}"
                product_line += f") - ${product['price']:.2f}"
                brand_list.append(product_line)
            
            brand_list.append("")  # Add spacing between brands
        
        return "Available Brands and Their Products:\n\n" + "\n".join(brand_list[:-1])  # Remove last empty line
        
    except Exception as e:
        return f"Error retrieving brands and products: {str(e)}"
