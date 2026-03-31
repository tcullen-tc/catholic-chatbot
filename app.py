from flask import Flask, request, jsonify, render_template_string
from catholic_chatbot import *

app = Flask(__name__)

# HTML template with menu and prayer mode
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>✝️ What Would Jesus Say?</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 0 auto; padding: 20px; background: #f5f0e8; }
        h1 { color: #8B4513; text-align: center; }
        .menu { display: flex; gap: 10px; margin-bottom: 20px; justify-content: center; }
        .menu button { padding: 10px 20px; background: #8B4513; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        .menu button:hover { background: #5a2c0c; }
        .menu .active { background: #2c5a2c; }
        .question-box, .prayer-box { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        input { width: 70%; padding: 10px; margin: 5px; border: 2px solid #ddd; border-radius: 5px; }
        button.ask-btn, button.pray-btn { padding: 10px 20px; background: #8B4513; color: white; border: none; border-radius: 5px; cursor: pointer; }
        #response { margin-top: 20px; padding: 15px; background: #fef7e0; border-radius: 10px; white-space: pre-wrap; font-family: 'Georgia', serif; line-height: 1.6; }
        .footer { margin-top: 20px; font-size: 12px; color: #777; text-align: center; }
        .prayer-intention { width: 80%; padding: 10px; margin: 10px 0; }
    </style>
</head>
<body>
    <h1>✝️ What Would Jesus Say?</h1>
    
    <div class="menu">
        <button id="questionBtn" class="active">❓ Ask a Question</button>
        <button id="prayerBtn">🙏 Prayer Mode</button>
    </div>
    
    <div id="questionMode" class="question-box">
        <h3>Ask a Question</h3>
        <input type="text" id="question" placeholder="e.g., What does the Bible say about forgiveness?">
        <button class="ask-btn" onclick="askQuestion()">Ask</button>
    </div>
    
    <div id="prayerMode" class="prayer-box" style="display:none;">
        <h3>🙏 Prayer Mode</h3>
        <p>Share your prayer intention with details (names, situations, etc.)</p>
        <p><em>Example: "Pray for my grandmother Maria who is in the hospital"</em></p>
        <input type="text" id="prayerIntention" class="prayer-intention" placeholder="What would you like to pray for?">
        <button class="pray-btn" onclick="submitPrayer()">Generate Prayer</button>
    </div>
    
    <div id="response"></div>
    <div class="footer">Sources: Scripture, Catechism, Vatican II, Church Fathers, Saints</div>
    
    <script>
        document.getElementById('questionBtn').onclick = function() {
            document.getElementById('questionMode').style.display = 'block';
            document.getElementById('prayerMode').style.display = 'none';
            document.getElementById('questionBtn').classList.add('active');
            document.getElementById('prayerBtn').classList.remove('active');
            document.getElementById('response').innerHTML = '';
        };
        
        document.getElementById('prayerBtn').onclick = function() {
            document.getElementById('questionMode').style.display = 'none';
            document.getElementById('prayerMode').style.display = 'block';
            document.getElementById('prayerBtn').classList.add('active');
            document.getElementById('questionBtn').classList.remove('active');
            document.getElementById('response').innerHTML = '';
        };
        
        async function askQuestion() {
            const question = document.getElementById('question').value;
            const responseDiv = document.getElementById('response');
            responseDiv.innerHTML = '📚 Searching for answers...';
            
            const res = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({type: 'question', content: question})
            });
            const data = await res.json();
            responseDiv.innerHTML = data.answer.replace(/\\n/g, '<br>');
        }
        
        async function submitPrayer() {
            const intention = document.getElementById('prayerIntention').value;
            const responseDiv = document.getElementById('response');
            responseDiv.innerHTML = '🙏 Generating prayer...';
            
            const res = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({type: 'prayer', content: intention})
            });
            const data = await res.json();
            responseDiv.innerHTML = data.answer.replace(/\\n/g, '<br>');
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return HTML_TEMPLATE

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    request_type = data.get('type', 'question')
    content = data.get('content', '')
    
    if request_type == 'prayer':
        # Prayer mode
        if not content.strip():
            return jsonify({'answer': 'Please share what you would like to pray for.'})
        
        prompt = f"""Write a warm, personal Catholic prayer for this intention:

INTENTION: {content}

Guidelines:
1. Use the specific details provided
2. Address God, Jesus, or Mary
3. Be warm and conversational, not stiff
4. Include hope and trust in God
5. End with "Amen"
6. Length: 4-8 sentences

PRAYER:"""
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a compassionate Catholic prayer companion. Write warm, personal prayers."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=400
            )
            prayer = response.choices[0].message.content
            return jsonify({'answer': f"🙏 **Your Prayer** 🙏\n\n{prayer}\n\n---\n*May God bless you and answer your intention.*"})
        except Exception as e:
            return jsonify({'answer': f"Error generating prayer: {e}"})
    
    else:
        # Question mode
        print(f"📚 Question received: {content}")
        
        sources = gather_sources(content)
        
        print(f"📖 Found {len(sources)} sources")
        
        if OPENAI_AVAILABLE and client is not None:
            answer = answer_with_openai(content, sources)
        else:
            answer = "OpenAI is not available. Please check your API key."
        
        return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
