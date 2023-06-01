from flask import Flask, request, render_template
import os
import requests, json
from dotenv import load_dotenv

global translator_endpoint    
global cog_key    
global cog_region

try:
    load_dotenv()
    cog_key = os.environ.get("COG_SERVICE_KEY")
    cog_region = os.environ.get("COG_SERVICE_REGION")      
    print(cog_key )
    print(cog_region )
    translator_endpoint = 'https://api.cognitive.microsofttranslator.com'   
except Exception as ex:        
    print(ex)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text = request.form['text']
        # Aquí es donde procesarías el texto. Por ahora, solo devolvemos el mismo texto.
        source_language = ''
        #translated_text = text
        source_language= GetLanguage(text)
        language = request.form['language']

        #trans= Translate(text, language)
        #source_language = proof
        translated_text = Translate(text, source_language, language)

        if source_language=="en":
            detected="Inglés"
        elif source_language=="es":
            detected="Español"
        elif source_language=="fr":
            detected="Francés"
        elif source_language=="de":
            detected="Alemán"
        


        #if source_language=="en"


        return render_template('propio.html', translated_text=translated_text,lang_detected=detected)
    
    return render_template('propio.html')

def GetLanguage(text):

        # Use the Translator detect function
    path = '/detect'
    url = translator_endpoint + path

    # Build the request
    params = {
        'api-version': '3.0'
    }

    headers = {
    'Ocp-Apim-Subscription-Key': cog_key,
    'Ocp-Apim-Subscription-Region': cog_region,
    'Content-type': 'application/json'
    }

    body = [{
        'text': text
    }]

    # Send the request and get response
    request = requests.post(url, params=params, headers=headers, json=body)
    response = request.json()

    # Parse JSON array and get language
    language = response[0]["language"]
    

    return language

def Translate(text, source_language, language):
    # Use the Translator translate function
    path = '/translate'
    url = translator_endpoint + path

    # Build the request
    params = {
        'api-version': '3.0',
        'from': source_language,
        'to': language
    }

    headers = {
        'Ocp-Apim-Subscription-Key': cog_key,
        'Ocp-Apim-Subscription-Region': cog_region,
        'Content-type': 'application/json'
    }

    body = [{
        'text': text
    }]

    # Send the request and get response
    request = requests.post(url, params=params, headers=headers, json=body)
    response = request.json()

    # Parse JSON array and get translation
    translation = response[0]["translations"][0]["text"]

    return translation

if __name__ == "__main__":
    app.run(debug=True)
