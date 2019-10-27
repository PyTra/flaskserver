from flask import Flask, request, jsonify, make_response
from firebase_admin import credentials, firestore, initialize_app
import os
from googletrans import Translator
import requests


#DO NOT PUSH THIS ON GITHUB
headers = {
    'x-rapidapi-host': "wordsapiv1.p.rapidapi.com",
    'x-rapidapi-key': "0f3ec5196emshc7cc72c460da828p14cc77jsna30a4b874345"
    }

#initialize Flask
app = Flask(__name__)

#initialize Firestore DB
cred = credentials.Certificate('firebase.json')
default_app = initialize_app(cred)
db = firestore.client()

#initialize Google Translate
translator = Translator()


#creates collection
images_ref = db.collection('images')

@app.route('/post', methods=['POST'])
def post():
    try:
        image_json = request.json
        images_ref.document(u'images').set(image_json)
        return jsonify({"success": True}, 200)
    except Exception as error:
        return "Error: {}".format(error)

@app.route('/translate', methods = ['POST'])
def translate():
    try:
        d = {}
        word_json = request.json
        word = word_json["word"]
        language = word_json["language"]
        translated_word = translator.translate(word, dest = language)
        d["translated_word"] = translated_word.text
        d["translated_pron"] = translated_word.pronunciation
        url = ("https://wordsapiv1.p.rapidapi.com/words/{}/definition".format(word))
        response = requests.request("GET", url, headers=headers)
        d["definition"] = response.json()["definition"]
        return make_response(jsonify(d), 200)
    except Exception as error:
        return "Error: {}".format(error)



if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
