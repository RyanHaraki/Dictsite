from flask import Flask, render_template, url_for, request, redirect, flash
from flask_wtf import FlaskForm, Form
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired, Length
import mysql.connector
from difflib import get_close_matches

conn = mysql.connector.connect(
    user="ardit700_student",
    password="ardit700_student",
    host="108.167.140.122",
    database="ardit700_pm1database",
    connection_timeout=300
)

cursor = conn.cursor()

## to include other script consider just consider moving the code here and turning it into functions.
##BEGINNING OF WEBSITE CODE
app = Flask(__name__)
app.config['SECRET_KEY'] = 'b16d28e9b3c719e85f57d081b9f974fb'


class wordInput(Form):
    word = StringField('Word', [DataRequired()])

@app.route("/home/", methods=['POST', 'GET'])
def home():

    if request.method == 'POST':
        word = request.form.get('word')
        query = cursor.execute("SELECT Definition FROM Dictionary WHERE Expression = '%s'" % word)
        results = cursor.fetchall()

        def definedAgain(wordDefined):
            if wordDefined:
                for result in wordDefined:
                    return wordDefined[0]
            else:
                query = cursor.execute("SELECT Expression FROM Dictionary")
                wordDefined = cursor.fetchall()
                words = [word[0] for word in wordDefined]
                match =  get_close_matches(word, words)
                query = cursor.execute("SELECT Definition FROM Dictionary WHERE Expression = '%s'" % match[0])
                wordDefined = cursor.fetchall()
                return ' '.join(word[0] for word in wordDefined)


        def define(definedWord):
            try:
                if definedWord:
                    for result in definedWord:
                        return ''.join(definedWord[0])
                elif definedWord == '':
                    return "Error, please input a word."
                else:
                    query = cursor.execute("SELECT Expression FROM Dictionary")
                    definedWord = cursor.fetchall()
                    words = [word[0] for word in definedWord]
                    match =  get_close_matches(word, words)
                    return f"Did you mean {match[0]}? If so, the definition(s) is/are: {definedAgain(results)}"
            except IndexError:
                return "Error, please enter a word."

        return render_template('home.html', word=request.form.get('word'), wordDefinition=define(results))
    form = wordInput()
    return render_template('home.html', language=request.args.get('language'))


@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')

@app.route('/tutorial/')
def tutorial():
    return render_template('tutorial.html')

if __name__ == '__main__':
    app.run(debug=True)