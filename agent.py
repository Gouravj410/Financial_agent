from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agno.agent import Agent
from agno.models.groq import Groq
import uvicorn
import os

# 👉 Put your GROQ API key here
os.environ["GROQ_API_KEY"] = "Enter_Your_GROQ_API_KEY"

app = FastAPI()

# Allow frontend (HTML/JS) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins (you can restrict later)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define AGNO agent with Groq LLaMA-3 model
agent = Agent(
    model=Groq(id="llama3-8b-8192"),  # You can also try "llama3-70b-8192"
    name="AGNO Financial Agent",
    instructions="You are a financial assistant. Help with stocks, companies, and finance in simple words."
)

# Input schema
class Query(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "✅ AGNO Financial Agent is running with Groq LLaMA-3. Use POST /ask to chat."}

@app.post("/ask")
def ask(query: Query):
    try:
        result = agent.run(query.question)

        # ✅ Only return the plain content instead of the full RunResponse object
        if hasattr(result, "content"):
            return {"answer": result.content}
        else:
            return {"answer": str(result)}

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    uvicorn.run("agent:app", host="127.0.0.1", port=8000, reload=True)
