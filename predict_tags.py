# -*- coding: utf-8 -*-
"""
Stack Overflow Tag predictor
"""

from preprocess import process_question, mlb, vectorizer, classifier


### Definition of functions to predict tags from preprocessed question
def transform(processed_q):
    tfidf_mat = vectorizer.transform([processed_q])
    return tfidf_mat

def predict(tfidf_mat):
    bin_labels = classifier.predict(tfidf_mat)
    return bin_labels

def translate(bin_labels):
    if bin_labels.sum() != 0:
        tags = mlb.inverse_transform(bin_labels)
        return tags[0]
    else:
        return "No relevant tags found for this question..."

def run_predictor(question):
    processed_q = process_question(question)
    tfidf_mat = transform(processed_q)
    bin_labels = predict(tfidf_mat)
    tags = translate(bin_labels)
    
    return tags