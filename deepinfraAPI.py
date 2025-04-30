
# https://deepinfra.com/dash/api_keys
import requests
from dotenv import load_dotenv
import os

load_dotenv() # Load variables from .env file
API_TOKEN = os.getenv('DI_TOKEN') # deepinfra api_keys
# print(API_TOKEN)
def CallDeepInfraAPI(qry):
    API_URL = "https://api.deepinfra.com/v1/inference/meta-llama/Meta-Llama-3-8B-Instruct"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    # qry = "who is current PM of india?"
    data = {
        "input": "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n" + qry + "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
        "stop": ["<|eot_id|>"],
        "stream": False
    }
    response = requests.post(API_URL, headers=headers, json=data)
    generated_text = ''
    if response.status_code == 200:
        response_json = response.json()
        generated_text = response_json["results"][0]["generated_text"]
    return generated_text

# if response.status_code == 200:
#     response_json = response.json()
#     generated_text = response_json["results"][0]["generated_text"]
#     print("🤖 AI Response:\n", generated_text)
# else:
#     print("❌ Error:", response.status_code, response.text)
