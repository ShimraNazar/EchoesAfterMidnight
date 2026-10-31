from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "tinyllama:1.1b"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Echoes After Midnight</title>

<link href="https://fonts.googleapis.com/css2?family=Creepster&family=Special+Elite&family=IM+Fell+English:ital@0;1&display=swap" rel="stylesheet">

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --red: #ff263b;
    --dark-red: #79000c;
    --moon: #cbdcff;
    --text: #eee5e8;
}

body {
    min-height: 100vh;
    background: #03050b;
    color: var(--text);
    font-family: 'IM Fell English', serif;
    overflow-x: hidden;
}

/* HAUNTED BACKGROUND */

.background {
    position: fixed;
    inset: 0;
    z-index: -5;
    background:
        linear-gradient(to bottom, rgba(1,3,10,.35), rgba(1,3,10,.72)),
        url("https://static.wixstatic.com/media/bbdbfa_7dadff22344843718ba75924072ebd15~mv2.png/v1/fill/w_980%2Ch_653%2Cal_c%2Cq_90%2Cusm_0.66_1.00_0.01%2Cenc_avif%2Cquality_auto/bbdbfa_7dadff22344843718ba75924072ebd15~mv2.png");
    background-size: cover;
    background-position: center;
    animation: backgroundZoom 35s ease-in-out infinite alternate;
}

@keyframes backgroundZoom {
    from { transform: scale(1); }
    to { transform: scale(1.09); }
}

