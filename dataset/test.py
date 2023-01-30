import spacy

nlp = spacy.load("en_core_web_sm")

parsed_text = nlp("My phone number is 505-234-5500")