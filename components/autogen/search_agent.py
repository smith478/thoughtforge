from autogen import AssistantAgent, UserProxyAgent

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
        "seed": 42,
        "config_list": config_list,
        "temperature": 0.4,
    },
    is_termination_msg=lambda x: True if "TERMINATE" in x.get("content") else False,
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: True if "TERMINATE" in x.get("content") else False,
    max_consecutive_auto_reply=10,
    human_input_mode="NEVER",
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,
    },
)

CLINICAL_QUESTION = "What is the prognosis for hemangiosaracoma in dogs?"
TASK_1 = f"Find research papers to help answer the following question: {CLINICAL_QUESTION}"

# Start conversation
user_proxy.initiate_chat(
    assistant,
    message=TASK_1
)