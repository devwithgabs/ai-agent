# 🏪 Furniture Store Floor Assistance ADK

**Google ADK + MCP Toolbox for Databases + BigQuery**

Transform retail customer service with AI-powered floor assistance that directly queries your BigQuery inventory database in Google Cloud Platform.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup MCP Toolbox
```bash
mkdir mcp-toolbox
cd mcp-toolbox
curl -L https://github.com/google/mcp-toolbox-databases/releases/latest/download/toolbox-linux -o toolbox
chmod +x toolbox
cd ..
```

### 3. Run Everything
```bash
export BIGQUERY_PROJECT=your-project-id

cd mcp-toolbox && ./toolbox --prebuilt bigquery

adk web
```

**Open http://localhost:8080** and start chatting with your furniture store assistant!

## 🎯 What This Does

Your AI agent can answer customer questions like:
- **"I need comfortable kitchen chairs"** → Automatically queries products table
- **"Do you have black bar stools in stock?"** → Checks inventory across all stores
- **"What's available at other locations?"** → Cross-store inventory search
- **"Show me dining tables under $500"** → Price range filtering

The agent writes SQL queries automatically.

## 🏗️ Architecture

```
Customer (Web UI) → ADK Agent → MCP Toolbox → BigQuery (GCP) → Response
```

- **ADK Web Interface**: Clean chat UI for customers/staff
- **Google ADK Agent**: Natural language understanding + automatic SQL generation
- **MCP Toolbox**: Google's pre-built BigQuery tools
- **BigQuery Database**: Your furniture inventory data in Google Cloud

## 📊 Database Structure

Your GCP BigQuery dataset `retail_demo` contains:
- **`products`** - Master catalog (16 items across kitchen, bedroom, living room, office)
- **`stock`** - Real-time inventory across 8 store locations (68 stock records)
- **`stores`** - Store locations in NY area with different types (retail, warehouse, showroom)

## 💡 How It Works

1. **Customer asks**: "Do you have comfortable kitchen chairs in black?"

2. **Agent automatically constructs SQL**:
```sql
SELECT p.product_name, p.base_price, s.available_quantity, s.location_in_store
FROM `your-project.retail_demo.products` p
JOIN `your-project.retail_demo.stock` s ON s.product_id = p.product_id
WHERE LOWER(p.description) LIKE '%comfortable%'
  AND LOWER(p.description) LIKE '%chair%'
  AND LOWER(s.color) = 'black'
  AND s.available_quantity > 0
```

3. **Agent formats response**:
```
🔍 Found Products:
• Modern Comfort Kitchen Chair - $149.99
  Stock: 15 available at Aisle A-1
  Materials: Wood, Fabric | Colors: Black, White, Gray
```

## 📁 Project Structure

```
ai-agent/
├── floor_asistance/agent.py     ← Main ADK agent
├── requirements.txt             ← Python dependencies
└── README.md                    ← This file
```

## 🎪 Demo Scenarios

Try these questions in the web interface:

**Product Search:**
- "Show me all kitchen chairs"
- "I need storage solutions for small kitchens"
- "Do you have extendable dining tables under $600?"

**Inventory Check:**
- "Is the Modern Comfort Chair available in black?"
- "How many bar stools do you have in stock?"
- "What's available at the Manhattan showroom?"

**Cross-Store Search:**
- "If you don't have it here, where else can I find it?"
- "Which stores have the marble dining table?"
- "Show me all locations with office chairs"

## 🏪 Business Value

- **⚡ Staff Training**: New employees provide expert service immediately
- **📈 Sales Growth**: Cross-store inventory visibility prevents lost sales
- **🎯 Customer Satisfaction**: Instant, accurate product information
- **📊 Scalability**: Works for 1 store or 100+ locations
- **🌐 Professional Interface**: Clean web UI for customer interactions
- **☁️ Cloud-Native**: All data securely stored in Google Cloud

## 🎯 Perfect For

- Furniture & Home Goods Stores
- Electronics & Appliance Retailers  
- Fashion & Apparel Chains
- Hardware & Tool Stores
- Any multi-location retail business with inventory

## 🔧 Troubleshooting

**ADK web won't start?**
```bash
cd ai-agent
export BIGQUERY_PROJECT=your-project-id
adk web
```

**Agent can't connect to database?**
- Verify `BIGQUERY_PROJECT` environment variable is set to your GCP project ID
- Ensure MCP Toolbox is running: `cd mcp-toolbox && ./toolbox --prebuilt bigquery`
- Ensure BigQuery dataset `retail_demo` exists in GCP Console

**No query results?**
- Check Google Cloud authentication: `gcloud auth list`
- Test queries directly in BigQuery Console first

**MCP Toolbox connection failed?**
- Toolbox runs on http://127.0.0.1:5000 by default
- Make sure no other service is using port 5000
- Try restarting: `./toolbox --prebuilt bigquery`

## 📞 Next Steps

1. **Customize Data**: Replace retail_demo data with your actual product catalog  
2. **Brand Interface**: Customize ADK web interface with your store's branding
3. **Add More Stores**: Expand your stores table with all locations
4. **Train Staff**: Show team how to use the web interface for customer service
5. **Integrate Systems**: Connect with existing POS and e-commerce platforms

---

**Ready to transform your retail customer experience with Google ADK!** 🚀

*This solution uses Google Cloud Platform and official MCP Toolbox for Databases - enterprise-ready and scalable.*