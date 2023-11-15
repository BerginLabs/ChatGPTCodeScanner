#!/usr/bin/env python3

import os
import base64

import openai

from flask import Flask, request, jsonify

app = Flask(__name__)
client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

@app.route("/analyze", methods=("GET", "POST"))
def analyze():
    if request.method == "POST":
        req_data = request.json
        
        encoded_code = req_data["code"]
        decoded_code = base64.b64decode(encoded_code)

        resp = client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "user", 
                "content": f"Tell me where there is a security vulnerability in the following code: {decoded_code}"
            }]
        )

        result = resp.choices[0].message.content
        return jsonify(result=result)

    return jsonify({"message": "please submit code."})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)