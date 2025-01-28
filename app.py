from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc 
from datetime import datetime
from waitress import serve
import pytz
from huggingface_hub import InferenceClient
import json
from dotenv import load_dotenv
import os

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/myfun_mail', methods=['GET','POST'])
def myfun_mail():
    if request.method == "POST":
        query = request.form['query'] # Email ID
        log = request.form['log'] # Body
        formatted_log = log.replace('\n', '<br>')
        qry = query.lower().strip()
        value = qry.replace("send mail to @", "").replace("send mail to", "").replace("@ to", "").replace("email :", "").replace("email:", "")
        email_id = value.strip()
        # print(email_id)
        # print(log)
        subject = "Delta AI Email Subject 01"
        body = "Hello " + email_id + ",<br>" + formatted_log
        sender = "caliberai123@gmail.com" #From
        load_dotenv() # Load variables from .env file
        password = os.getenv('PSW_Key')
        recipients = [email_id] # To       
        res = send_email(subject, body, sender, recipients, password)
        if(res == 1):
            print("Email sent successfully.")
            return jsonify({'output':'Email sent successfully.'})
        else:
            print("Error in Email!!!")
            return jsonify({'output': 'The error in Email.'})
    return render_template('index.html')

import smtplib
from email.mime.text import MIMEText
def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())    
    # print("Email sent successfully!")
    return 1


@app.route('/myfun', methods=['GET','POST'])
def myfun():
    if request.method == "POST":
        query = request.form['query']
        if len(query.strip()) > 0:  
            try:
                response = take_cmd(query)
                return jsonify({'output':response})
            except Exception as e:
                print("The error is: ", str(e))
                return jsonify({'output': "The error is : " + str(e)})
        else:
            return jsonify({'output':'Error!'})
    return render_template('index.html')

import time
def take_cmd(query):
    a1 = ["hello", "namaskar", "namaste", "namskar" , "namste", "salam"]
    a2 = ["who r u", "who r u?" , "w r u", "who are you", "who are you?", "how are you", "h r u", "how r u"]
    response = ""
    if any(x in query.lower() for x in a1) or query.lower() == "hi":
        # print(query)
        response = "Hello! I'm DeltaAI, How can I assist you today?"
        time.sleep(2)   
    elif any(x in query.lower() for x in a2):
        response ="I'm DeltaAI, your friendly AI assistant! I can help with answering questions, brainstorming ideas, learning new topics, writing, coding, and much more. What's on your mind?" 
        time.sleep(2)  
    elif "play" in query.lower():     
        print('Playing on Youtube....')  
        topic = query.lower().replace('play ', '')
        response = playonyt(topic)  
    elif "weather" in query.lower():
        # key, value = query.lower().split(":")
        qry = query.lower().strip()
        value = qry.replace("weather of", "").replace("weather for", "").replace("weather in", "").replace("weather :", "").replace("weather:", "").replace("weather", "").strip()
        # import re
        # value = re.sub(r"weather (of|for|in|:)\s*", "", query.lower()).strip()
        # key, value = map(str.strip, query.lower().split(":"))
        city_name = value
        res = GetWeather(city_name)
        if res.status_code == 200:
            api_data = res.json()
            # a = json.dumps(api_data)  # for double quoats str response           
        response = str(api_data)
    elif "pollution" in query.lower():
        qry = query.lower().strip()
        value = qry.replace("air pollution in", "").replace("air pollution of", "").replace("pollution of", "").replace("pollution for", "").replace("pollution in", "").replace("air pollution", "").replace("pollution", "").strip()
        city_name = value
        # print('M1 = ' , city_name)
        res = GetPollution(city_name)       
        if res.status_code == 200:
            api_data = res.json()      
            api_data['city'] = city_name.capitalize()    
        response = str(api_data)    
    elif "news headlines sports" in query.lower():
        response = GetNews("Sports")
    elif "news headlines technology" in query.lower():
        response = GetNews("Technology")
    elif "news headlines entertainment" in query.lower():
        response = GetNews("Entertainment")
    elif "news headlines nation" in query.lower():
        response = GetNews("Nation")
    elif "news headlines business" in query.lower():
        response = GetNews("Business")
    elif "news headlines health" in query.lower():
        response = GetNews("Health")
    elif "news" in query.lower():
        response = GetNews("Sports") + "\n"
        response += GetNews("Technology") + "\n"
        response += GetNews("Entertainment")
    else:        
        load_dotenv() # Load variables from .env file
        api_key = os.getenv('HF_TOKEN')
        model_1 = os.getenv('MODEL_1')    
        os.environ["HF_TOKEN"] = api_key
        # model_1 = "microsoft/Phi-3.5-mini-instruct"
        # model_1 = "mistralai/Mistral-Nemo-Instruct-2407" 
        repo_id = model_1 
        My_client = InferenceClient(model=repo_id, timeout=120,)
        response = call_chatBot(My_client, query)
    return response

def call_chatBot(inference_client: InferenceClient, prompt: str):
    response = inference_client.post(
        json={
            "inputs": prompt,
            "parameters": {"max_new_tokens": 1000},
            "task": "text-generation",
        },
    )
    return json.loads(response.decode())[0]["generated_text"]

def playonyt(topic):
    # """Will play video on following topic, takes about 10 to 15 seconds to load"""
    url = 'https://www.youtube.com/results?q=' + topic
    print(url)
    count = 0
    import requests
    cont = requests.get(url)
    data = str(cont.content)
    lst = data.split('"')
    for i in lst:
        count+=1
        if i == 'WEB_PAGE_TYPE_WATCH':
            break
    if lst[count-5] == "/results":
        raise Exception("No video found.")
    # web.open("https://www.youtube.com"+lst[count-5])
    return "https://www.youtube.com"+lst[count-5]

import requests
def GetWeather(city_name):   
    load_dotenv() # Load variables from .env file
    API_Key = os.getenv('API_Key')  
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_Key}'
    response = requests.get(url)
    return response

def GetPollution(city_name):
    response1 = GetWeather(city_name)
    if response1.status_code == 200:
        api_data = response1.json()
        lon = api_data['coord']['lon']
        lat = api_data['coord']['lat']
        data = GetPollution2(lat,lon)
        return data
    else:
        return "No response"
    
def GetPollution2(lat,lon):   
    load_dotenv() # Load variables from .env file
    API_Key = os.getenv('API_Key')
    url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_Key}'
    response2 = requests.get(url)
    return response2
from gnewsclient import gnewsclient
def GetNews(_topic):
    date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")
    output = []
    output.append("------------------------------------------------------------------------------------------")
    output.append(f"News Headlines - {_topic.upper()}  || {date_time}")
    output.append("------------------------------------------------------------------------------------------")
    
    client = gnewsclient.NewsClient(language='english', location='india', topic=_topic, max_results=3)
    news_list = client.get_news()
    
    if not news_list:
        output.append(f"No news found for topic: {_topic}")
        return "\n".join(output)
    
    for count, item in enumerate(news_list, start=1):
        # Escape special characters
        title = item.get('title', 'No Title Available') #.replace("'", "\\'")
        # link = item.get('link', 'No Link Available')
        output.append(f"{count}: {title}")
        # output.append(f"Link: {link}\n")
    
    return "\n".join(output)


@app.route('/load')
def load():
   return render_template('test.html')

if __name__ == "__main__":
    # app.debug = True
    # app.run(host="0.0.0.0", port=8000)
    serve(app, host="0.0.0.0", port=8000, threads=8)