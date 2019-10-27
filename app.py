from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
import os

#initialize Flask
app = Flask(__name__)

#initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
#creates collection
images_ref = db.collection('images')

@app.route('/post', methods=['POST'])
def post():
    try:
        image_json = request.json
        images_ref.document(u'images').set(image_json)
        return jsonify({"success": True}), 200
    except Exception as error:
        return "Error: {}".format(error)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
