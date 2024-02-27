# Note Organizer

A flask app that organizes notes using AI tools. relying on 2 cutting edge technologies : 
- EdenAI's Optical Character Recognition (OCR) for Image to Text Conversion. this helps increase the accuracy of text extraction.
- OpenAI's Large Language Model (LLM) for Text Generation and Organization. to make your notes much clearer in minutes.
## Installation

1- to make API calls, register to [OpenAI](https://openai.com/) and create a developer account. create a secret key and save it.

2- same goes to EdenAI, register to [EdenAI](https://www.edenai.co/) and create a secret key and save it.

3- clone the repository 

4- create a .env file and save the keys inside it. like this : 
```bash
EDENAI_KEY = "your_edenAI_key"
OPENAI_KEY = "your_openAI_key"
```

5- install the requirements:
```
pip install -r requirements.txt
```

6- run the flask app and use it.  



## Usage

After launching the app, it will be accessible at http://localhost:5000. Upload your notes through the web interface, and the organized results will be available within minutes.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## Future plans

**Model Enhancement**: We're focused on refining the model to understand and execute user-specific commands for more personalized note organization.

**Language Support**: Efforts are underway to enhance the accuracy of text results in Arabic and other languages.

**UI/UX Improvements**: Plans to revamp the user interface for a more intuitive experience are in the pipeline.

