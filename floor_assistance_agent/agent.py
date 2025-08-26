import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from toolbox_core import ToolboxSyncClient

load_dotenv()

project_id = os.getenv('BIGQUERY_PROJECT')
dataset = os.getenv('BIGQUERY_DATASET', 'mobilis')
store_id = os.getenv('STORE_ID')
toolbox_url = os.getenv('TOOLBOX_URL', 'http://127.0.0.1:5000')

# Vertex AI configuration
google_cloud_project = os.getenv('GOOGLE_CLOUD_PROJECT')
google_cloud_location = os.getenv('GOOGLE_CLOUD_LOCATION')

# Ensure ADK / google-genai uses Vertex AI backend when project/location are provided
if google_cloud_project and google_cloud_location:
    os.environ.setdefault('GOOGLE_GENAI_USE_VERTEXAI', 'TRUE')
    os.environ.setdefault('GOOGLE_CLOUD_PROJECT', google_cloud_project)
    os.environ.setdefault('GOOGLE_CLOUD_LOCATION', google_cloud_location)
else:
    # Optional: helpful hint if misconfigured
    print(
        "[WARN] GOOGLE_CLOUD_PROJECT or GOOGLE_CLOUD_LOCATION is not set.\n"
        "ADK will default to Google AI Studio if GOOGLE_API_KEY is configured,\n"
        "or may error if neither Vertex AI nor API key is provided."
    )

if not project_id:
    raise ValueError("BIGQUERY_PROJECT environment variable is required")
if not store_id:
    raise ValueError("STORE_ID environment variable is required")

# Connect to MCP Toolbox
try:
    toolbox_client = ToolboxSyncClient(toolbox_url)
    bigquery_toolset = toolbox_client.load_toolset()
except Exception:
    bigquery_toolset = []

root_agent = Agent(
    name="floor_assistance_agent",
    model="gemini-2.0-flash",
    description="Floor assistance agent for furniture store with BigQuery database access",
    instruction=f"You are a furniture store floor assistant with BigQuery database access. Project: {project_id}, Dataset: {dataset}. You can help customers with inventory across ALL stores, not just store {store_id}. Use the get_store_inventory tool to check stock for any store ID (like '006', '001', etc.). Use check_product_availability to find products across all locations.",
    tools=bigquery_toolset
)
