# https://dashboard.cohere.com/api-keys
# Basic Text Generation (Using cohere Python SDK):
import cohere
from dotenv import load_dotenv
import os

load_dotenv() # Load variables from .env file
API_TOKEN = os.getenv('COHERE_TOKEN') # cohere api_keys
def CallCohereAPI(prompt):
    # Initialize client (replace with your API key)
    # print(API_TOKEN)
    co = cohere.Client(API_TOKEN)  # Free tier key 

    # Generate text using Cohere's 'command' model
    response = co.generate(
        model="command",  # Free model
        prompt=prompt,
        max_tokens=100,
        temperature=0.7,
        stop_sequences=[]           # Optional: add if you want to control where generation stops
    )
    return response.generations[0].text.strip()

# res = CallCohereAPI("Who won IPL 2022?")
# print(res)
# print(response.generations[0].text)
# print("🤖 AI Response:\n", response.generations[0].text.strip())
