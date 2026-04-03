from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI
from pymongo import MongoClient

app = Flask(__name__)

# ✅ MongoDB connection (CLEAN)
mongo_uri = os.getenv("MONGO_URI")

if not mongo_uri:
    raise Exception("MONGO_URI is missing")

client_db = MongoClient(mongo_uri)
db = client_db["zoo"]
animals_collection = db["animals"]

# ✅ OpenAI client
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
            return jsonify({"reply": "Please enter a message.", "image": None})

        # ✅ Mongo search
        animal = animals_collection.find_one({
            "name": {"$regex": user_msg, "$options": "i"}
        })

        if animal:
            return jsonify({
                "reply": f"{animal['name']} is a {animal['diet']} located in {animal['location']}. Fun fact: {animal['fact']}",
                "image": None
            })

        # 🤖 AI fallback
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a zoo assistant."},
                {"role": "user", "content": user_msg}
            ]
        )

        return jsonify({
            "reply": response.choices[0].message.content,
            "image": None
        })

    except Exception as e:
        print("CHAT ERROR:", str(e))
        return jsonify({
            "reply": f"Error: {str(e)}",
            "image": None
        })


# 🌐 Vercel handler
def handler(request, response):
    return app(request.environ, lambda *args: None)