from flask import Flask, request, Response
import json
import processor
from logger import init

init()
app = Flask(__name__)

@app.route('/ticker/list')
def get_ticker_list():
    return Response(json.dumps(processor.get_tickers()), content_type='application/json; charset=utf-8')

@app.route('/ticker', methods=['POST'])
def add_ticker():
    return Response(processor.add_ticker(request.get_json()), content_type='application/json; charset=utf-8')

@app.route('/ticker', methods=['DELETE'])
def remove_ticker():
    return Response(processor.remove_ticker(request.get_json()), content_type='application/json; charset=utf-8')
