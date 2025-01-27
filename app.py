import spacy
import os

# Ensure spacy model is downloaded
if not spacy.util.is_package("en_core_web_sm"):
    os.system("python -m spacy download en_core_web_sm")
from flask import Flask, render_template, request, jsonify
import wikipediaapi
import spacy
import random
import re  # Added to clean up punctuation issues

# Load spaCy model for NLP
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

def clean_text(text):
    """Clean text by removing unnecessary quotation marks and fixing grammar."""
    # Remove stray quotes and surrounding spaces
    text = re.sub(r'["\']', '', text.strip())
    return text

def generate_flashcards(topic):
    # Initialize Wikipedia API
    wiki_wiki = wikipediaapi.Wikipedia(language='en')
    page = wiki_wiki.page(topic)

    if not page.exists():
        return [{"question": "Page Error", "answer": f"No Wikipedia page found for '{topic}'."}]

    # Get the summary text
    text = page.summary
    
    # Split the summary into sentences
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents if len(sent.text.split()) > 8]

    flashcards = []
    for sentence in sentences:
        # Process each sentence to extract meaningful flashcard content
        sentence_doc = nlp(sentence)

        # Extract the most significant noun chunk or key phrase
        key_phrases = [chunk.text for chunk in sentence_doc.noun_chunks if len(chunk.text.split()) > 1]
        if not key_phrases:
            continue

        main_phrase = random.choice(key_phrases)
        
        # Fix capitalization for key phrases
        main_phrase = main_phrase[0].lower() + main_phrase[1:] if main_phrase[0].isupper() else main_phrase
        main_phrase = clean_text(main_phrase)  # Clean the text to remove quotes or stray punctuation
        
        # Formulate the question templates dynamically
        question_templates = [
            f"What is the significance of {main_phrase}?",
            f"How does {main_phrase} relate to the topic of {topic}?",
            f"Explain the importance of {main_phrase}.",
            f"Describe the role of {main_phrase}."
        ]

        question = clean_text(random.choice(question_templates))  # Clean the final question
        flashcards.append({"question": question, "answer": sentence})

    return flashcards

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        topic = data.get('topic')
        flashcards = generate_flashcards(topic)
        return jsonify({"flashcards": flashcards})
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
