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

while True:
    print('Enter text:')
    x = input()
    print('Correct text:')
    print(correct(x))