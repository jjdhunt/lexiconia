samuel_johnson = '''The user will give you a single word or concept. You should provide as many definitions as possible for it. Your reply should be structured as json like this:
{
    "term": <the word or concept provided>,
    "root_word": <the root word the term comes from>,
    "variants": [<list of alternate forms of the term>],
    "definitions": [
        {
        "part_of_speech": <noun, verb, etc.>,
        "definition": <the definition>,
        "example": <an example usage>,
        "synonyms": [<list of synonyms>]
        },
        {<next definition>}
    ]
}

If the provided word or concept is jibberish, return '{}'.
Be sure to capture all possible definitions and interpretations - as a noun, pronoun, verb, adjective, adverb, preposition, conjunction, or interjection. Capture technical meanings as well as vernacular.
The root word can be the provided term itself.
'''

identify_topic = '''Given a set of words, identify a broad theme or topic they share or represent. Some words may not fit. Respond only with the topic or theme; give no preamble.'''

generate_words_on_topic = '''Given a topic and a number, generate that number of words related to the topic. Print only words, separated by newlines. If no number is given, print twenty words.'''

words_valence = '''Given a list of words, rate their average meaning from 1 to 5 along three dimensions:
emotional valence (1 - most negative, 3 - neutral, 5 - most positive). For example, 'hate' would score a 1, 'math' would score a 3, and 'love' would score a 5. 
physicality (1 - completely imaginary, 3 - combination of ideas and physical, 5 - entirely physical). For example,'santa clause' would score a 1, 'democracy' would score a 3, and 'rock' would score a 5.  
humanity (1 - not related to people at all, 5 - entirely related to people). For example, 'rock' would score a 1, 'economics' would score a 3, and 'humans' would score a 5.
You should return just a json object like this:
{
"valence": <emotional valence score>,
"physicality": <physicality score>,
"humanity": <humanity score>
}
'''

land_name = '''Given a topic, come up with a creative name for a fantasy country, land, or region having to do with it.'''

sea_name = '''Given a topic, come up with a creative name for a sea in a fantasy world having to do with it. Use the forms, Sea of X or X Sea.'''