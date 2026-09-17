from flask import Flask, request, jsonify, render_template_string
import requests, os

app = Flask(__name__)
GEMINI_KEY = os.getenv("GEMINI_KEY") # GitHub secret la irunthu varum

HTML_PAGE = """
<html><body style="font-family:sans-serif; text-align:center; padding:50px">
<h1>En AI Bot Ready Da! 🔥</h1>
<input id="q" placeholder="Enna venum kelu da - Tamil/English la" style="width:80%; padding:10px">
<button onclick="ask()" style="padding:10px">Kelu</button>
<p id="ans"></p>
<script>
async function ask(){
 let q=document.getElementById('q').value;
 let r=await fetch('/chat?q='+q);
 let d=await r.json();
 document.getElementById('ans').innerText=d.answer;
}
</script></body></html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/chat")
def chat():
    user_q = request.args.get("q")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    payload = {"contents": [{"parts": [{"text": f"Answer in same language user asked. Question: {user_q}"}]}]}
    res = requests.post(url, json=payload).json()
    try:
        answer = res["candidates"][0]["content"]["parts"][0]["text"]
    except:
        answer = "Sorry da, konjam thappu aayiduchu, thirimba try pannu"
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
