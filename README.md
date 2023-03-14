# A Simple Markov Chain Text Generator

I remember a project to create something like this from Dave Ackley's CS class
at UNM. Or maybe it was another class.

You specify a base number of characters to use for each Markov state.
Each such set of characters that appear in the input is an "ngram".
When training, the program considers each n+1 characters of text, and
associates with the ngram the number of times each other character actually
appears next in the input text.

That is, it learns what the text looks like by considering which characters
follow each ngram. It can then generate similar text by choosing the next
generated character based on what it saw in the input text. That is, the
input text is the training data.

For example, input text of "hello world" with 4-character ngrams would result
in a model with seven ngrams, and their associated next characters:
- "hell": 'o':1
- "ello": ' ':1
- "llo ": 'w':1
- "lo w": 'o':1
- "o wo": 'r':1
- " wor": 'l':1
- "worl": 'd':1

Note that there is no ngram "orld", because no character appears after that
set of four characters, as they are at the end of the input text.

Note also that this is not a very interesting example, as there are zero ngrams
that have more than one next character that appear in the input text.

A more interesting example of input text would be "hello world hell yeah" with
the following 4-character ngrams:
- "hell": 'o':1, ' ':1
- "ello": ' ':1
- "llo ": 'w':1
- "lo w": 'o':1
- "o wo": 'r':1
- " wor": 'l':1
- "worl": 'd':1
- "orld": ' ':1
- "rld ": 'h':1
- "ld h": 'e':1
- "d he": 'l':1
- " hel": 'l':1
- "ell ": 'y':1
- "ll y": 'e':1
- "l ye": 'a':1
- " yea": 'h':1

Note that the ngram "hell" has two next characters, 'o' and ' ' (space), as
each appears once in the input text.

When generating text based on this model, an input ngram of "hell" would have a
1-in-2 chance of generating 'o' as the next character, and a 1-in-2 chance of
generating ' ' as the next character.

As it trains on more text, the number of ngrams & next characters for each, and
the number of times each next character appears increases dramatically. More
input text is typically better.

Increasing the N value (the number of characters in each ngram) increases the
number of possible ngrams that could be encountered. The amount of memory
used by the model will scale with the input text, and generally with
the value of N. Larger N values give the model more context of the next
character, but increase the potential memory cost.

Run the program like this for more info on command line parameters:
```
python3 markov-chain-text.py -h
```

The program first parses the input file into the model. This make take a few seconds depending on your hardware and the size of the input file.

It then prompts for the number of characters to output.

It then selects an ngram from the model at random, and outputs it.
It then uses the model to generate the remaining number of characters
(specified number minus n).
It may stop early if it happens to encounter the final ngram in the input file.
This is unlikely to happen with a reasonably-sized input file.

It then prompts for another number of characters to output & repeats the
process.

I've had humorous success using [The Complete Works of William Shakespeare](https://www.gutenberg.org/ebooks/100) ([plaintext UTF-8](https://www.gutenberg.org/ebooks/100.txt.utf-8) version) from [Project Gutenberg](https://www.gutenberg.org), incluing this gem of an excerpt (with N=7):
```
DUKE.
Give me the
    kissing Titan, and a Spaniard.
```
