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
word = input("Enter a word: ")
query = cursor.execute("SELECT Definition FROM Dictionary WHERE Expression = '%s'" % word)

results = cursor.fetchall()

def define(definedWord):
    try:
        pass
    except IndexError as e:
        return "Error" 

    if definedWord:
        for result in definedWord:
            return definedWord[0]
    else:
        query = cursor.execute("SELECT Expression FROM Dictionary")
        definedWord = cursor.fetchall()
        words = [word[0] for word in definedWord]
        match =  get_close_matches(word, words)
        if len(match) > 0:
            ##the match[0] means that only one word will be returned, if you want multiple get rid of [0]
            response = input(f"Did you mean {match[0]}? Press Y if you did, press N if you didn't. ").upper()
            if response == 'Y':
                query = cursor.execute("SELECT Definition FROM Dictionary WHERE Expression = '%s'" % match[0])
                definedWord = cursor.fetchall()
                return definedWord[0]
            elif response == 'N':
                return "We do not understand what word you're looking for."
            else:
                return "We do not understand what word you're looking for."
        else:
            return "Error"

print(define(results))
