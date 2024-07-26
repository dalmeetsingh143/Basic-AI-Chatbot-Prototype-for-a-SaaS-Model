from flask import Flask, request, jsonify, send_from_directory
import json
import spacy
import os

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

# Defining the path to the JSON file
faqs_path = "/Users/dalmeet/Robotics/ai_chatbot/database/faqs.json"

# Checking if the JSON file exists
if not os.path.exists(faqs_path):
    raise FileNotFoundError(f"The file {faqs_path} does not exist.")

# Loading FAQs
with open(faqs_path, "r") as file:
    data = json.load(file)

greetings = data["greetings"]
farewells = data["farewells"]
faqs = data["faqs"]

# NLP function to find the best matching FAQ
def find_faq(query):
    doc = nlp(query.lower())
    for faq, answer in faqs.items():
        if doc.similarity(nlp(faq)) > 0.75:
            return answer
    return "I'm sorry, I didn't understand. Please re-type correctly or contact customer support (0123-456-789) for further assistance."

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    
    # Checking for greetings
    if user_input.lower() in greetings:
        return jsonify({"response": "Hello! How can I assist you today?"})
    
    # Checking for farewells
    elif user_input.lower() in farewells:
        return jsonify({"response": "Goodbye! Have a great day."})
    
    # Finding FAQ answer
    else:
        response = find_faq(user_input)
        return jsonify({"response": response})

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5003)
