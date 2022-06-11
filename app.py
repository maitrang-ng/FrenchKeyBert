import flask
from flask import Flask, request
from processing import processing
from filters import fuzzy_string_matching

app = Flask(__name__)

@app.route('/')
def welcome():
    return 'Home page'

@app.route('/json', methods=['POST'])
def process_text():
    data = request.get_json()
    if not data or len(data['text'])<50:
        return 'Please type more than 50 characters!'
    else:
        X = processing(data['text'])
        NER = fuzzy_string_matching(X[0], threshold=4)
        KEYS = fuzzy_string_matching(X[1], threshold=7)
        R = {}
        R['ner'] = NER
        R['keys'] = KEYS
        #print('NER:', NER)
        #print('KEYS:', KEYS )
        return R



