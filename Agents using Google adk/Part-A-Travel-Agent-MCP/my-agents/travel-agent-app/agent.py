from google.adk.agents import Agent
from toolbox_core import ToolboxSyncClient


# Initialize client to connect to the running MCP Toolbox server
# The toolbox server must be running separately with: ./toolbox --tools_file "tools.yaml"
toolbox = ToolboxSyncClient("http://127.0.0.1:5000")

# Load the entire toolset defined in tools.yaml
# This includes search-hotels-by-name and search-hotels-by-location
tools = toolbox.load_toolset('my_first_toolset')

# Create the hotel agent with MCP database tools
hotel_agent = Agent(
    model='gemini-2.5-flash',
    name='hotel_agent',
    description='Agent to answer questions about hotels in a city or by name.',
    instruction=(
        'You are a helpful agent who must use the tools to answer user questions about hotels. '
        'Use search-hotels-by-name when the user asks about a specific hotel name. '
        'Use search-hotels-by-location when the user asks about hotels in a city or location. '
        'Always provide clear, helpful responses based on the database results.'
    ),
    tools=tools  # MCP tools loaded from toolbox
)


if __name__ == '__main__':
    # Example usage
    print("Hotel Agent initialized successfully!")
    print("\nMake sure the MCP Toolbox server is running:")
    print("  ./toolbox --tools_file 'tools.yaml'")
    print("\nExample queries:")
    print("- 'Find hotels in New York'")
    print("- 'Show me the Grand Plaza Hotel'")
    print("- 'What hotels are available in Miami?'")
    print("- 'Are there any luxury hotels in Los Angeles?'")
