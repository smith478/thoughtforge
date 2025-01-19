from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from litellm import completion
import torch
import os

app = FastAPI()

MODEL_PATH = "/models/qwen"

# Verify CUDA is available
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"Using GPU: {torch.cuda.get_device_name(0)}")

print(f"Loading model from: {MODEL_PATH}")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "gpu": torch.cuda.is_available(),
        "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "None",
        "model_path": MODEL_PATH
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        response = completion(
            # TODO correct this model name
            model="qwen/Qwen1.5-7B-Chat",
            messages=[{"role": "user", "content": request.message}],
            temperature=0.7,
            max_tokens=150,
            gpu_device_id=0,
            model_path=MODEL_PATH
        )
        return ChatResponse(response=response.choices[0].message.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)