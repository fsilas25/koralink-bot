from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import re

app = Flask(__name__)
CORS(app)

FAQ_FILE = "faqs_final.json"
# Stop words list to improve matching accuracy
STOP_WORDS = {"is", "a", "the", "what", "how", "i", "do", "does", "to", "in", "my", "of", "can", "are", "you"}

def load_faq_data():
    """Loads the FAQ JSON file into memory."""
    if os.path.exists(FAQ_FILE):
        with open(FAQ_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"Successfully loaded {len(data)} FAQ entries from {FAQ_FILE}.")
            return data
    else:
        print(f"Error: {FAQ_FILE} not found. Please ensure the file exists.")
        return []

# Initialize data
faq_data = load_faq_data()

def get_tokens(text):
    """Tokenizes text and removes stop words."""
    words = re.findall(r'\w+', text.lower())
    return [w for w in words if w not in STOP_WORDS]

def find_answer(user_message):
    """Matches user input to the best FAQ entry based on token overlap."""
    user_tokens = set(get_tokens(user_message))
    if not user_tokens:
        return "I'm sorry, I didn't catch that. Could you please rephrase your question about KoraLink?"

    best_score = 0
    best_answer = "I am not sure about that. Please contact KoraLink support or visit https://koralink.org/rw for help."

    for item in faq_data:
        # Check all question variations for this entry
        for question in item.get("questions", []):
            q_tokens = set(get_tokens(question))
            # Calculate intersection score
            score = len(user_tokens & q_tokens)
            
            if score > best_score:
                best_score = score
                best_answer = item["answer"]

    # Only return if we have a reasonable keyword match
    return best_answer if best_score >= 1 else best_answer

@app.route("/chat", methods=["POST"])
def chat():
    """Endpoint for chatbot interaction."""
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"response": "Please provide a 'message' key in your JSON request."}), 400
    
    message = data["message"]
    answer = find_answer(message)
    return jsonify({"response": answer})

if __name__ == "__main__":
    app.run(debug=True)