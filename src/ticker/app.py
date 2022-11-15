from flask import Flask, request
import json
import processor

app = Flask(__name__)

@app.route('/ticker/list')
def get_ticker_list():
    return json.dumps(processor.get_tickers())

@app.route('/ticker', methods=['POST'])
def add_ticker():
    return processor.add_ticker(request.get_json())

@app.route('/ticker', methods=['DELETE'])
def remove_ticker():
    return processor.remove_ticker(request.get_json())
