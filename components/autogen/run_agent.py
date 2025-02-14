local_llm_config = {
    "config_list": [
        {
            "model": "NotRequired",      # Model is loaded by Ollama
            "api_key": "NotRequired",    # No API key needed for local use
            "base_url": "http://host.docker.internal:4000",  # Use this on macOS/Windows
            "price": [0, 0],             # Set token pricing to zero for local inference
        }
    ],
    "cache_seed": None,
}

# Initialize your literature review agent with this configuration
from autogen import ConversableAgent, UserProxyAgent
assistant = ConversableAgent("assistant", llm_config=local_llm_config)
user_proxy = UserProxyAgent("user", code_execution_config=False)

# Start the conversation (or your literature review task)
res = assistant.initiate_chat(user_proxy, message="Please start the literature review on topic X")
print(assistant)
