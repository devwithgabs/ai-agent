import os
from google.cloud import bigquery
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

def get_product_categories() -> str:
    """
    Get all product categories and subcategories available in the database.
    
    Returns:
        String with all available product categories and subcategories
    """
    project_id = os.getenv("PROJECT_ID", "adk-demo-469711")
    dataset = os.getenv("DATASET", "mobilis")
    
    client = bigquery.Client(project=project_id)
    
    query = f"""
    SELECT DISTINCT 
        category,
        subcategory,
        COUNT(*) as product_count
    FROM `{project_id}.{dataset}.products`
    WHERE category IS NOT NULL
    GROUP BY category, subcategory
    ORDER BY category, subcategory
    """
    
    try:
        results = client.query(query).result()
        
        if not results.total_rows:
            return "No product categories found in the database."
        
        # Group by category
        categories = {}
        for row in results:
            category = row.category
            subcategory = row.subcategory or "General"
            product_count = row.product_count
            
            if category not in categories:
                categories[category] = []
            categories[category].append(f"  • {subcategory} ({product_count} products)")
        
        # Format output
        category_list = []
        for category, subcategories in categories.items():
            total_products = sum(int(sub.split('(')[1].split(' ')[0]) for sub in subcategories)
            category_list.append(f"**{category}** ({total_products} total products)")
            category_list.extend(subcategories)
            category_list.append("")  # Add spacing
        
        return "Available Product Categories:\n\n" + "\n".join(category_list[:-1])  # Remove last empty line
        
    except Exception as e:
        return f"Error retrieving product categories: {str(e)}"
