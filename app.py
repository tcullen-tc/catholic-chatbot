from flask import Flask, request, jsonify
from catholic_chatbot import *
import os
from openai import OpenAI
import sys
import os
from openai import OpenAI

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
print("=" * 50, flush=True)
print("ENVIRONMENT CHECK:", flush=True)
print(f"OPENAI_API_KEY exists: {'Yes' if OPENAI_API_KEY else 'No'}", flush=True)
if OPENAI_API_KEY:
    print(f"Key starts with: {OPENAI_API_KEY[:15]}...", flush=True)
else:
    print("Key is missing or empty!", flush=True)
print("=" * 50, flush=True)
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
print("=" * 50)
print("ENVIRONMENT CHECK:")
print(f"OPENAI_API_KEY exists: {'Yes' if OPENAI_API_KEY else 'No'}")
if OPENAI_API_KEY:
    print(f"Key starts with: {OPENAI_API_KEY[:15]}...")
else:
    print("Key is missing or empty!")
print("=" * 50)
app = Flask(__name__)
print(f"DEBUG: OPENAI_API_KEY is {'SET' if OPENAI_API_KEY else 'NOT SET'}")
@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Catholic Chatbot</title>
        <style>
            body { font-family: Arial; max-width: 800px; margin: 0 auto; padding: 20px; background: #f5f0e8; }
            h1 { color: #8B4513; }
            input { width: 70%; padding: 10px; margin: 5px; }
            button { padding: 10px 20px; background: #8B4513; color: white; border: none; cursor: pointer; }
            #response { margin-top: 20px; padding: 15px; background: #fef7e0; border-radius: 10px; white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <h1>✝️ What Would Jesus Say?</h1>
        <input type="text" id="question" placeholder="Ask a question...">
        <button onclick="ask()">Ask</button>
        <div id="response"></div>
        <script>
            async function ask() {
                const question = document.getElementById('question').value;
                const responseDiv = document.getElementById('response');
                responseDiv.innerHTML = 'Thinking...';
                const res = await fetch('/ask', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({question: question})
                });
                const data = await res.json();
                responseDiv.innerHTML = data.answer.replace(/\\n/g, '<br>');
            }
        </script>
    </body>
    </html>
    '''

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '')
    sources = gather_sources(question)
    answer = answer_with_openai(question, sources)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
