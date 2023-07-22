from flask import Flask, jsonify, request
from datetime import datetime
import random

app = Flask(__name__)


@app.route('/pay', methods=['POST'])
def process_payment():
    print(f"\n\n*********\nReceived data from sender at {datetime.now()}:-\n{request.form}")
    val = random.randint(0, 1)
    return {"result": "No" if val == 0 else "Ok"}


if __name__ == '__main__':
    app.run(port=8083, debug=True)
