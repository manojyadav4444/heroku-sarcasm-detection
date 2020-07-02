from flask import Flask, request, render_template, redirect, url_for
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pickle
from keras.models import load_model
import re
from keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)

@app.route('/success/<name>')
def success(name):
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer_obj = pickle.load(handle)
    model = load_model('model-021.model')
    tokens = word_tokenize(name)
    stop_words = set(stopwords.words("english"))
    words = [w for w in tokens if not w in stop_words]
    sequences = tokenizer_obj.texts_to_sequences(words)
    lines_pad = pad_sequences(sequences, maxlen=25, padding='post')
    pred = model.predict(lines_pad)
    pred*=100
    if pred[0][0]>=50: return "It's a sarcasm!" 
    else: return "It's not a sarcasm."

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success', name = user))

    return render_template('sarcasm.html')

if __name__ == "__main__":
    app.run(debug=True)