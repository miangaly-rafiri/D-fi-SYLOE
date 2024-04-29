from flask import Flask, request, jsonify
from profanity_check import predict

app = Flask(__name__)

@app.route('/nlp', methods=['POST'])
def nlp_processing():
    
    data = request.get_json()
    
    if data is None:
        return jsonify({"error": "No JSON data provided"}), 400

    if 'text' not in data:
        return jsonify({"error": "The 'text' key is missing in the JSON data"}), 400

    text = data['text']

    words = text.split()

    danger_score = 0

    for word in words:
        profanity = predict([word])
        if any(profanity):
            danger_score += 10  
            
    if danger_score > 100:
        danger_score = 100

    # Determine if the language is offensive based on the danger score
    langage_offensant = danger_score > 20  # If more than 20% danger

    # Convert langage_offensant to a standard Python boolean
    langage_offensant = bool(langage_offensant)

    # Return the results in JSON format
    results = {
        'langage_offensant': langage_offensant,
        'pourcentage_dangerosite': danger_score
    }
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
