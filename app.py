from flask import Flask, render_template, request, jsonify
import os
from pymongo import MongoClient

app = Flask(__name__)

# ✅ MongoDB connection
mongo_uri = os.getenv("MONGO_URI")

if not mongo_uri:
    raise Exception("MONGO_URI is missing")

client_db = MongoClient(mongo_uri)
db = client_db["zoo"]
animals_collection = db["animals"]


# 🧠 Offline smart response function
def get_zoo_response(user_input):
    user_input = user_input.lower()

    # 🦁 Animals (fallback if not in DB)
    if "lion" in user_input:
        return "🦁 Lion is known as the king of the jungle. It lives in groups called prides."

    elif "tiger" in user_input:
        return "🐯 Tigers are powerful solitary animals and excellent swimmers."

    elif "elephant" in user_input:
        return "🐘 Elephants are the largest land animals and have strong memory."

    elif "giraffe" in user_input:
        return "🦒 Giraffes are the tallest animals and have long necks to reach tall trees."

    elif "zebra" in user_input:
        return "🦓 Zebras have unique black and white stripes, no two are alike."

    # 📍 Directions
    elif "washroom" in user_input or "toilet" in user_input:
        return "🚻 Washrooms are located near the entrance."

    elif "food" in user_input or "restaurant" in user_input:
        return "🍔 Food court is available near the central zone."

    elif "exit" in user_input:
        return "🚪 Exit is near the main gate."

    elif "location" in user_input or "where am i" in user_input:
        return "📍 You are inside the zoo. Check nearby signboards for directions."

    # 🕒 General info
    elif "timing" in user_input or "time" in user_input:
        return "⏰ Zoo is open from 9 AM to 5 PM."

    elif "ticket" in user_input or "price" in user_input:
        return "🎟️ Tickets are available at the entrance counter."

    else:
        return "🌿 I can help with animals, directions, and facilities inside the zoo."


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

        # ✅ 1. Try MongoDB first
        animal = animals_collection.find_one({
            "name": {"$regex": user_msg, "$options": "i"}
        })

        if animal:
            return jsonify({
                "reply": f"🦁 {animal['name']} is a {animal['diet']} found in {animal['location']}. Fun fact: {animal['fact']}",
                "image": None
            })

        # ✅ 2. Fallback to offline logic
        response = get_zoo_response(user_msg)

        return jsonify({
            "reply": response,
            "image": None
        })

    except Exception as e:
        print("CHAT ERROR:", str(e))
        return jsonify({
            "reply": "⚠️ Something went wrong. Please try again.",
            "image": None
        })


# 🌐 Vercel handler
def handler(request, response):
    return app(request.environ, lambda *args: None)