from flask import Flask, render_template, request, jsonify
import json
import os
from openai import OpenAI

app = Flask(__name__)

# ✅ Load animal data
with open("data/animals.json") as f:
    animals = json.load(f)

# ✅ OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Chat memory (simple global memory)
chat_history = [
    {
        "role": "system",
        "content": """
You are ZooAssist AI, a smart zoo guide.

Rules:
- Give short, accurate answers
- Prefer zoo database info when possible
- If user asks directions → explain clearly
- If unknown → say politely
- Add 1 fun fact when possible
"""
    }
]

# 🏠 Home route
@app.route("/")
def home():
    return render_template("index.html")


# 💬 Chat route
@app.route("/chat", methods=["POST"])
def chat():
    global chat_history

    try:
        user_msg = request.json.get("message", "").lower()

        if not user_msg:
            return jsonify({"reply": "Please enter a message.", "image": None})

        # 🧠 Intent Detection
        if "where" in user_msg or "location" in user_msg:
            return jsonify({
                "reply": "Use the 📍 button to find nearby animals!",
                "image": None
            })

        if "ticket" in user_msg:
            return jsonify({
                "reply": "Tickets are available at the entrance from 9 AM to 5 PM.",
                "image": None
            })

        # 🐾 Rule-based animal response
        for animal in animals:
            if animal in user_msg:
                info = animals[animal]

                return jsonify({
                    "reply": f"{info['name']} is a {info['diet']} animal located in {info['location']}. Fun fact: {info['fact']}",
                    "image": f"/static/images/{animal}.jpg"
                })

        # 🧠 Add user message to memory
        chat_history.append({
            "role": "user",
            "content": user_msg
        })

        # 🤖 AI fallback with memory
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=chat_history
        )

        reply = response.choices[0].message.content

        # 🧠 Store AI response
        chat_history.append({
            "role": "assistant",
            "content": reply
        })

        return jsonify({
            "reply": reply,
            "image": None
        })

    except Exception as e:
        return jsonify({
            "reply": f"⚠️ Error: {str(e)}",
            "image": None
        })


# 🚀 Run locally
if __name__ == "__main__":
    app.run(debug=True)


# 🌐 Vercel handler
def handler(request, response):
    return app(request.environ, lambda *args: None)