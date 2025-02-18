import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

# class CustomAssistant(AssistantAgent):
#     def process_response(self, response: str) -> str:
#         if "<|answer|>" in response:
#             return response.split("<|answer|>")[1].split("</answer>")[0].strip()
#         return response
    
class CustomAssistant(AssistantAgent):
    def process_response(self, response: str) -> str:
        if "</think>" in response:
            return response.split("</think>")[1].strip()
        return response

model_client = OpenAIChatCompletionClient(
    model="deepseek-r1:7b",
    base_url="http://localhost:11434/v1",
    api_key="placeholder",
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": "deepseek",
    },
    temperature=0.3,  # Reduce randomness
)

async def get_weather(city: str) -> str:
    """Get current weather for a city. Args: city (str). Returns: str."""
    return f"Weather in {city}: 73°F, Sunny"

agent = CustomAssistant(
    name="weather_agent",
    model_client=model_client,
    tools=[get_weather],
    system_message="""You are a helpful assistant. ALWAYS use tools when answering questions.
    Available tools: get_weather(city: str) -> str. Use get_weather for weather-related queries.""",
    reflect_on_tool_use=True,
)

async def main() -> None:
    # task = """What's New York's weather? Format response:
    # <|thinking|>...<|/thinking|>
    # <|answer|>...<|/answer|>"""
    task = "What's the weather in New York?"
    
    await Console(agent.run_stream(task=task))

asyncio.run(main())