from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import uvicorn

# Import the LangGraph agent
from agent import graph

app = FastAPI(
    title="Vinmec Chatbot API",
    description="Backend API for Vinmec Medical Assistant",
    version="1.0.0"
)

# In-memory dictionary to store session histories
# Note: In a production environment, you should use a database (e.g., Redis, PostgreSQL) instead of in-memory store.
sessions: Dict[str, List] = {}

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    session_id: str
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Retrieve conversation history for the session
        history = sessions.get(request.session_id, [])
        
        # Append the new user message
        history.append(("human", request.message))
        
        # Keep only the last 4 messages to prevent context overflow
        # (similar to the CLI loop in agent.py)
        if len(history) > 4:
            history = history[-4:]
            
        print(f"Processing message for session: {request.session_id}")
        
        # Invoke LangGraph
        result = graph.invoke({"messages": history})
        
        # The result["messages"] contains the entire updated conversation history
        updated_history = result["messages"]
        sessions[request.session_id] = updated_history
        
        # Extract the assistant's response from the last message
        final_message = updated_history[-1]
        
        return ChatResponse(
            session_id=request.session_id,
            response=final_message.content
        )
        
    except Exception as e:
        print(f"Error processing chat: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    """Endpoint for health check"""
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
