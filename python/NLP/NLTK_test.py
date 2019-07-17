# Natural Language Toolkit 3.3
import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

sentence = """At eight o'clock on Thursday morning Arthur didn't feel very good."""
sentence = """Is the water in False Creek  safe for paddlers taking part in the Alcan Dragon Boat Festival?"""
# sentence = """What will the water temperature be at the beach for the AI summer BBQ?"""
sentence = """What was the water temperature at False Creek at June 2018?"""

print(sentence)

tokens = nltk.word_tokenize(sentence)

print(tokens)

tagged = nltk.pos_tag(tokens)

print(tagged)

entities = nltk.chunk.ne_chunk(tagged)

print(entities)






