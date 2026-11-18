from flask import Flask, request, jsonify, render_template_string
from catholic_chatbot import *

app = Flask(__name__)

# ============================================================
# MAIN PAGE TEMPLATE (with Liturgy of the Hours button)
# ============================================================
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>✝️ What Would Jesus Say? - Catholic Chatbot</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            background: linear-gradient(rgba(245, 240, 232, 0.92), rgba(245, 240, 232, 0.92)),
                        url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" opacity="0.1"><path d="M10,10 L90,10 M10,20 L90,20 M10,30 L90,30 M10,40 L90,40 M10,50 L90,50 M10,60 L90,60 M10,70 L90,70 M10,80 L90,80 M10,90 L90,90" stroke="%238B4513" stroke-width="0.5"/><path d="M10,10 L10,90 M20,10 L20,90 M30,10 L30,90 M40,10 L40,90 M50,10 L50,90 M60,10 L60,90 M70,10 L70,90 M80,10 L80,90 M90,10 L90,90" stroke="%238B4513" stroke-width="0.5"/></svg>');
            background-repeat: repeat; margin: 0; padding: 20px; min-height: 100vh;
        }
        .container {
            max-width: 900px; margin: 0 auto; background: white;
            border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);
            overflow: hidden; border: 1px solid #d4c5a9;
        }
        .header {
            background: linear-gradient(135deg, #2c1a0e 0%, #4a2c1a 100%);
            color: #f5e6c4; padding: 20px; text-align: center;
            border-bottom: 4px solid #c9a03d;
        }
        .crucifix { font-size: 48px; margin-bottom: 10px; display: inline-block; animation: gentlePulse 3s ease-in-out infinite; }
        @keyframes gentlePulse { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.9; transform: scale(1.02); } }
        .header h1 { font-size: 28px; margin: 5px 0; letter-spacing: 2px; }
        .header p { font-size: 14px; color: #e8d5a8; font-style: italic; }

        .did-you-know {
            background: linear-gradient(135deg, #fef7e0 0%, #fdf4d0 100%);
            border-left: 5px solid #c9a03d; border-right: 5px solid #c9a03d;
            margin: 20px; padding: 15px 20px; border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        .dyk-header { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
        .dyk-icon { font-size: 28px; }
        .dyk-header h3 { color: #8B4513; font-size: 18px; margin: 0; flex-grow: 1; }
        .dyk-next { background: #8B4513; color: white; border: none; padding: 5px 12px; border-radius: 20px; cursor: pointer; font-size: 12px; }
        .dyk-next:hover { background: #5a2c0c; }
        .dyk-content { font-size: 15px; line-height: 1.5; color: #3a2a1a; min-height: 80px; padding: 5px; }
        .dyk-source { font-size: 11px; color: #8B7355; margin-top: 10px; text-align: right; font-style: italic; }

        .menu { display: flex; gap: 10px; margin: 20px 20px 0 20px; justify-content: center; flex-wrap: wrap; }
        .menu button {
            padding: 12px 20px; background: #8B4513; color: white; border: none;
            border-radius: 8px; cursor: pointer; font-size: 15px; font-weight: bold;
            transition: all 0.2s; font-family: 'Georgia', serif;
        }
        .menu button:hover { background: #5a2c0c; transform: translateY(-2px); }
        .menu .active { background: #2c5a2c; box-shadow: 0 2px 8px rgba(44,90,44,0.3); }

        .question-box, .prayer-box {
            background: white; padding: 25px; margin: 0 20px 20px 20px;
            border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            border: 1px solid #e8dcc8;
        }
        .question-box h3, .prayer-box h3 { color: #8B4513; margin-bottom: 15px; font-size: 20px; }

        input {
            width: 70%; padding: 12px; margin: 5px; border: 2px solid #e0d4c0;
            border-radius: 8px; font-size: 14px; font-family: 'Georgia', serif;
        }
        input:focus { outline: none; border-color: #c9a03d; }

        button.ask-btn, button.pray-btn {
            padding: 12px 24px; background: #c9a03d; color: #2c1a0e;
            border: none; border-radius: 8px; cursor: pointer; font-size: 14px; font-weight: bold;
        }
        button.ask-btn:hover, button.pray-btn:hover { background: #b8902a; }

        #response {
            margin: 20px; padding: 20px; background: #fef7e0; border-radius: 12px;
            white-space: pre-wrap; font-family: 'Georgia', serif; line-height: 1.6;
            border-left: 4px solid #c9a03d; color: #2c1a0e;
        }
        .footer { margin: 20px; padding: 15px; font-size: 11px; color: #8B7355; text-align: center; border-top: 1px solid #e8dcc8; }
        .prayer-intention { width: 80%; padding: 12px; margin: 10px 0; }

        @media (max-width: 600px) {
            body { padding: 10px; }
            input { width: 100%; margin: 10px 0; }
            .prayer-intention { width: 100%; }
            .menu button { padding: 8px 12px; font-size: 13px; }
            .header h1 { font-size: 22px; }
            .crucifix { font-size: 36px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="crucifix">✝️</div>
            <h1>What Would Jesus Say?</h1>
            <p>Guided by Scripture, Tradition, and the Magisterium</p>
        </div>

        <div class="did-you-know" id="didYouKnow">
            <div class="dyk-header">
                <span class="dyk-icon">📜</span>
                <h3>Did You Know?</h3>
                <div class="dyk-controls">
                    <button class="dyk-next" onclick="nextFact()">Next →</button>
                </div>
            </div>
            <div class="dyk-content" id="dykContent">Loading Catholic wisdom...</div>
            <div class="dyk-source" id="dykSource"></div>
        </div>

        <div class="menu">
            <button id="questionBtn" class="active">❓ Ask a Question</button>
            <button id="prayerBtn">🙏 Prayer Mode</button>
            <button id="liturgyBtn" onclick="window.location.href='/liturgy'">📖 Liturgy of the Hours</button>
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
        const facts = [
            { text: "The 'Angelus' is a prayer traditionally recited at 6:00 AM, noon, and 6:00 PM to commemorate the Annunciation.", source: "Tradition of the Church" },
            { text: "The Passover in the Old Testament prefigures Christ's sacrifice as the 'Lamb of God' who takes away the sins of the world.", source: "Exodus 12, John 1:29, CCC 1330" },
            { text: "The Feast of the Presentation of the Lord (February 2) is also known as Candlemas Day.", source: "General Roman Calendar" },
            { text: "The Liturgical Year begins with the First Sunday of Advent, not January 1.", source: "General Norms for the Liturgical Year" },
            { text: "The word 'Eucharist' comes from the Greek 'eucharistia' meaning 'thanksgiving.'", source: "CCC 1324-1332" },
            { text: "The first Saturday of each month is traditionally dedicated to the Virgin Mary.", source: "Messages of Fatima, 1917" },
            { text: "St. Joseph is the patron saint of the Universal Church, fathers, workers, and a happy death.", source: "Patris Corde, Pope Francis" },
            { text: "The Season of Lent lasts 40 days, representing the 40 days Jesus spent fasting in the desert.", source: "General Norms for Lent" },
            { text: "Purgatory is a purification after death for those who die in God's grace but are not yet perfectly purified.", source: "CCC 1030-1032" },
            { text: "The Chaplet of Divine Mercy was given to St. Faustina by Jesus in 1935.", source: "Diary of St. Faustina, 687-690" }
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
        updateFactDisplay();

        document.getElementById('questionBtn').onclick = function() {
            document.getElementById('questionMode').style.display = 'block';
            document.getElementById('prayerMode').style.display = 'none';
            document.getElementById('questionBtn').classList.add('active');
            document.getElementById('prayerBtn').classList.remove('active');
            document.getElementById('response').innerHTML = '';
            document.getElementById('question').value = '';
        };

        document.getElementById('prayerBtn').onclick = function() {
            document.getElementById('questionMode').style.display = 'none';
            document.getElementById('prayerMode').style.display = 'block';
            document.getElementById('prayerBtn').classList.add('active');
            document.getElementById('questionBtn').classList.remove('active');
            document.getElementById('response').innerHTML = '';
            document.getElementById('prayerIntention').value = '';
        };

        async function askQuestion() {
            const questionInput = document.getElementById('question');
            const question = questionInput.value;
            const responseDiv = document.getElementById('response');
            responseDiv.innerHTML = '📚 Searching Sacred Scripture and Tradition...';
            const res = await fetch('/ask', {
                method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({type: 'question', content: question})
            });
            const data = await res.json();
            responseDiv.innerHTML = data.answer.replace(/\\\\n/g, '<br>');
            questionInput.value = '';
        }

        async function submitPrayer() {
            const prayerInput = document.getElementById('prayerIntention');
            const intention = prayerInput.value;
            const responseDiv = document.getElementById('response');
            responseDiv.innerHTML = '🙏 Lifting up your intention in prayer...';
            const res = await fetch('/ask', {
                method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({type: 'prayer', content: intention})
            });
            const data = await res.json();
            responseDiv.innerHTML = data.answer.replace(/\\\\n/g, '<br>');
            prayerInput.value = '';
        }
    </script>
</body>
</html>
'''

# ============================================================
# LITURGY OF THE HOURS PAGE
# ============================================================
LITURGY_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>📖 Liturgy of the Hours - Guided Prayer</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            background: linear-gradient(rgba(245, 240, 232, 0.92), rgba(245, 240, 232, 0.92)),
                        url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" opacity="0.1"><path d="M10,10 L90,10 M10,20 L90,20 M10,30 L90,30 M10,40 L90,40 M10,50 L90,50 M10,60 L90,60 M10,70 L90,70 M10,80 L90,80 M10,90 L90,90" stroke="%238B4513" stroke-width="0.5"/><path d="M10,10 L10,90 M20,10 L20,90 M30,10 L30,90 M40,10 L40,90 M50,10 L50,90 M60,10 L60,90 M70,10 L70,90 M80,10 L80,90 M90,10 L90,90" stroke="%238B4513" stroke-width="0.5"/></svg>');
            background-repeat: repeat; margin: 0; padding: 20px; min-height: 100vh;
        }
        .container {
            max-width: 900px; margin: 0 auto; background: white;
            border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);
            overflow: hidden; border: 1px solid #d4c5a9;
        }
        .header {
            background: linear-gradient(135deg, #2c1a0e 0%, #4a2c1a 100%);
            color: #f5e6c4; padding: 20px; text-align: center;
            border-bottom: 4px solid #c9a03d;
        }
        .header .crucifix { font-size: 40px; margin-bottom: 8px; display: inline-block; }
        .header h1 { font-size: 26px; margin: 5px 0; letter-spacing: 2px; }
        .header p { font-size: 14px; color: #e8d5a8; font-style: italic; }

        .back-btn {
            display: inline-block; margin: 20px; padding: 10px 20px;
            background: #8B4513; color: white; text-decoration: none;
            border-radius: 8px; font-weight: bold;
        }
        .back-btn:hover { background: #5a2c0c; }

        .content { padding: 0 20px 20px 20px; }

        .intro {
            background: #fef7e0; padding: 20px; border-radius: 12px;
            border-left: 5px solid #c9a03d; margin-bottom: 25px;
            line-height: 1.7; color: #2c1a0e;
        }

        .hour-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 15px; margin-bottom: 25px;
        }
        .hour-card {
            background: linear-gradient(135deg, #fef7e0 0%, #fdf4d0 100%);
            border: 2px solid #c9a03d; border-radius: 12px; padding: 18px;
            cursor: pointer; transition: all 0.2s; text-align: center;
        }
        .hour-card:hover { transform: translateY(-3px); box-shadow: 0 6px 16px rgba(139,69,19,0.2); }
        .hour-card.selected { background: #8B4513; color: white; border-color: #5a2c0c; }
        .hour-card.selected .hour-time { color: #e8d5a8; }
        .hour-icon { font-size: 32px; margin-bottom: 8px; }
        .hour-card h3 { color: #8B4513; font-size: 16px; margin-bottom: 5px; }
        .hour-card.selected h3 { color: #f5e6c4; }
        .hour-time { font-size: 12px; color: #8B7355; font-style: italic; }

        .prayer-panel {
            background: #fdfaf3; border: 1px solid #e8dcc8;
            border-radius: 12px; padding: 25px; margin-top: 20px;
        }
        .prayer-panel h2 { color: #8B4513; margin-bottom: 8px; font-size: 22px; }
        .prayer-panel .subtitle { color: #8B7355; font-style: italic; margin-bottom: 20px; font-size: 14px; }

        .prayer-step {
            margin-bottom: 20px; padding: 15px; background: white;
            border-radius: 8px; border-left: 4px solid #c9a03d;
        }
        .prayer-step h4 {
            color: #8B4513; font-size: 15px; margin-bottom: 10px;
            text-transform: uppercase; letter-spacing: 1px;
        }
        .prayer-step p { line-height: 1.7; color: #2c1a0e; margin-bottom: 8px; }
        .prayer-step .response { color: #2c5a2c; font-weight: bold; }
        .prayer-step .rubric { color: #8B7355; font-style: italic; font-size: 13px; }
        .antiphon {
            background: #f0e8d8; padding: 10px 15px; border-radius: 6px;
            font-style: italic; color: #5a2c0c; margin: 10px 0;
        }
        .glory-be { color: #8B4513; font-weight: bold; font-style: italic; margin-top: 10px; }

        .external-links {
            margin-top: 25px; padding: 20px; background: #f0e8d8;
            border-radius: 12px; text-align: center;
        }
        .external-links h3 { color: #8B4513; margin-bottom: 12px; }
        .external-links a {
            display: inline-block; margin: 5px; padding: 10px 18px;
            background: #8B4513; color: white; text-decoration: none;
            border-radius: 8px; font-size: 14px;
        }
        .external-links a:hover { background: #5a2c0c; }

        .footer { margin: 20px; padding: 15px; font-size: 11px; color: #8B7355; text-align: center; border-top: 1px solid #e8dcc8; }

        @media (max-width: 600px) {
            body { padding: 10px; }
            .header h1 { font-size: 20px; }
            .header .crucifix { font-size: 32px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="crucifix">📖</div>
            <h1>Liturgy of the Hours</h1>
            <p>The Daily Prayer of the Church</p>
        </div>

        <a href="/" class="back-btn">← Back to Chatbot</a>

        <div class="content">
            <div class="intro">
                <strong>What is the Liturgy of the Hours?</strong><br>
                Also called the <em>Divine Office</em>, this is the daily prayer of the Church, prayed by priests, religious, and laypeople around the world. It sanctifies the entire day by marking specific hours with psalms, Scripture, and prayers. The Second Vatican Council called it <em>"the very voice of the Church"</em> (Sacrosanctum Concilium, 84).<br><br>
                Click on any Hour below to see its structure and the fixed prayers you can pray along with. For the full texts of today's psalms, readings, and antiphons, use the external links at the bottom.
            </div>

            <h2 style="color: #8B4513; margin-bottom: 15px;">Choose an Hour to Pray:</h2>

            <div class="hour-grid" id="hourGrid">
                <div class="hour-card" onclick="showHour('office', this)">
                    <div class="hour-icon">🌙</div>
                    <h3>Office of Readings</h3>
                    <div class="hour-time">Any time (traditionally before dawn)</div>
                </div>
                <div class="hour-card" onclick="showHour('lauds', this)">
                    <div class="hour-icon">🌅</div>
                    <h3>Morning Prayer</h3>
                    <div class="hour-time">Lauds • ~6:00 AM</div>
                </div>
                <div class="hour-card" onclick="showHour('daytime', this)">
                    <div class="hour-icon">☀️</div>
                    <h3>Daytime Prayer</h3>
                    <div class="hour-time">Terce, Sext, None • 9 AM, Noon, 3 PM</div>
                </div>
                <div class="hour-card" onclick="showHour('vespers', this)">
                    <div class="hour-icon">🌇</div>
                    <h3>Evening Prayer</h3>
                    <div class="hour-time">Vespers • ~6:00 PM</div>
                </div>
                <div class="hour-card" onclick="showHour('compline', this)">
                    <div class="hour-icon">🌃</div>
                    <h3>Night Prayer</h3>
                    <div class="hour-time">Compline • Before bed</div>
                </div>
            </div>

            <div class="prayer-panel" id="prayerPanel" style="display:none;">
                <h2 id="hourTitle"></h2>
                <div class="subtitle" id="hourSubtitle"></div>
                <div id="hourContent"></div>
            </div>

            <div class="external-links">
                <h3>📿 Pray with Full Texts</h3>
                <p style="margin-bottom: 12px; color: #5a2c0c;">For the complete prayers of today, visit:</p>
                <a href="https://universalis.com" target="_blank" rel="noopener">Universalis</a>
                <a href="https://divineoffice.org" target="_blank" rel="noopener">DivineOffice.org</a>
                <a href="https://ibreviary.com" target="_blank" rel="noopener">iBreviary</a>
                <a href="https://www.liturgyhours.org" target="_blank" rel="noopener">LiturgyHours.org</a>
            </div>
        </div>

        <div class="footer">
            "Seven times a day I praise you." — Psalm 119:164<br>
            The Liturgy of the Hours is the public prayer of the Church.
        </div>
    </div>

    <script>
        const hourData = {
            office: {
                title: "Office of Readings",
                subtitle: "Traditionally prayed before dawn — opens the day with Scripture and the Fathers",
                content: `
                    <div class="prayer-step">
                        <h4>Opening Verse</h4>
                        <p><strong>V.</strong> O God, come to my assistance.<br>
                        <span class="response"><strong>R.</strong> O Lord, make haste to help me.</span></p>
                        <p class="glory-be">Glory be to the Father, and to the Son, and to the Holy Spirit. As it was in the beginning, is now, and ever shall be, world without end. Amen.</p>
                    </div>
                    <div class="prayer-step">
                        <h4>Hymn</h4>
                        <p class="rubric">A hymn appropriate to the season or feast is sung or recited.</p>
                    </div>
                    <div class="prayer-step">
                        <h4>Psalmody</h4>
                        <p>Three psalms (or parts of psalms), each followed by a psalm-prayer.</p>
                        <div class="antiphon">Antiphon: (varies by day) — recited before and after each psalm.</div>
                        <p class="glory-be">Glory be to the Father...</p>
                    </div>
                    <div class="prayer-step">
                        <h4>First Reading</h4>
                        <p>From Scripture (longer passage), followed by a responsory.</p>
                        <p class="rubric">A period of silent reflection may follow.</p>
                    </div>
                    <div class="prayer-step">
                        <h4>Second Reading</h4>
                        <p>From the Church Fathers, Doctors, or saints — followed by a responsory.</p>
                        <p class="rubric">On solemnities, the Te Deum may be said.</p>
                    </div>
                    <div class="prayer-step">
                        <h4>Concluding Prayer</h4>
                        <p>Proper to the day or feast.</p>
                        <p><strong>V.</strong> Let us praise the Lord.<br>
                        <span class="response"><strong>R.</strong> And give him thanks.</span></p>
                    </div>
                `
            },
            lauds: {
                title: "Morning Prayer (Lauds)",
                subtitle: "Prayed at dawn — consecrates the day to God",
                content: `
                    <div class="prayer-step">
                        <h4>Opening Verse</h4>
                        <p><strong>V.</strong> O God, come to my assistance.<br>
                        <span class="response"><strong>R.</strong> O Lord, make haste to help me.</span></p>
                        <p class="glory-be">Glory be to the Father, and to the Son, and to the Holy Spirit. As it was in the beginning, is now, and ever shall be, world without end. Amen.</p>
                    </div>
                    <div class="prayer-step">
                        <h4>Hymn</h4>
                        <p class="rubric">A morning hymn appropriate to the season.</p>
                    </div>
                    <div class="prayer-step">
                        <h4>Psalmody</h4>
                        <p>Psalm, canticle, psalm — each with its antiphon.</p>
                        <div class="antiphon">Antiphon: (varies by day)</div>
                        <p class="glory-be">Glory be to the Father...</p>
                    </div>
                    <div class="prayer-step">
                        <h4>Short Reading</h4>
                        <p>A brief Scripture passage (e.g., Romans 13:11-12).</p>
                    </div>
                    <div class="prayer-step">
                        <h4>Responsory</h4>
                        <p>A short response alternating between leader and people.</p>
                    </div>
                    <div class="prayer-step">
                        <h4>Canticle of Zechariah (Benedictus)</h4>
                        <p class="rubric">Luke 1:68-79 — said standing, with the sign of the cross at the beginning.</p>
                        <div class="antiphon">Antiphon: (varies by day)</div>
                        <p>Blessed be the Lord, the God of Israel; he has come to his people and set them free. He has raised up for us a mighty savior, born of the house of his servant David. Through his holy prophets he promised of old that he would save us from our enemies, from the hands of all who hate us. He promised to show mercy to our fathers and to remember his holy covenant. This was the oath he swore to our father Abraham: to set us free from the hands of our enemies, free to worship him without fear, holy and righteous in his sight all the days of our life.<br><br>
                        You, my child, shall be called the prophet of the Most High; for you will go before the Lord to prepare his way, to give his people knowledge of salvation by the forgiveness of their sins. In the tender compassion of our God the dawn from on high shall break upon us, to shine on those who dwell in darkness and the shadow of death, and to guide our feet into the way of peace.</p>
                        <p class="glory-be">Glory be to the Father...</p>
                    </div>
                    <div class="prayer-step">
                        <h4>Intercessions</h4>
                        <p>Prayers of petition for the day, the Church, and the world.</p>
                        <p><strong>V.</strong> Lord, hear our prayer.<br>
                        <span class="response"><strong>R.</strong> And let our cry come to you.</span></p>
                    </div>
                    <div class="prayer-step">
                        <h4>Lord's Prayer</h4>
                        <p>Our Father, who art in heaven, hallowed be thy name; thy kingdom come; thy will be done on earth as it is in heaven. Give us this day our daily bread; and forgive us our trespasses as we forgive those who trespass against us; and lead us not into temptation, but deliver us from evil.</p>
                    </div>
                    <div class="prayer-step">
                        <h4>Concluding Prayer & Blessing</h4>
                        <p>Then the collect proper to the day.</p>
                        <p><strong>V.</strong> May the Lord bless us, protect us from all evil, and bring us to everlasting life.<br>
                        <span class="response"><strong>R.</strong> Amen.</span></p>
                    </div>
                `
            },
            daytime: {
                title: "Daytime Prayer",
                subtitle: "Terce (9 AM) • Sext (Noon) • None (3 PM) — sanctifying the work of the day",
                content: `
                    <div class="prayer-step">
                        <h4>About Daytime Prayer</h4>
                        <p>Daytime Prayer is shorter, meant to be prayed during work hours. It is prayed at mid-morning (Terce), noon (Sext), and mid-afternoon (None).</p>
                    </div>
                    <div class="prayer-step">
                        <h4>Opening Verse</h4>
                        <p><strong>V.</strong> O God, come to my assistance.<br>
                        <span class="response"><strong>R.</strong> O Lord, make haste to help me.</span></p>
                        <p class="glory-be">Glory be to the Father...</p>
                    </div>
                    <div class="prayer-step">
                        <h4>Hymn</h4>
                        <p class="rubric">A hymn appropriate to the hour.</p>
                    </div>
                    <div class="prayer-step">
                        <h4>Three Psalms</h4>
                        <p>Each with an antiphon and the Glory Be.</p>
                        <p class="rubric">On Sundays, the psalms are of the day.</p>
                    </div>
                    <div class="prayer-step">
                        <h4>Short Reading & Responsory</h4>
                        <p>A brief Scripture passage followed by a short response.</p>
                    </div>
                    <div class="prayer-step">
                        <h4>Concluding Prayer</h4>
                        <p>Proper to the hour or day.</p>
                        <p><strong>V.</strong> Let us praise the Lord.<br>
                        <span class="response"><strong>R.</strong> And give him thanks.</span></p>
                    </div>
                `
            },
            vespers: {
                title: "Evening Prayer (Vespers)",
                subtitle: "Prayed at sunset — the Church's evening sacrifice of praise",
                content: `
                    <div class="prayer-step">
                        <h4>Opening Verse</h4>
                        <p><strong>V.</strong> O God, come to my assistance.<br>
                        <span class="response"><strong>R.</strong> O Lord, make haste to help me.</span></p>
                        <p class="glory-be">Glory be to the Father...</p>
                    </div>
                    <div class="prayer-step">
                        <h4>Hymn</h4>
                        <p class="rubric">An evening hymn appropriate to the season.</p>
                    </div>
                    <div class="prayer-step">
                        <h4>Psalmody</h4>
                        <p>Psalm, psalm, canticle (often from Revelation or the epistles).</p>
                        <div class="antiphon">Antiphon: (varies by day)</div>
                        <p class="glory-be">Glory be to the Father...</p>
                    </div>
                    <div class="prayer-step">
                        <h4>Short Reading</h4>
                        <p>A brief Scripture passage, often from the epistles.</p>
                    </div>
                    <div class="prayer-step">
                        <h4>Canticle of Mary (Magnificat)</h4>
                        <p class="rubric">Luke 1:46-55 — said standing, with the sign of the cross at the beginning.</p>
                        <div class="antiphon">Antiphon: (varies by day)</div>
                        <p>My soul proclaims the greatness of the Lord, my spirit rejoices in God my Savior; for he has looked with favor on his lowly servant. From this day all generations will call me blessed: the Almighty has done great things for me, and holy is his Name. He has mercy on those who fear him in every generation. He has shown the strength of his arm, he has scattered the proud in their conceit. He has cast down the mighty from their thrones, and has lifted up the lowly. He has filled the hungry with good things, and the rich he has sent away empty. He has come to the help of his servant Israel for he has remembered his promise of mercy, the promise he made to our fathers, to Abraham and his children for ever.</p>
                        <p class="glory-be">Glory be to the Father...</p>
                    </div>
                    <div class="prayer-step">
                        <h4>Intercessions</h4>
                        <p>Prayers of petition for the day, the Church, and the world.</p>
                        <p><strong>V.</strong> Lord, hear our prayer.<br>
                        <span class="response"><strong>R.</strong> And let our cry come to you.</span></p>
                    </div>
                    <div class="prayer-step">
                        <h4>Lord's Prayer</h4>
                        <p>Our Father, who art in heaven, hallowed be thy name; thy kingdom come; thy will be done on earth as it is in heaven. Give us this day our daily bread; and forgive us our trespasses as we forgive those who trespass against us; and lead us not into temptation, but deliver us from evil.</p>
                    </div>
                    <div class="prayer-step">
                        <h4>Concluding Prayer & Blessing</h4>
                        <p>Then the collect proper to the day.</p>
                        <p><strong>V.</strong> May the Lord bless us, protect us from all evil, and bring us to everlasting life.<br>
                        <span class="response"><strong>R.</strong> Amen.</span></p>
                    </div>
                `
            },
            compline: {
                title: "Night Prayer (Compline)",
                subtitle: "The last prayer before sleep — entrusting the night to God",
                content: `
                    <div class="prayer-step">
                        <h4>Opening Verse</h4>
                        <p><strong>V.</strong> O God, come to my assistance.<br>
                        <span class="response"><strong>R.</strong> O Lord, make haste to help me.</span></p>
                        <p class="glory-be">Glory be to the Father...</p>
                    </div>
                    <div class="prayer-step">
                        <h4>Examination of Conscience</h4>
                        <p class="rubric">A brief pause to reflect on the day's sins and blessings.</p>
                    </div>
                    <div class="prayer-step">
                        <h4>Hymn</h4>
                        <p class="rubric">A hymn appropriate for night.</p>
                    </div>
                    <div class="prayer-step">
                        <h4>Psalmody</h4>
                        <p>One or two psalms, chosen for their themes of trust and protection.</p>
                        <div class="antiphon">Antiphon: (varies by day)</div>
                        <p class="glory-be">Glory be to the Father...</p>
                    </div>
                    <div class="prayer-step">
                        <h4>Short Reading</h4>
                        <p>Often from 1 Peter 5:8-9 or similar.</p>
                    </div>
                    <div class="prayer-step">
                        <h4>Responsory</h4>
                        <p><strong>V.</strong> Into your hands, Lord, I commend my spirit.<br>
                        <span class="response"><strong>R.</strong> Into your hands, Lord, I commend my spirit.</span></p>
                    </div>
                    <div class="prayer-step">
                        <h4>Canticle of Simeon (Nunc Dimittis)</h4>
                        <p class="rubric">Luke 2:29-32 — said standing, with the sign of the cross at the beginning.</p>
                        <div class="antiphon">Antiphon: (varies by day)</div>
                        <p>Lord, now you let your servant go in peace; your word has been fulfilled: my own eyes have seen the salvation which you have prepared in the sight of every people: a light to reveal you to the nations and the glory of your people Israel.</p>
                        <p class="glory-be">Glory be to the Father...</p>
                    </div>
                    <div class="prayer-step">
                        <h4>Concluding Prayer</h4>
                        <p>Proper to the day.</p>
                    </div>
                    <div class="prayer-step">
                        <h4>Final Antiphon to the Blessed Virgin Mary</h4>
                        <p class="rubric">One of four antiphons is said, depending on the season:</p>
                        <div class="antiphon">
                            <strong>Alma Redemptoris Mater</strong> (Advent–Feb 2)<br>
                            <strong>Ave Regina Caelorum</strong> (Feb 3–Wednesday of Holy Week)<br>
                            <strong>Regina Caeli</strong> (Easter–Pentecost)<br>
                            <strong>Salve Regina</strong> (Pentecost–Advent)
                        </div>
                    </div>
                    <div class="prayer-step">
                        <h4>Blessing</h4>
                        <p><strong>V.</strong> May the all-powerful Lord grant us a restful night and a peaceful death.<br>
                        <span class="response"><strong>R.</strong> Amen.</span></p>
                        <p class="rubric">Then the invocation of the Blessed Virgin Mary, followed by the sign of the cross.</p>
                    </div>
                `
            }
        };

        function showHour(hourKey, cardElement) {
            // Highlight selected card
            document.querySelectorAll('.hour-card').forEach(c => c.classList.remove('selected'));
            cardElement.classList.add('selected');

            const data = hourData[hourKey];
            document.getElementById('hourTitle').innerHTML = data.title;
            document.getElementById('hourSubtitle').innerHTML = data.subtitle;
            document.getElementById('hourContent').innerHTML = data.content;
            document.getElementById('prayerPanel').style.display = 'block';

            // Smooth scroll to the panel
            document.getElementById('prayerPanel').scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    </script>
</body>
</html>
'''

# ============================================================
# ROUTES
# ============================================================
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/liturgy')
def liturgy():
    return render_template_string(LITURGY_TEMPLATE)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    request_type = data.get('type', 'question')
    content = data.get('content', '')

    if request_type == 'prayer':
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
            return jsonify({'answer': f"🙏 **Your Prayer** 🙏\\n\\n{prayer}\\n\\n---\\n*May God bless you and answer your intention.*"})
        except Exception as e:
            return jsonify({'answer': f"Error generating prayer: {e}"})

    else:
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