from flask import Flask, request, jsonify, render_template
from profanity_check import predict
import spacy

app = Flask(__name__)
nlp_fr = spacy.load("fr_core_news_sm")

@app.route('/')
def index():
    return render_template('index.html')

def identifier_nature_dangerosite(texte):
    mots_menaces = ['menace', 'nuisible', 'dangereux', 'tuer', 'crève']
    nature_dangerosite = []

    for mot in mots_menaces:
        if nlp_fr.vocab[mot].is_stop:
            profanity_score = predict([mot])[0] * 100

            if profanity_score > 100:
                profanity_score = 100

            nature_dangerosite.append({
                'type_menace': mot,
                'pourcentage': profanity_score
            })

    return nature_dangerosite

def analyse_semantique(texte):
    doc = nlp_fr(texte)
    
    entites_nommees = [ent.text for ent in doc.ents]
    verbes = [token.text for token in doc if token.pos_ == "VERB"]
    adjectif = [token.text for token in doc if token.pos_ == "ADJ"]
    
    return entites_nommees, verbes, adjectif

@app.route('/', methods=['POST'])
def nlp_processing():
    data = request.get_json()
    
    if data is None:
        return jsonify({"error": "No JSON data provided"}), 400

    if 'text' not in data:
        return jsonify({"error": "The 'text' key is missing in the JSON data"}), 400

    text = data['text']

    doc_fr = nlp_fr(text)

    insults_count_fr = sum([token.is_stop for token in doc_fr])

    danger_score_fr = (insults_count_fr / len(doc_fr)) * 100

    if danger_score_fr > 100:
        danger_score_fr = 100

    danger_score_en = predict([text])[0] * 100

    if danger_score_en > 100:
        danger_score_en = 100

    danger_score_global = (danger_score_fr + danger_score_en) / 2

    langage_offensant = danger_score_global > 10

    nature_dangerosite = identifier_nature_dangerosite(text)

    entites_nommees, verbes, adjectif = analyse_semantique(text)

    results = {
        'langage_offensant': bool(langage_offensant),
        'pourcentage_dangerosite_fr': float(danger_score_fr),
        'pourcentage_dangerosite_en': float(danger_score_en),
        'pourcentage_dangerosite_global': float(danger_score_global),
        # 'nature_dangerosite': nature_dangerosite,
        'entites_nommees': entites_nommees,
        'verbes': verbes,
        'adjectif': adjectif
    }
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)