from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

# Configuration for Ollama
config_list = [
    {
        "model": "qwen2.5:latest",
        "base_url": "http://localhost:11434/v1/",
        "api_key": "ollama", 
    }
]

# Create agents
assistant = AssistantAgent(
    name="assistant",
    llm_config={
        "config_list": config_list,
        "temperature": 0.6,
    }
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="ALWAYS",
    code_execution_config={"work_dir": "coding"},
)

# Start conversation
user_proxy.initiate_chat(
    assistant,
    message="Write a Python function to calculate Fibonacci numbers up to n and explain it."
)