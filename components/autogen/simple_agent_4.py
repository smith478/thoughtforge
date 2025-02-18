import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Set up the model client
model_client = OpenAIChatCompletionClient(
    model="llama3.2:latest",
    base_url="http://localhost:11434/v1",
    api_key="placeholder",
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": False,
        "family": "llama",
    },
)

# Define a tool
async def get_weather(city: str) -> str:
    """Get the weather for a given city."""
    return f"The weather in {city} is 73°F and Sunny."

# Create the assistant agent
agent = AssistantAgent(
    name="weather_agent",
    model_client=model_client,
    tools=[get_weather],
    system_message="You are a helpful assistant. Use tools when needed.",
)

# Run the agent
async def main() -> None:
    await Console(agent.run_stream(task="What is the weather in New York? Use the `get_weather` tool."))

asyncio.run(main())