import gradio as gr
import requests
import ollama
def search_web(query: str) -> list:
    SEARXNG_URL = "http://localhost:4000/search"
    params = {'q': query, 'format': 'json'}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    response = requests.get(SEARXNG_URL, params=params, headers=headers)
    if response.status_code != 200:
        print("Response status code:", response.status_code)
        print("Response text:", response.text)
        raise Exception(f"Search query failed with status code {response.status_code}")
    return response.json().get("results", [])
def chat_with_search(query: str, use_web_search: bool):
    # Optionally integrate web search based on user toggle
    if use_web_search:
        results = search_web(query)
        context_str = format_search_results(results, max_results=5)
    else:
        context_str = "No additional context provided."
return generate_augmented_response(query, context_str)
def format_search_results(results: list, max_results: int = 5) -> str:
    """
    Format the top search results into a context string.
    """
    formatted = []
    for result in results[:max_results]:
        title = result.get("title", "No title")
        url = result.get("url", "No URL")
        snippet = result.get("content", "No snippet")
        formatted.append(f"Title: {title}\nURL: {url}\nSnippet: {snippet}")
    return "\n\n".join(formatted)
def generate_augmented_response(query: str, context: str) -> str:
    """
    Combine the user's query with the search context and send it to DeepSeek R1 via Ollama.
    """
    # Create a composite prompt
    composite_prompt = f"""
{context}
Please use the following web search results to provide the detailed summary of the request above.
{query}
Answer:"""
    response = ollama.chat(
        model="deepseek-r1:14b",
        messages=[
            {"role": "user", "content": composite_prompt}
        ]
    )
    return response["message"]["content"]
iface = gr.Interface(
    fn=chat_with_search,
    inputs=[
        gr.Textbox(label="Your Query"),
        gr.Checkbox(label="Enable Web Search", value=True)
    ],
    outputs="text",
    title="DeepSeek R1 with Web Search",
    description="Ask questions and get answers augmented with real-time web search results."
)
iface.launch()