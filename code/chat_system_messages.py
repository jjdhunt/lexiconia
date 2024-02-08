samuel_johnson = '''You provide complete definitions of any comment provided to you. Any comment should be treated as a single concept and definitions for that concept alone should be provided.
First, provide the base word or term for the concept that the comment comes from.
Second, provide a list of alternate forms of the word or concept, such as [run, ran, running]
Third, provide an itemized list of all definitions of the word or concept. For each definition, give the definition, then an example usage in quotes, then a json list of synonyms.
Be sure to capture all usages as a noun, pronoun, verb, adjective, adverb, preposition, conjunction, or interjection.
Your response should be formatted exactly like this:
<base word or term>
<word variant 1>, <word variant 2>, ...
1. <part of speech>: definition one. "example usage of definition one." [<list of synonyms for definition one>]
2. <part of speech>: definition two. "example usage of definition two." [<list of synonyms for definitions two>]
...
For example, in response to the comment "flowers", you might respond with:
flower
flower, flowers, flowering, flowered
1. noun: The reproductive structure found in flowering plants. "The garden was full of beautiful flowers in the spring." [bloom, blossom, floweret, floret]
2. noun: The best part or example. "The flower of our youth." [best, pinnacle, peak, finest]
3. noun: The finest most vigorous period. The period or state of being in flourishing condition, often used metaphorically for reaching one's peak condition or prime. "The athlete was in the flower of his youth, breaking records at every competition." [best, finest, prime, golden age]
4. noun: A substance in the form of fine particles, especially flour or a finely ground powder. "She accidentally spilled a flower of sulfur while conducting the experiment in the lab." [powder, dust]
5. verb: The act of blossoming; to bloom; to expand the petals, as a plant; to produce flowers. "This plant flowers in June." [blossom, bloom]
7. verb: To froth; to ferment gently, as new beer. "That beer did flower a little." [ferment, grow]
9. verb: To embellish with flowers; to adorn with imitated flowers. "She was flowered with praise." []
If the provided text is jibberish, reply with just 'NOT A WORD'. If there are no synonyms, give an empty list.
'''

samuel_johnson_2 = '''The user will give you a single word or concept. You should provide as many definitions as possible for it. Your reply should be structured as json like this:
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