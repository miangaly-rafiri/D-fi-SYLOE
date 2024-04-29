from flask import Flask, request, jsonify
import spacy

app = Flask(__name__)

nlp = spacy.load("fr_core_news_sm")

def analyse_semantique(texte):
    doc = nlp(texte)
    
    # Exemple d'analyse sémantique :
    entites_nommees = [ent.text for ent in doc.ents]
    verbes = [token.text for token in doc if token.pos_ == "VERB"]
    adjectives = [token.text for token in doc if token.pos_ == "ADJ"]
    
    
    return entites_nommees, verbes, adjectives

# Exemple d'utilisation :
text = "Le chat noir est rapide et élégant. La journée est ensoleillée et agréable. Le gâteau au chocolat est délicieux. La tour Eiffel est un monument francais"
entites, verbes, adjectives = analyse_semantique(text)
print("Entités nommées :", entites)
print("Verbes :", verbes)
print("Adjectifs :", adjectives)

