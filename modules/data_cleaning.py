# modules/data_cleaning.py

import fitz  # PyMuPDF
import spacy
import pandas as pd
import re
from gender_guesser.detector import Detector

# Load spaCy English model and gender detector once
nlp = spacy.load("en_core_web_sm")
gender_detector = Detector()

def extract_script_text(pdf_file):
    """
    Extracts text from a PDF file uploaded via Streamlit.
    Accepts: pdf_file (UploadedFile object)
    Returns: Full extracted text from the PDF
    """
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        return "\n".join([page.get_text() for page in doc])

def extract_intro_lines(text):
    """
    Filters out long/short lines and removes all-uppercase or cue-style lines.
    """
    lines = text.split('\n')
    clean_lines = []

    for line in lines:
        line = line.strip()
        if 5 < len(line.split()) < 30:
            if not line.isupper() and not re.match(r'^[A-Z]+:$', line):
                clean_lines.append(line)
    return clean_lines

def detect_character_and_gender(line):
    """
    Uses spaCy NER to detect character names and gender-guesser for gender.
    """
    doc = nlp(line)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            gender = gender_detector.get_gender(name.split()[0])
            return name, gender
    return None, None

def process_pdf(pdf_file):
    """
    Main entry point for data cleaning.
    Accepts: pdf_file (UploadedFile object)
    Returns: Cleaned DataFrame with character, gender, and line
    """
    text = extract_script_text(pdf_file)
    lines = extract_intro_lines(text)

    clean_data = []
    for line in lines:
        character, gender = detect_character_and_gender(line)
        if character and gender in ['male', 'female']:
            clean_data.append({
                "character": character,
                "gender": gender,
                "line": line.strip()
            })

    return pd.DataFrame(clean_data)