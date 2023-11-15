#!/usr/bin/env python3

import os
import base64

import openai

from flask import Flask, request, jsonify

# c_buffer_overflow_code = "I2luY2x1ZGUgPHN0ZGlvLmg+CiNpbmNsdWRlIDxzdHJpbmcuaD4KCmludCBtYWluKHZvaWQpCnsKICAgIGNoYXIgYnVmZlsxNV07CiAgICBpbnQgcGFzcyA9IDA7CgogICAgcHJpbnRmKCJcbiBFbnRlciB0aGUgcGFzc3dvcmQgOiBcbiIpOwogICAgZ2V0cyhidWZmKTsKCiAgICBpZihzdHJjbXAoYnVmZiwgInRoZWdlZWtzdHVmZiIpKQogICAgewogICAgICAgIHByaW50ZiAoIlxuIFdyb25nIFBhc3N3b3JkIFxuIik7CiAgICB9CiAgICBlbHNlCiAgICB7CiAgICAgICAgcHJpbnRmICgiXG4gQ29ycmVjdCBQYXNzd29yZCBcbiIpOwogICAgICAgIHBhc3MgPSAxOwogICAgfQoKICAgIGlmKHBhc3MpCiAgICB7CiAgICAgICAvKiBOb3cgR2l2ZSByb290IG9yIGFkbWluIHJpZ2h0cyB0byB1c2VyKi8KICAgICAgICBwcmludGYgKCJcbiBSb290IHByaXZpbGVnZXMgZ2l2ZW4gdG8gdGhlIHVzZXIgXG4iKTsKICAgIH0KCiAgICByZXR1cm4gMDsKfQ=="
# xxs_ruby_code = "IyB4c3Nfc2ltdWxhdGlvbi5yYgpjbGFzcyBNZXNzYWdlCiAgYXR0cl9hY2Nlc3NvciA6Y29udGVudAoKICBkZWYgaW5pdGlhbGl6ZShjb250ZW50KQogICAgQGNvbnRlbnQgPSBjb250ZW50CiAgZW5kCmVuZAoKIyBTaW11bGF0aW5nIGEgdmlldyB0ZW1wbGF0ZSByZW5kZXJpbmcKZGVmIHJlbmRlcl9tZXNzYWdlcyhtZXNzYWdlcykKICBtZXNzYWdlcy5lYWNoIGRvIHxtZXNzYWdlfAogICAgcHV0cyAiTWVzc2FnZTogI3ttZXNzYWdlLmNvbnRlbnR9IgogIGVuZAplbmQKCiMgU2ltdWxhdGUgY3JlYXRpbmcgbWVzc2FnZXMgKGFzIGlmIHRoZXkgd2VyZSBjcmVhdGVkIGJ5IHVzZXJzKQptZXNzYWdlcyA9IFsKICBNZXNzYWdlLm5ldygiSGVsbG8sIHdvcmxkISIpLAogIE1lc3NhZ2UubmV3KCI8c2NyaXB0PmFsZXJ0KCdYU1MnKTwvc2NyaXB0PiIpICMgWFNTIFBheWxvYWQKXQoKIyBSZW5kZXIgdGhlIG1lc3NhZ2VzIChzaW11bGF0aW5nIGEgdnVsbmVyYWJsZSB2aWV3KQpwdXRzICJSZW5kZXJpbmcgbWVzc2FnZXMgKHZ1bG5lcmFibGUgdG8gWFNTKToiCnJlbmRlcl9tZXNzYWdlcyhtZXNzYWdlcykKCiMgVG8gcHJldmVudCBYU1MsIHlvdSB3b3VsZCB0eXBpY2FsbHkgc2FuaXRpemUgdGhlIGNvbnRlbnQgaW4gYSByZWFsIFJhaWxzIGFwcC4KIyBJbiB0aGlzIHNpbXVsYXRpb24sIHdlJ2xsIGp1c3QgZGVtb25zdHJhdGUgZXNjYXBpbmcgdGhlIEhUTUwuCmRlZiBlc2NhcGVfaHRtbCh0ZXh0KQogIHRleHQuZ3N1YignPCcsICcmbHQ7JykuZ3N1YignPicsICcmZ3Q7JykKZW5kCgpkZWYgcmVuZGVyX21lc3NhZ2VzX3NhZmVseShtZXNzYWdlcykKICBtZXNzYWdlcy5lYWNoIGRvIHxtZXNzYWdlfAogICAgcHV0cyAiTWVzc2FnZTogI3tlc2NhcGVfaHRtbChtZXNzYWdlLmNvbnRlbnQpfSIKICBlbmQKZW5kCgojIFJlbmRlciB0aGUgbWVzc2FnZXMgc2FmZWx5CnB1dHMgIlxuUmVuZGVyaW5nIG1lc3NhZ2VzICh3aXRoIGJhc2ljIEhUTUwgZXNjYXBpbmcgdG8gcHJldmVudCBYU1MpOiIKcmVuZGVyX21lc3NhZ2VzX3NhZmVseShtZXNzYWdlcykK"

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