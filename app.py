from flask import Flask, render_template, request, redirect, url_for
from openai import OpenAI
from werkzeug.utils import secure_filename
import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

EDENAI_KEY = os.environ.get('EDENAI_KEY')
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        #call to EdenAI
        headers = {"Authorization": EDENAI_KEY}

        url = "https://api.edenai.run/v2/ocr/ocr"
        data = {
            "providers": "google",
            "fallback_providers": ""
        }
        files = {"file": open(filepath, 'rb')}
        try:
            response = requests.post(url, data=data, files=files, headers=headers)
            if response.ok:
                result = json.loads(response.text)
                resulttext = result["google"]["text"]

                print(resulttext)
            else:
                # Handle HTTP error
                print(f"Error calling EdenAI: {response.status_code}")
                return redirect(url_for('error'))  # Assuming an error route exists
        except requests.RequestException as e:
            # Handle request exception
            print(f"Request to EdenAI failed: {e}")
            return redirect(url_for('error'))  # Assuming an error route exists

        # end of first api
        
        # GPT prompt 
        
        system_prompt =  "You will get the extracted text from a user messy and incomplete note. try to figure out what is the topic and what is messing then organize the notes. if the notes are not in Engish, use the same language as the notes."
        #call to OpenAI


        messages = [
            {"role": "system", "content":system_prompt},
            {"role": "user", "content": resulttext}
        ]
        try:
            completion = client.chat.completions.create(model="gpt-4", messages=messages)
            if completion.choices and completion.choices[0].message is not None:
                result= completion.choices[0].message.content
            print(result)
        except UnicodeEncodeError as e:
            # Log the error or print a message for debugging purposes
            print("UnicodeEncodeError occurred: %s", e)
            pass

        #end of second api
        
        return redirect(url_for('show_result'),result)
    
    return redirect(request.url)


@app.route('/result')
def show_result(result):
    return render_template('result.html', result=result)
    
    
if __name__ == '__main__':
    app.run(debug=True)
