"""Floor assistance agent for furniture store with BigQuery database access."""
import os
from dotenv import load_dotenv
from google.adk import Agent
from tools.check_our_store_inventory import check_our_store_inventory
from tools.check_product_availability import check_product_availability
from tools.list_store_ids import list_store_ids
from tools.search_products import search_products
from tools.get_our_store_info import get_our_store_info, test_store_exists
from tools.get_product_categories import get_product_categories
from tools.get_brands_and_products import get_brands_and_products
load_dotenv()

def get_analysis_prompt() -> str:
    """Get the instruction prompt for the agent."""
    return """You are a furniture store floor assistant with access to inventory data across all stores.

You are currently working at STORE_001 (Downtown Kitchen Gallery). When customers say "at our store", "our store", "this store", or "here", they are referring to STORE_001.

Key context:
- Our store = STORE_001 (Downtown Kitchen Gallery)
- Use check_our_store_inventory() when customers ask about products "at our store" or "here"
- When products aren't available at our store, suggest alternatives from other locations
- Always be helpful and provide complete information about product availability

Help customers find products and check availability across all store locations."""


def build_agent() -> Agent:
    """Factory for the autoloader in main.py."""
    model = os.getenv("ROOT_AGENT_MODEL", "gemini-2.0-flash")
    return Agent(
        name=os.getenv("AGENT_NAME", "searcher_agent"),
        model=model,
        tools=[
            check_our_store_inventory,
            search_products,
            check_product_availability,
            list_store_ids,
            get_our_store_info,
            test_store_exists,
            get_product_categories,
            get_brands_and_products,
        ],
        instruction=get_analysis_prompt(),
    )


# Expose both patterns the autoloader might look for
root_agent = build_agent()
