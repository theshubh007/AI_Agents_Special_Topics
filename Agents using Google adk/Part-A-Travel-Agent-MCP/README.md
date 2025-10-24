# 🏨 Travel(Hotel Search) Agent with ADK and MCP Toolbox for Databases

## 🎯 Project Goal

This repository demonstrates the architecture and implementation of a production-grade, data-grounded AI hotel search agent using Google's Agent Development Kit (ADK) and the Model Context Protocol (MCP) Toolbox for Databases. The agent handles hotel-related queries by securely connecting to and querying a managed PostgreSQL database (Cloud SQL).

The implementation showcases how MCP acts as a crucial intermediary between the LLM and the database, providing secure, parameterized SQL execution while shielding the raw database connection from direct LLM access.

## 📹 Video Demonstration
https://youtu.be/3AcKGGuLYLw

## 🏗️ Architecture Overview

The system operates across three secure and distinct layers:

### 1. Database Layer (Cloud SQL)

The immutable source of truth for hotel data:

- PostgreSQL database storing hotel information
- Schema includes: name, location, price_tier, booking status
- Managed Cloud SQL instance for reliability and security

### 2. Toolbox Layer (MCP Toolbox for Databases)

A crucial intermediary service that:

- Provides secure, parameterized SQL execution
- Defines database queries as tools via `tools.yaml`
- Shields raw database connection from the LLM
- Translates natural language requests into structured SQL queries
- Prevents SQL injection and unauthorized access

### 3. Agent Layer (ADK)

The application hosting the Gemini model:

- Acts as a reasoning engine
- Decides when to invoke database queries
- Interprets user questions about hotels
- Generates natural language responses grounded in database results

## 📋 Implementation Phases

### Phase 1: Infrastructure Setup (Cloud SQL)

**Database Provisioning:**

- Create Cloud SQL PostgreSQL instance (`hoteldb-instance`)
- Configure network access and authentication
- Enable necessary Google Cloud APIs

**Database Schema:**

```sql
CREATE TABLE hotels (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    location VARCHAR(255),
    price_tier VARCHAR(50),
    booking_status VARCHAR(50)
);
```

**Sample Data:**

```sql
INSERT INTO hotels (name, location, price_tier, booking_status) VALUES
    ('Grand Plaza Hotel', 'New York', 'Luxury', 'Available'),
    ('Budget Inn', 'Los Angeles', 'Economy', 'Available'),
    ('Seaside Resort', 'Miami', 'Midscale', 'Booked');
```

### Phase 2: MCP Toolbox Configuration

The MCP Toolbox defines database queries as tools through `tools.yaml`:

```yaml
sources:
  my-cloud-sql-source:
    kind: cloud-sql-postgres
    # Connection details (project, instance, user, password)

tools:
  search-hotels-by-name:
    description: Search for hotels based on name
    statement: SELECT * FROM hotels WHERE name ILIKE '%' || $1 || '%';

  search-hotels-by-location:
    description: Search for hotels based on location, sorted by price
    statement: |
      SELECT * FROM hotels WHERE location ILIKE '%' || $1 || '%'
      ORDER BY CASE price_tier
        WHEN 'Economy' THEN 1
        WHEN 'Midscale' THEN 2
        WHEN 'Luxury' THEN 3
      END;

toolsets:
  my_first_toolset:
    - search-hotels-by-name
    - search-hotels-by-location
```

**Key Configuration Elements:**

- Database source connection definition
- Parameterized SQL statements ($1, $2, etc.)
- Tool descriptions for LLM understanding
- Toolset grouping for agent consumption
- SQL injection prevention through parameterization

### Phase 3: Agent Development (ADK Integration)

The Agent connects to the MCP Toolbox server and loads the defined toolset:

```python
from google.adk.agents import Agent
from toolbox_core import ToolboxSyncClient

# Initialize client to connect to the running MCP Toolbox server
toolbox = ToolboxSyncClient("http://127.0.0.1:5000")

# Load the entire toolset
tools = toolbox.load_toolset('my_first_toolset')

hotel_agent = Agent(
    model='gemini-2.5-flash',
    name='hotel_agent',
    description='Agent to answer questions about hotels in a city or by name',
    instruction='You are a helpful agent who must use the tools to answer user questions about hotels',
    tools=tools  # MCP tools loaded from toolbox
)
```

**Agent Capabilities:**

- Natural language query understanding
- Intelligent tool selection (by name vs by location)
- Database query execution via MCP
- Result interpretation and response generation

### Phase 4: Testing and Deployment

**Local Testing:**

1. Start MCP Toolbox server: `./toolbox --tools_file "tools.yaml"`
2. Run the agent: `adk run`
3. Test queries:
   - "Find hotels in New York"
   - "Show me the Grand Plaza Hotel"
   - "What hotels are available in Miami?"

**Cloud Deployment (Optional):**

1. Deploy MCP Toolbox to Cloud Run for external URL
2. Update agent to use Cloud Run endpoint
3. Deploy agent application: `adk deploy cloud_run`


## 🚀 Usage Examples

The hotel agent can handle various queries:

**Search by Location:**

```
"Find hotels in New York"
→ Agent invokes search-hotels-by-location with parameter "New York"
→ Returns hotels sorted by price tier (Economy → Midscale → Luxury)
```

**Search by Name:**

```
"Show me the Grand Plaza Hotel"
→ Agent invokes search-hotels-by-name with parameter "Grand Plaza"
→ Returns matching hotel details
```

**Availability Queries:**

```
"What hotels are available in Miami?"
→ Agent invokes search-hotels-by-location with parameter "Miami"
→ Filters results to show only available hotels
```

## 🔄 Interaction Flow

1. **User Query** → Natural language hotel search request
2. **LLM Analysis** → Agent determines which tool to invoke (by name or location)
3. **Tool Call Generation** → Agent generates parameterized tool call
4. **MCP Execution** → Toolbox executes SQL query against Cloud SQL
5. **Database Results** → Structured hotel data returned
6. **Response Generation** → LLM synthesizes natural language response
7. **User Response** → Grounded answer based on actual database records

## 🔑 Key Concepts

### MCP as Database Security Layer

- Prevents direct SQL access from LLM
- Enforces parameterized queries (prevents SQL injection)
- Provides audit trail for database operations
- Shields connection credentials from agent code

### Tool Selection Intelligence

- Agent chooses between search-by-name vs search-by-location
- Natural language understanding determines appropriate tool
- Parameterized queries ensure safe execution

### Grounded Database Responses

- All hotel information comes from actual database records
- No hallucination of hotel names, locations, or availability
- Transparent about data source (Cloud SQL database)

## 🔗 Learning Resources

- **Original Codelab:** https://codelabs.developers.google.com/travel-agent-mcp-toolbox-adk#0
- **MCP Documentation:** https://modelcontextprotocol.io/
- **ADK Documentation:** https://developers.google.com/adk

## 🧹 Cleanup

Always clean up Google Cloud resources to manage costs:

- Delete Cloud SQL instance (`hoteldb-instance`)
- Remove Cloud Run services (if deployed)
- Disable unused APIs

## 💡 Key Takeaways

1. **Three-layer architecture** - Clear separation between database, toolbox, and agent
2. **MCP for database security** - Parameterized SQL execution prevents injection attacks
3. **Tool-first design** - SQL queries defined as tools improve reliability
4. **Production-ready patterns** - Cloud SQL + MCP + ADK for scalable deployment
5. **Grounded intelligence** - LLM reasoning combined with factual database queries
