from fastapi import FastAPI, HTTPException
from openai import OpenAI
import os
from pydantic import BaseModel
from dotenv import load_dotenv,find_dotenv

#  uvicorn chatting:app --reload
#  pip install fastapi uvicorn openai pydantic
#  uvicorn main:app --reload
#  pip install python-dotenv
#  source venv/Scripts/activate




load_dotenv(find_dotenv())

app = FastAPI()


# Initialize OpenAI client with your API key
# It's best practice to load this from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set.")
client = OpenAI(api_key=openai_api_key)



class ChatRequest(BaseModel):
    message: str
    # Optional: Add a conversation ID for managing history
    conversation_id: str = None 

@app.post("/chat")
async def chat_with_gpt(request: ChatRequest):
    try:
        # Prepare messages for the OpenAI API
        # You might need to retrieve past messages based on conversation_id
        messages = [{"role": "user", "content": request.message}]

            # Make the API call to OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Or your desired model
            messages=messages
        )
            
        # Extract the AI's response
        ai_message = response.choices[0].message.content
        return {"response": ai_message}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