.background::after {
    content: "";
    position: absolute;
    inset: 0;
    background:
        radial-gradient(circle at 78% 25%, transparent 0%, rgba(0,0,0,.15) 35%, #02040a 100%);
}

/* DARK CINEMATIC OVERLAY */

.dark-overlay {
    position: fixed;
    inset: 0;
    z-index: -4;
    background: linear-gradient(90deg,
        rgba(0,0,0,.25),
        rgba(0,0,0,.48) 45%,
        rgba(0,0,0,.22));
}

/* MOON */

.moon {
    position: fixed;
    z-index: -3;
    width: 190px;
    height: 190px;
    top: 7%;
    right: 9%;
    border-radius: 50%;
    background:
        radial-gradient(circle at 35% 30%, #fff 0%, #dce8ff 35%, #8195b8 75%, #34445f 100%);
    box-shadow:
        0 0 25px #b7d4ff,
        0 0 65px rgba(135,174,255,.55),
        0 0 130px rgba(111,151,255,.28);
    opacity: .72;
    animation: moonGlow 5s ease-in-out infinite alternate;
}

.moon::before {
    content: "";
    position: absolute;
    width: 35px;
    height: 35px;
    top: 40px;
    left: 45px;
    border-radius: 50%;
    background: rgba(65,83,116,.17);
    box-shadow:
        45px 35px 0 5px rgba(65,83,116,.12),
        -10px 85px 0 2px rgba(65,83,116,.12);
}

@keyframes moonGlow {
    from {
        box-shadow: 0 0 25px #b7d4ff, 0 0 65px rgba(135,174,255,.4);
    }
    to {
        box-shadow: 0 0 40px #d4e4ff, 0 0 110px rgba(135,174,255,.65);
    }
}

/* FOG */

.fog {
    position: fixed;
    z-index: -2;
    left: -20%;
    bottom: 0;
    width: 140%;
    height: 38%;
    pointer-events: none;
    background:
        radial-gradient(ellipse at 20% 70%, rgba(174,196,220,.17), transparent 55%),
        radial-gradient(ellipse at 70% 80%, rgba(150,176,210,.16), transparent 60%);
    filter: blur(25px);
    animation: fogMove 18s ease-in-out infinite alternate;
}

.fog.second {
    bottom: 10%;
    opacity: .45;
    animation-duration: 25s;
    animation-direction: alternate-reverse;
}

@keyframes fogMove {
    from { transform: translateX(-5%) translateY(10px); }
    to { transform: translateX(7%) translateY(-18px); }
}

/* FLOATING GHOST */

.ghost {
    position: fixed;
    z-index: -1;
    right: 12%;
    top: 20%;
    font-size: 125px;
    opacity: .18;
    filter: blur(1px) drop-shadow(0 0 18px #a9c8ff);
    animation: ghostFloat 7s ease-in-out infinite;
    pointer-events: none;
}

@keyframes ghostFloat {
    0%, 100% {
        transform: translateY(0) rotate(-4deg);
        opacity: .13;
    }
    50% {
        transform: translateY(-30px) rotate(4deg);
        opacity: .25;
    }
}

/* NAVBAR */

.navbar {
    height: 47px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 22px;
    background: rgba(0,0,0,.72);
    border-bottom: 1px solid rgba(255,255,255,.13);
    box-shadow: 0 3px 20px rgba(0,0,0,.5);
}

.brand {
    font-family: 'IM Fell English', serif;
    font-size: 19px;
    font-style: italic;
    letter-spacing: .5px;
}

.brand span {
    color: var(--red);
}

.brand-icon {
    color: #fff;
    font-size: 25px;
    margin-right: 10px;
    filter: drop-shadow(0 0 7px #b7d4ff);
}

.nav-quote {
    color: #aaa0a9;
    font-size: 13px;
    font-style: italic;
}

/* MAIN CONTENT */

.container {
    width: min(100% - 30px, 550px);
    margin: 10px auto 40px;
    animation: appear 1.4s ease both;
}

@keyframes appear {
    from { opacity: 0; transform: translateY(25px); }
    to { opacity: 1; transform: translateY(0); }
}

/* HEADING */

.heading {
    text-align: center;
    margin: 0 auto 20px;
}

.heading h1 {
    font-family: 'Creepster', cursive;
    font-size: clamp(43px, 8vw, 69px);
    font-weight: normal;
    line-height: 1.15;
    color: #f3eeee;
    letter-spacing: 1px;
    text-shadow:
        0 2px 2px #000,
        0 0 12px rgba(255,255,255,.35),
        0 0 28px rgba(255,0,25,.28);
    animation: titleGlow 4s ease-in-out infinite alternate;
}

.heading h1 span {
    color: #d20b23;
    text-shadow: 0 0 15px rgba(255,0,25,.65);
}

@keyframes titleGlow {
    from { text-shadow: 0 0 10px rgba(255,255,255,.2), 0 0 20px rgba(255,0,25,.15); }
    to { text-shadow: 0 0 16px rgba(255,255,255,.5), 0 0 35px rgba(255,0,25,.4); }
}

.subtitle {
    font-size: 17px;
    color: #e0d6df;
    margin-top: 4px;
    letter-spacing: .4px;
}

.subtitle::before,
.subtitle::after {
    content: "";
    display: inline-block;
    width: 45px;
    height: 1px;
    vertical-align: middle;
    margin: 0 12px;
    background: linear-gradient(90deg, transparent, var(--red));
}

/* GENERATOR PANEL */

.panel {
    position: relative;
    padding: 20px 24px 18px;
    background: rgba(5,4,9,.88);
    border: 1px solid #b20b20;
    border-radius: 15px;
    box-shadow:
        0 0 8px rgba(255,0,25,.6),
        0 0 25px rgba(160,0,20,.25),
        inset 0 0 35px rgba(100,0,10,.13);
    backdrop-filter: blur(9px);
    animation: panelGlow 4s ease-in-out infinite alternate;
}

@keyframes panelGlow {
    from {
        box-shadow: 0 0 8px rgba(255,0,25,.35), 0 0 22px rgba(160,0,20,.15), inset 0 0 35px rgba(100,0,10,.1);
    }
    to {
        box-shadow: 0 0 15px rgba(255,0,25,.65), 0 0 35px rgba(160,0,20,.3), inset 0 0 35px rgba(100,0,10,.2);
    }
}

.panel-top {
    text-align: center;
    color: #ff9ca5;
    font-size: 15px;
    margin-bottom: 18px;
}

.skull-divider {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    margin-bottom: 8px;
    color: #ff3448;
    font-size: 20px;
    text-shadow: 0 0 10px red;
}

.skull-divider::before,
.skull-divider::after {
    content: "";
    height: 1px;
    flex: 1;
    background: linear-gradient(90deg, transparent, #bd1729, transparent);
}

/* FORM */

label {
    display: block;
    margin-bottom: 7px;
    font-size: 14px;
    color: #eee5e8;
}

.label-icon {
    color: #ff3448;
    margin-right: 7px;
}

textarea,
select {
    width: 100%;
    color: #f1e9ed;
    background: rgba(22,18,26,.9);
    border: 1px solid #42333e;
    border-radius: 8px;
    outline: none;
    font-family: 'IM Fell English', serif;
    font-size: 14px;
    transition: .3s ease;
}

textarea {
    height: 78px;
    padding: 12px;
    resize: vertical;
    margin-bottom: 16px;
}

textarea::placeholder {
    color: #8c818d;
}

textarea:focus,
select:focus {
    border-color: #e52b40;
    box-shadow: 0 0 12px rgba(255,0,30,.22);
}

.select-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 25px;
}

select {
    height: 39px;
    padding: 0 10px;
    cursor: pointer;
}

select option {
    background: #151019;
    color: white;
}

/* GENERATE BUTTON */

.generate-btn {
    display: block;
    position: relative;
    overflow: hidden;
    margin: 23px auto 18px;
    min-width: 270px;
    padding: 13px 25px;
    color: white;
    font-family: 'IM Fell English', serif;
    font-size: 18px;
    border: 1px solid #ff263b;
    border-radius: 9px;
    cursor: pointer;
    background:
        linear-gradient(110deg, #3b0008, #a00014 48%, #310006);
    box-shadow:
        0 0 10px rgba(255,0,25,.7),
        inset 0 0 15px rgba(255,0,25,.25);
    text-shadow: 0 1px 4px #000;
    transition: .3s ease;
    animation: buttonPulse 2.5s infinite;
}

.generate-btn:hover {
    transform: translateY(-3px) scale(1.025);
    background: linear-gradient(110deg, #72000d, #d00020, #65000b);
    box-shadow: 0 0 25px rgba(255,0,30,.85);
}

.generate-btn:active {
    transform: scale(.97);
}

.generate-btn:disabled {
    opacity: .65;
    cursor: wait;
    animation: none;
}

@keyframes buttonPulse {
    0%, 100% { box-shadow: 0 0 8px rgba(255,0,25,.45), inset 0 0 15px rgba(255,0,25,.2); }
    50% { box-shadow: 0 0 19px rgba(255,0,25,.8), inset 0 0 20px rgba(255,0,25,.3); }
}

.generate-btn span {
    margin-right: 9px;
    font-size: 22px;
    vertical-align: middle;
}

/* STORY OUTPUT */

.story-divider {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 15px 0 12px;
    color: #ff3347;
    font-size: 20px;
}

.story-divider::before,
.story-divider::after {
    content: "";
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, #a20b1c, transparent);
}

.story-label {
    margin-bottom: 8px;
}

.story-box {
    min-height: 67px;
    max-height: 420px;
    overflow-y: auto;
    padding: 12px;
    color: #d9cbd2;
    font-family: 'Special Elite', cursive;
    font-size: 14px;
    line-height: 1.8;
    white-space: pre-wrap;
    background: rgba(22,14,22,.82);
    border: 1px solid #67101c;
    border-radius: 9px;
    box-shadow: inset 0 0 20px rgba(130,0,15,.12);
}

.placeholder {
    color: #827580;
    font-style: italic;
}

.error {
    color: #ff7885;
    text-align: center;
    margin: 12px 0;
    font-size: 14px;
}

/* LOADING EFFECT */

.loading-text {
    color: #ff8c99;
    text-align: center;
    margin: 10px 0;
    font-size: 14px;
    animation: loadingBlink 1.2s infinite;
}

@keyframes loadingBlink {
    50% { opacity: .35; }
}

/* FOOTER */

.footer {
    text-align: center;
    color: rgba(220,210,220,.55);
    font-size: 12px;
    margin-top: 18px;
    letter-spacing: 1px;
}

.footer span {
    color: #e42b40;
}

/* RESPONSIVE */

@media (max-width: 600px) {
    .navbar {
        padding: 0 12px;
    }

    .nav-quote {
        font-size: 11px;
    }

    .container {
        margin-top: 25px;
    }

    .heading h1 {
        font-size: 43px;
    }

    .subtitle {
        font-size: 14px;
    }

    .subtitle::before,
    .subtitle::after {
        width: 20px;
        margin: 0 5px;
    }

    .panel {
        padding: 18px 15px;
    }

    .select-row {
        gap: 12px;
    }

    .moon {
        width: 120px;
        height: 120px;
        right: 4%;
        top: 10%;
        opacity: .4;
    }

    .ghost {
        font-size: 75px;
        right: 4%;
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: .01ms !important;
        animation-iteration-count: 1 !important;
        scroll-behavior: auto !important;
    }
}
</style>
</head>

<body>

<div class="background"></div>
<div class="dark-overlay"></div>
<div class="moon"></div>
<div class="fog"></div>
<div class="fog second"></div>


<nav class="navbar">
    <div class="brand">
        <span class="brand-icon">👻</span>
        Echoes <span>After</span> Midnight
    </div>
    <div class="nav-quote">Let the past whisper...</div>
</nav>

<main class="container">

    <header class="heading">
        <h1>Echoes <span>After</span> Midnight</h1>
        <p class="subtitle">An AI-Powered Ghost Story Generator</p>
    </header>

    <section class="panel">

        <div class="panel-top">
            <div class="skull-divider">☠</div>
            Enter a creepy idea... and let the shadows speak.
        </div>

        <form method="POST" id="storyForm">

            <label for="idea">
                <span class="label-icon">✎</span>
                Your Story Idea
            </label>

            <textarea
                id="idea"
                name="idea"
                placeholder="e.g. A student hears footsteps in an abandoned university..."
                required
            >{{ idea }}</textarea>

            <div class="select-row">

                <div>
                    <label for="setting">
                        <span class="label-icon">⌂</span>
                        Choose a Setting
                    </label>

                    <select name="setting" id="setting">
                        <option>Haunted Mansion</option>
                        <option>Abandoned University</option>
                        <option>Dark Forest</option>
                        <option>Forgotten Cemetery</option>
                        <option>Deserted Hospital</option>
                        <option>Empty Village</option>
                        <option>Old Railway Station</option>
                    </select>
                </div>

                <div>
                    <label for="level">
                        <span class="label-icon">♨</span>
                        Horror Level
                    </label>

                    <select name="level" id="level">
                        <option>Mysterious</option>
                        <option>Medium</option>
                        <option>Terrifying</option>
                        <option>Nightmare</option>
                    </select>
                </div>

            </div>

            <button type="submit" class="generate-btn" id="generateBtn">
                <span>👻</span> Generate My Ghost Story
            </button>

        </form>

        <div id="loading" class="loading-text" style="display:none;">
            The shadows are writing your story...
        </div>

        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}

        <div class="story-divider">☠</div>

        <label class="story-label">
            <span class="label-icon">▣</span>
            Your Story
        </label>

        <div class="story-box" id="storyBox">
            {% if story %}
                {{ story }}
            {% else %}
                <span class="placeholder">Your chilling story will appear here...</span>
            {% endif %}
        </div>

    </section>

    <footer class="footer">
        CREATED IN THE DARK <span>✦</span> POWERED BY TINYLLAMA AI
    </footer>

</main>

<script>
const form = document.getElementById("storyForm");
const button = document.getElementById("generateBtn");
const loading = document.getElementById("loading");

form.addEventListener("submit", function() {
    button.disabled = true;
    button.innerHTML = "<span>☠</span> Summoning the Shadows...";
    loading.style.display = "block";
});
</script>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    story = ""
    error = ""
    idea = ""

    if request.method == "POST":
        idea = request.form.get("idea", "").strip()
        setting = request.form.get("setting", "Haunted Mansion")
        level = request.form.get("level", "Medium")

        prompt = f"""
You are an expert horror fiction writer.

Write an engaging and terrifying horror story based on:

Story idea: {idea}
Setting: {setting}
Horror level: {level}

STORY REQUIREMENTS:

- Write a detailed story of approximately 700 words.
- Create an interesting title.
- Develop the main character and the setting.
- Start with a mysterious and engaging introduction.
- Build suspense gradually throughout the story.
- Include realistic dialogue and detailed descriptions.
- Make the frightening events logically connected.
- Create a powerful climax.
- Include an unexpected and disturbing final twist.
- Finish with a complete and satisfying horror ending.
- Do not repeat events or descriptions.
- Do not introduce unrelated characters or events.
- Do not end with a moral lesson or a happy ending.

IMPORTANT:
Write one continuous, complete horror story.
Do not summarize the story.
Do not stop before the final ending.
Finish with a complete final sentence.

Begin the story:
"""

        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.8,
                        "num_predict": 900
                    }
                },
                timeout=240
            )

            response.raise_for_status()
            story = response.json().get("response", "").strip()

            if not story:
                error = "The AI could not create a story. Please try again."

        except requests.exceptions.ConnectionError:
            error = "Cannot connect to Ollama. Make sure Ollama is running."

        except requests.exceptions.Timeout:
            error = "The AI is taking too long. Please try again."

        except requests.exceptions.RequestException:
            error = "Something went wrong while generating your story."

    return render_template_string(
        HTML,
        story=story,
        error=error,
        idea=idea
    )


if __name__ == "__main__":
    app.run(debug=True)