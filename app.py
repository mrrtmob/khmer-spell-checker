from flask import Flask, redirect, url_for, request
app = Flask(__name__)
from khmernltk import word_tokenize
from spell_checker import SpellChecker
spell_checker = SpellChecker()
def correct(str):
    words = word_tokenize(str, return_tokens=True)
    suggestWords = []
    for i in range(len(words)):
        if words[i] == ' ':
            suggestWords.append(' ')
        else:
            suggest = spell_checker.suggest(words[i])
            suggestWords.append(suggest)

    correctWord = ""
    for i in range(len(suggestWords)):
        if type(suggestWords[i]) is list:
            correctWord += suggestWords[i][0]
        else:
            correctWord += suggestWords[i]

    return correctWord

@app.route('/success/<name>')

def success(name):
   return 'original: %s' % name + '<br>suggest: %s' % correct(name)

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

if __name__ == '__main__':
   app.run(debug = True)