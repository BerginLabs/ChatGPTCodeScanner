#!/usr/bin/env python3

import os
import json

import openai

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


# c_buffer_overflow_code = "I2luY2x1ZGUgPHN0ZGlvLmg+CiNpbmNsdWRlIDxzdHJpbmcuaD4KCmludCBtYWluKHZvaWQpCnsKICAgIGNoYXIgYnVmZlsxNV07CiAgICBpbnQgcGFzcyA9IDA7CgogICAgcHJpbnRmKCJcbiBFbnRlciB0aGUgcGFzc3dvcmQgOiBcbiIpOwogICAgZ2V0cyhidWZmKTsKCiAgICBpZihzdHJjbXAoYnVmZiwgInRoZWdlZWtzdHVmZiIpKQogICAgewogICAgICAgIHByaW50ZiAoIlxuIFdyb25nIFBhc3N3b3JkIFxuIik7CiAgICB9CiAgICBlbHNlCiAgICB7CiAgICAgICAgcHJpbnRmICgiXG4gQ29ycmVjdCBQYXNzd29yZCBcbiIpOwogICAgICAgIHBhc3MgPSAxOwogICAgfQoKICAgIGlmKHBhc3MpCiAgICB7CiAgICAgICAvKiBOb3cgR2l2ZSByb290IG9yIGFkbWluIHJpZ2h0cyB0byB1c2VyKi8KICAgICAgICBwcmludGYgKCJcbiBSb290IHByaXZpbGVnZXMgZ2l2ZW4gdG8gdGhlIHVzZXIgXG4iKTsKICAgIH0KCiAgICByZXR1cm4gMDsKfQ=="
# xxs_ruby_code = "IyB4c3Nfc2ltdWxhdGlvbi5yYgpjbGFzcyBNZXNzYWdlCiAgYXR0cl9hY2Nlc3NvciA6Y29udGVudAoKICBkZWYgaW5pdGlhbGl6ZShjb250ZW50KQogICAgQGNvbnRlbnQgPSBjb250ZW50CiAgZW5kCmVuZAoKIyBTaW11bGF0aW5nIGEgdmlldyB0ZW1wbGF0ZSByZW5kZXJpbmcKZGVmIHJlbmRlcl9tZXNzYWdlcyhtZXNzYWdlcykKICBtZXNzYWdlcy5lYWNoIGRvIHxtZXNzYWdlfAogICAgcHV0cyAiTWVzc2FnZTogI3ttZXNzYWdlLmNvbnRlbnR9IgogIGVuZAplbmQKCiMgU2ltdWxhdGUgY3JlYXRpbmcgbWVzc2FnZXMgKGFzIGlmIHRoZXkgd2VyZSBjcmVhdGVkIGJ5IHVzZXJzKQptZXNzYWdlcyA9IFsKICBNZXNzYWdlLm5ldygiSGVsbG8sIHdvcmxkISIpLAogIE1lc3NhZ2UubmV3KCI8c2NyaXB0PmFsZXJ0KCdYU1MnKTwvc2NyaXB0PiIpICMgWFNTIFBheWxvYWQKXQoKIyBSZW5kZXIgdGhlIG1lc3NhZ2VzIChzaW11bGF0aW5nIGEgdnVsbmVyYWJsZSB2aWV3KQpwdXRzICJSZW5kZXJpbmcgbWVzc2FnZXMgKHZ1bG5lcmFibGUgdG8gWFNTKToiCnJlbmRlcl9tZXNzYWdlcyhtZXNzYWdlcykKCiMgVG8gcHJldmVudCBYU1MsIHlvdSB3b3VsZCB0eXBpY2FsbHkgc2FuaXRpemUgdGhlIGNvbnRlbnQgaW4gYSByZWFsIFJhaWxzIGFwcC4KIyBJbiB0aGlzIHNpbXVsYXRpb24sIHdlJ2xsIGp1c3QgZGVtb25zdHJhdGUgZXNjYXBpbmcgdGhlIEhUTUwuCmRlZiBlc2NhcGVfaHRtbCh0ZXh0KQogIHRleHQuZ3N1YignPCcsICcmbHQ7JykuZ3N1YignPicsICcmZ3Q7JykKZW5kCgpkZWYgcmVuZGVyX21lc3NhZ2VzX3NhZmVseShtZXNzYWdlcykKICBtZXNzYWdlcy5lYWNoIGRvIHxtZXNzYWdlfAogICAgcHV0cyAiTWVzc2FnZTogI3tlc2NhcGVfaHRtbChtZXNzYWdlLmNvbnRlbnQpfSIKICBlbmQKZW5kCgojIFJlbmRlciB0aGUgbWVzc2FnZXMgc2FmZWx5CnB1dHMgIlxuUmVuZGVyaW5nIG1lc3NhZ2VzICh3aXRoIGJhc2ljIEhUTUwgZXNjYXBpbmcgdG8gcHJldmVudCBYU1MpOiIKcmVuZGVyX21lc3NhZ2VzX3NhZmVseShtZXNzYWdlcykK"
# pickle_deserializer_python_code = "aW1wb3J0IHBpY2tsZQppbXBvcnQgYmFzZTY0CmZyb20gZmxhc2sgaW1wb3J0IEZsYXNrLCByZXF1ZXN0CgphcHAgPSBGbGFzayhfX25hbWVfXykKCkBhcHAucm91dGUoIi9ob21lIiwgbWV0aG9kcz1bIlBPU1QiXSkKZGVmIGhvbWUoKToKICAgIGRhdGEgPSBiYXNlNjQudXJsc2FmZV9iNjRkZWNvZGUocmVxdWVzdC5mb3JtWydwaWNrbGVkJ10pCiAgICBkZXNlcmlhbGl6ZWQgPSBwaWNrbGUubG9hZHMoZGF0YSkKICAgIHJldHVybiAnJywgMjA0"


