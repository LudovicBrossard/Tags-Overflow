# -*- coding: utf-8 -*-
"""
Stack Overflow Tag predictor
"""

import pickle
import re
from bs4 import BeautifulSoup
from nltk.tokenize import ToktokTokenizer
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer


MAP_TABLE = {"\n": " ", "\'\xa0": " ", "\s+": " "}
PUNCTUATION = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~’'
STOP_WORDS = list(stopwords.words("english")) 
# adding specific words into the list
STOP_WORDS += ['im', 'okay', 'ok', 'help', 'please', 'thank', 'thanks', 'happy', 'cant']

token=ToktokTokenizer() 
lemma = WordNetLemmatizer()

### load  multilabel binarizer, vectorizer and classifier
mlb = pickle.load(open('multilabel_binarizer.pkl','rb'))
vectorizer = pickle.load(open('tfidf_vectorizer.pkl','rb'))
classifier = pickle.load(open('classifier.pkl','rb'))

tags = mlb.classes_

### construct the regular expression that is used in the preprocessing steps
def construct_regexp():
    added_tags = [r'c\+\+',r'c\#',r'\sc\s',r'\.net',r'oop',r'ssl',r'r',r'x86',
                   r'g\+\+',r'f\#',r'd3',r'ssis',r'ggplot',r'3d',r'ssh']
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    regexp = r""
    start = r"\b"
    end = r"{0,12}\b"
    for i,letter in enumerate(alphabet):
        if i==0: #remove pattern of the form abc...
            regexp += start+letter+"["+alphabet.replace(letter,"")+"][abd-z][a-z]{0,11}\\b"
        else: #remove pattern with first letter repeated
            regexp += start+letter+"["+alphabet.replace(letter,"")+"][a-z]"+end
        if i!=len(alphabet)-1:
            regexp+="|"
    for tag in added_tags: #added specific tags that are not considered otherwise
        regexp += "|"+tag
    return regexp

REGEXP = construct_regexp()

### Definition of function to preprocess question
def remove_code(text):
    text = re.sub('<code>[\s\S]+?</code>', ' ', text)
    return text

def remove_html(text):
    text = BeautifulSoup(text, "html.parser").get_text()
    return text

def clean_text(text, mapping=MAP_TABLE):
    text = text.lower()
    for pattern, trad in mapping.items():
        text = re.sub(pattern,trad,text)
    return text

def remove_punct(text, symbols=PUNCTUATION, protected=tags):
    words = token.tokenize(text)
    without_punct = []
    for word in words:
        if word in protected:
            without_punct.append(word)
        else:
            without_punct.append(re.sub('['+symbols+']',' ',word))
    new_text = ' '.join(without_punct)
    new_text = new_text.replace("\\","")
    new_text = re.sub('\s+',' ',new_text)
    return new_text.strip()

def remove_stop_words(text, stopwords=STOP_WORDS):
    words = token.tokenize(text)
    without_stops = [word for word in words if word not in stopwords]
    return ' '.join(without_stops)

def regex_and_lemmatize(text, regex=REGEXP, protected=tags):
    protected_add = list(protected)+['js','tls']
    lemmatized = []
    #findall returns a list of tokens that serves as input of lemmatize function
    words = re.findall(regex,text)
    for word in words:
        if word in protected_add:
            lemmatized.append(word)
        else:
            x = lemma.lemmatize(word)
            lemmatized.append(x)
    new_text = ' '.join(lemmatized)
    new_text = re.sub('\s+',' ',new_text)
    return new_text

def process_question(question):
    processed_q = remove_code(question)
    processed_q = remove_html(processed_q)
    processed_q = clean_text(processed_q)
    processed_q = remove_punct(processed_q)
    processed_q = remove_stop_words(processed_q)
    processed_q = regex_and_lemmatize(processed_q)
    
    return processed_q