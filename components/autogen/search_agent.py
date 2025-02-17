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
TASK_2 = "Execute code to fetch a list of the top 10 to 20 papers that are most relevant to the question."
TASK_3 = f"Sythesize the information from the papers and provide an answer to: {CLINICAL_QUESTION}. Provide references (as links) from the papers."
TASK_4 = """Reflect on the sequence and create a recipe containing all of the steps necessary and name for it. Suggest well-documented, generalized Python function(s) to perform similar tasks for coding steps in the future. Make sure coding and non-coding steps are never mixed in one function. In the docstring of the function(s), clarify what non-coding steps are needed to use the language skill of the assistant."""

# Start looking for research papers
user_proxy.initiate_chat(
    assistant,
    message=TASK_1
)

# Execute code to fetch the top 10 to 20 papers
user_proxy.initiate_chat(
    assistant,
    message=TASK_2,
    clear_history=False
)

# Answer the clinical question with references
user_proxy.initiate_chat(
    assistant,
    message=TASK_3,
    clear_history=False
)