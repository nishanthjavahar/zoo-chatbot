from flask import Flask, render_template, request, jsonify
import json
import os
from openai import OpenAI

app = Flask(__name__)

# ✅ Load animal data
with open("data/animals.json") as f:
    animals = json.load(f)

# ✅ Secure API key (use environment variable)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🏠 Home route
@app.route("/")
def home():
    return render_template("index.html")


# 💬 Chat route
@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_msg = request.json.get("message", "").lower()

        if not user_msg:
            return jsonify({"reply": "Please enter a message."})

        # 🧠 Rule-based response (fast + reliable)
        for animal in animals:
            if animal in user_msg:
                info = animals[animal]

                return jsonify({
                    "reply": f"{info['name']} is a {info['diet']} animal located in {info['location']}. Fun fact: {info['fact']}",
                    "image": f"/static/images/{animal}.jpg"
                })

        # 🤖 AI fallback
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful zoo assistant. Keep answers short and informative."},
                {"role": "user", "content": user_msg}
            ]
        )

        return jsonify({
            "reply": response.choices[0].message.content,
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