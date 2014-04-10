import pdb

from flask import Flask, request, jsonify
from pipeline import RiskOfBiasPipeline, SampleSizePipeline
import json
import logging

DEBUG_MODE = True

logging.basicConfig(level=(logging.DEBUG if DEBUG_MODE else logging.INFO))
logger = logging.getLogger(__name__)

app = Flask(__name__)
pipelines = [RiskOfBiasPipeline(), SampleSizePipeline()]

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/annotate', methods=['POST'])
def annotate():
    payload = json.loads(request.data)

    results = [p.run(payload["pages"]) for p in pipelines]
    result = reduce(lambda memo, r: memo + r["result"], results, [])

    response = {}
    response["result"] = result
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=DEBUG_MODE)