class Config(object):
    SECRET_KEY = os.environ['FLASK_SECRET_KEY']


class CodeSubmitForm(FlaskForm):
    code = TextAreaField(
        'code', 
        validators=[DataRequired()], 
        render_kw={'rows': 50, 'cols': 100}
    )
    submit = SubmitField('submit')


class ChatGPT(object):
    def __init__(self, client):
        self.client = client
        self.model = "gpt-4"
        self.messages = [
            {
                "role": "system",
                "content": "You are a programming bot to help users write and secure code in any programming language."
            },
            {
                "role": "system", 
                "content": "When you create your response, for each 'finding' describe 5 data points: 'issue_id', 'issue_severity', 'issue_name', 'issue_description', and 'issue_solution'."
            },
            {
                "role": "system",
                "content": "For the 'issue_id' data point, create a uuid identifier for object you generate using uuid4"
            },
            {
                "role": "system",
                "content": "For the 'issue_severity' data point, rank the objects risk severity from this range: Low, Medium, High, Critical"
            },
            {
                "role": "system", 
                "content": "Make sure to provide your response in a JSON structure that can be parsed. Dont include any other data."
            },
            {
                "role": "system", 
                "content": "Here is an example structure for your answers output: {'findings': [{'issue_name':'', 'issue_description': '', 'issue_solution': '', 'issue_id': '', 'issue_severity': ''}]}"
            },
            {
                "role": "system", 
                "content": "Your response should only include the JSON data you produced."
            }
        ]
        self._setup_context()

    def _setup_context(self):
        response = client.chat.completions.create(
            model=self.model,
            messages=self.messages
        )
        self.messages.append(
            {
                "role": "assistant", 
                "content": response.choices[0].message.content
            }
        )
        return response.choices[0].message.content

    def get_chat_thread(self):
        return self.messages

    def message(self, message):
        self.messages.append({"role": "user", "content": message})
        response = client.chat.completions.create(
            model=self.model,
            messages=self.messages
        )
        self.messages.append(
            {
                "role": "assistant", 
                "content": response.choices[0].message.content
            }
        )
        return response.choices[0].message.content


app = Flask(__name__)
client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
gpt = ChatGPT(client)


@app.route("/", methods=("GET",))
def home():
    return redirect(url_for('index'))


@app.route("/clear", methods=["GET",])
def clear():
    for msg in gpt.messages:
        if msg['role'] != 'system':
            gpt.messages.remove(msg)
    return redirect(url_for('code_analyzer'))


@app.route('/home', methods=["GET",])
def index():
    user = {'username': 'Brett'}
    title = "ChatGPT Analyzer"
    chat_thread = gpt.get_chat_thread()

    return render_template(
        "index.html", 
        title=title, 
        user=user, 
        chat_thread=chat_thread
    )


@app.route('/code', methods=["GET", "POST"])
def code_analyzer():
    user = {'username': 'Brett'}
    title = "ChatGPT Analyzer"
    form = CodeSubmitForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            source_code = form.code.data
            result = gpt.message(message=f"{source_code}")
            try:
                result = json.loads(result)
                result_as_json = True

            except Exception as parser_err:
                print(f"[-] Failed to parse ChatGPT response as JSON: {parser_err}")
                result_as_json = False

            return render_template(
                "code.html", 
                title=title, 
                user=user, 
                form=form,
                code=source_code,
                answer=result,
                result_as_json=result_as_json,
                chat_thread=gpt.get_chat_thread()
            )

    return render_template(
        "code.html", 
        title=title, 
        user=user, 
        chat_thread=gpt.get_chat_thread(),
        form=form
    )

@app.route('/chat', methods=['GET',])
def chat():
    thread = gpt.get_chat_thread()
    return render_template(
        "chat_thread.html",
        chat_thread=thread,
    )


if __name__ == '__main__':
    app.config.from_object(Config)
    app.run(host='0.0.0.0', port=8888)
