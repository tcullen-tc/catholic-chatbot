from flask import Flask, request, jsonify, render_template_string
from catholic_chatbot import *

app = Flask(__name__)

# HTML template with menu, prayer mode, and Did You Know section
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>✝️ What Would Jesus Say? - Catholic Chatbot</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            background: linear-gradient(rgba(245, 240, 232, 0.92), rgba(245, 240, 232, 0.92)),
                        url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" opacity="0.1"><path d="M10,10 L90,10 M10,20 L90,20 M10,30 L90,30 M10,40 L90,40 M10,50 L90,50 M10,60 L90,60 M10,70 L90,70 M10,80 L90,80 M10,90 L90,90" stroke="%238B4513" stroke-width="0.5"/><path d="M10,10 L10,90 M20,10 L20,90 M30,10 L30,90 M40,10 L40,90 M50,10 L50,90 M60,10 L60,90 M70,10 L70,90 M80,10 L80,90 M90,10 L90,90" stroke="%238B4513" stroke-width="0.5"/></svg>');
            background-repeat: repeat;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
            overflow: hidden;
            border: 1px solid #d4c5a9;
        }
        
        /* Header with Crucifix */
        .header {
            background: linear-gradient(135deg, #2c1a0e 0%, #4a2c1a 100%);
            color: #f5e6c4;
            padding: 20px;
            text-align: center;
            border-bottom: 4px solid #c9a03d;
            position: relative;
        }
        
        .crucifix {
            font-size: 48px;
            margin-bottom: 10px;
            display: inline-block;
            animation: gentlePulse 3s ease-in-out infinite;
        }
        
        @keyframes gentlePulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.9; transform: scale(1.02); }
        }
        
        .header h1 {
            font-size: 28px;
            margin: 5px 0;
            letter-spacing: 2px;
            font-family: 'Georgia', serif;
        }
        
        .header p {
            font-size: 14px;
            color: #e8d5a8;
            font-style: italic;
        }
        
        /* Did You Know Section */
        .did-you-know {
            background: linear-gradient(135deg, #fef7e0 0%, #fdf4d0 100%);
            border-left: 5px solid #c9a03d;
            border-right: 5px solid #c9a03d;
            margin: 20px;
            padding: 15px 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
        }
        
        .dyk-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 12px;
        }
        
        .dyk-icon {
            font-size: 28px;
        }
        
        .dyk-header h3 {
            color: #8B4513;
            font-size: 18px;
            margin: 0;
            flex-grow: 1;
        }
        
        .dyk-controls {
            display: flex;
            gap: 8px;
        }
        
        .dyk-next {
            background: #8B4513;
            color: white;
            border: none;
            padding: 5px 12px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 12px;
            transition: background 0.2s;
        }
        
        .dyk-next:hover {
            background: #5a2c0c;
        }
        
        .dyk-content {
            font-size: 15px;
            line-height: 1.5;
            color: #3a2a1a;
            min-height: 80px;
            padding: 5px;
        }
        
        .dyk-source {
            font-size: 11px;
            color: #8B7355;
            margin-top: 10px;
            text-align: right;
            font-style: italic;
        }
        
        .menu {
            display: flex;
            gap: 10px;
            margin: 20px 20px 0 20px;
            justify-content: center;
        }
        
        .menu button {
            padding: 12px 24px;
            background: #8B4513;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: all 0.2s;
            font-family: 'Georgia', serif;
        }
        
        .menu button:hover {
            background: #5a2c0c;
            transform: translateY(-2px);
        }
        
        .menu .active {
            background: #2c5a2c;
            box-shadow: 0 2px 8px rgba(44,90,44,0.3);
        }
        
        .question-box, .prayer-box {
            background: white;
            padding: 25px;
            margin: 0 20px 20px 20px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            border: 1px solid #e8dcc8;
        }
        
        .question-box h3, .prayer-box h3 {
            color: #8B4513;
            margin-bottom: 15px;
            font-size: 20px;
        }
        
        input {
            width: 70%;
            padding: 12px;
            margin: 5px;
            border: 2px solid #e0d4c0;
            border-radius: 8px;
            font-size: 14px;
            font-family: 'Georgia', serif;
            transition: border-color 0.2s;
        }
        
        input:focus {
            outline: none;
            border-color: #c9a03d;
        }
        
        button.ask-btn, button.pray-btn {
            padding: 12px 24px;
            background: #c9a03d;
            color: #2c1a0e;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            transition: all 0.2s;
        }
        
        button.ask-btn:hover, button.pray-btn:hover {
            background: #b8902a;
            transform: translateY(-1px);
        }
        
        #response {
            margin: 20px;
            padding: 20px;
            background: #fef7e0;
            border-radius: 12px;
            white-space: pre-wrap;
            font-family: 'Georgia', serif;
            line-height: 1.6;
            border-left: 4px solid #c9a03d;
            color: #2c1a0e;
        }
        
        .footer {
            margin: 20px;
            padding: 15px;
            font-size: 11px;
            color: #8B7355;
            text-align: center;
            border-top: 1px solid #e8dcc8;
        }
        
        .prayer-intention {
            width: 80%;
            padding: 12px;
            margin: 10px 0;
        }
        
        @media (max-width: 600px) {
            body { padding: 10px; }
            input { width: 100%; margin: 10px 0; }
            .prayer-intention { width: 100%; }
            .menu button { padding: 8px 16px; font-size: 14px; }
            .header h1 { font-size: 22px; }
            .crucifix { font-size: 36px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header with Crucifix -->
        <div class="header">
            <div class="crucifix">✝️</div>
            <h1>What Would Jesus Say?</h1>
            <p>Guided by Scripture, Tradition, and the Magisterium</p>
        </div>
        
        <!-- Did You Know Section -->
        <div class="did-you-know" id="didYouKnow">
            <div class="dyk-header">
                <span class="dyk-icon">📜</span>
                <h3>Did You Know?</h3>
                <div class="dyk-controls">
                    <button class="dyk-next" onclick="nextFact()">Next →</button>
                </div>
            </div>
            <div class="dyk-content" id="dykContent">
                Loading Catholic wisdom...
            </div>
            <div class="dyk-source" id="dykSource"></div>
        </div>
        
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
        <div class="footer">Sources: Scripture, Catechism of the Catholic Church, Vatican II, Church Fathers, Saints</div>
    </div>
    
    <script>
        // Did You Know facts - Catholic teachings, forgotten traditions, feast days, etc.
        const facts = [
            {
                text: "The 'Angelus' is a prayer traditionally recited at 6:00 AM, noon, and 6:00 PM to commemorate the Annunciation. The name comes from its opening word in Latin, 'Angelus Domini' (The Angel of the Lord).",
                source: "Tradition of the Church"
            },
            {
                text: "The Passover in the Old Testament prefigures Christ's sacrifice as the 'Lamb of God' who takes away the sins of the world. Jesus celebrated the Last Supper during Passover, instituting the Eucharist.",
                source: "Exodus 12, John 1:29, CCC 1330"
            },
            {
                text: "The Feast of the Presentation of the Lord (February 2) is also known as Candlemas Day, when candles are blessed for use throughout the year, symbolizing Christ as the light of the world.",
                source: "General Roman Calendar"
            },
            {
                text: "The Liturgical Year begins with the First Sunday of Advent, not January 1. Advent marks a time of joyful preparation for the coming of Christ at Christmas.",
                source: "General Norms for the Liturgical Year"
            },
            {
                text: "The word 'Eucharist' comes from the Greek 'eucharistia' meaning 'thanksgiving.' The Eucharist is 'the source and summit of the Christian life' (CCC 1324).",
                source: "Catechism of the Catholic Church 1324-1332"
            },
            {
                text: "The first Saturday of each month is traditionally dedicated to the Virgin Mary. Many Catholics practice the Five First Saturdays devotion as requested by Our Lady of Fatima.",
                source: "Messages of Fatima, 1917"
            },
            {
                text: "St. Joseph is the patron saint of the Universal Church, fathers, workers, and a happy death. Pope Francis declared December 8, 2020 to December 8, 2021 as the Year of St. Joseph.",
                source: "Patris Corde, Pope Francis"
            },
            {
                text: "The Season of Lent lasts 40 days, representing the 40 days Jesus spent fasting in the desert. Sundays are not counted in the 40 days, as each Sunday is a mini-Easter.",
                source: "General Norms for Lent"
            },
            {
                text: "Purgatory is not a second chance but a purification after death for those who die in God's grace but are not yet perfectly purified to enter heaven (CCC 1030-1032).",
                source: "Catechism of the Catholic Church 1030-1032"
            },
            {
                text: "The Chaplet of Divine Mercy was given to St. Faustina by Jesus in 1935. Jesus promised, 'Whoever will recite it will receive great mercy at the hour of death.'",
                source: "Diary of St. Faustina, 687-690"
            }
        ];
        
        let currentFactIndex = 0;
        
        function updateFactDisplay() {
            const fact = facts[currentFactIndex];
            document.getElementById('dykContent').innerHTML = fact.text;
            document.getElementById('dykSource').innerHTML = 'Source: ' + fact.source;
        }
        
        function nextFact() {
            currentFactIndex = (currentFactIndex + 1) % facts.length;
            updateFactDisplay();
        }
        
        // NO AUTO-ROTATION - removed the setInterval timer
        
        // Initialize first fact
        updateFactDisplay();
        
        // Menu toggle functions
        document.getElementById('questionBtn').onclick = function() {
            document.getElementById('questionMode').style.display = 'block';
            document.getElementById('prayerMode').style.display = 'none';
            document.getElementById('questionBtn').classList.add('active');
            document.getElementById('prayerBtn').classList.remove('active');
            document.getElementById('response').innerHTML = '';
            
            // Clear the question input field when switching to question mode
            document.getElementById('question').value = '';
        };
        
        document.getElementById('prayerBtn').onclick = function() {
            document.getElementById('questionMode').style.display = 'none';
            document.getElementById('prayerMode').style.display = 'block';
            document.getElementById('prayerBtn').classList.add('active');
            document.getElementById('questionBtn').classList.remove('active');
            document.getElementById('response').innerHTML = '';
            
            // Clear the prayer intention input field when switching to prayer mode
            document.getElementById('prayerIntention').value = '';
        };
        
        async function askQuestion() {
            const questionInput = document.getElementById('question');
            const question = questionInput.value;
            const responseDiv = document.getElementById('response');
            responseDiv.innerHTML = '📚 Searching Sacred Scripture and Tradition...';
            
            const res = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({type: 'question', content: question})
            });
            const data = await res.json();
            responseDiv.innerHTML = data.answer.replace(/\\\\n/g, '<br>');
            
            // Clear the question input after asking
            questionInput.value = '';
        }
        
        async function submitPrayer() {
            const prayerInput = document.getElementById('prayerIntention');
            const intention = prayerInput.value;
            const responseDiv = document.getElementById('response');
            responseDiv.innerHTML = '🙏 Lifting up your intention in prayer...';
            
            const res = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({type: 'prayer', content: intention})
            });
            const data = await res.json();
            responseDiv.innerHTML = data.answer.replace(/\\\\n/g, '<br>');
            
            // Clear the prayer intention input after submitting
            prayerInput.value = '';
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
