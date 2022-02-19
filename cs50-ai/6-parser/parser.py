import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj VP | S Conj S
S -> NP PP | S P S
AP -> Adj N | Adj AP
NP -> N | Det N | Det AP
PP -> P | P NP
VP -> V | Adv VP | N V | V PP | V NP | V NP PP
VP -> VP Adv
"""


grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Tokenzie the sentence.
    words = nltk.tokenize.wordpunct_tokenize(sentence)

    # Convert all characters to lowercase removing words that
    # do not contain at least one alphabetic character.
    words = [word.lower() for word in words if word.isalpha()]

    # Return pre-processed sentence.
    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # Create a list to store the noun phrase chunks.
    noun_prhase_chunks = []

    # Iterate over the subtrees of 'tree'.
    for subtree in tree.subtrees():
        # For each 'subtree' iterate over its subtrees 's' adding the label
        # for each 's' to the list 'labels'.
        labels = []
        for s in subtree:
            # Use a try loop to try to add all the labels of each 's' to avoid
            # erros. Because at some point 's' might be a string, which doesn't
            # have a label method.
            try:
                labels.append(s.label())
            except:
                continue

        # A 'subtree' that is a noun phrase will not have subtrees 's' with
        # the label "NP".
        if subtree.label() == "NP" and "NP" not in [labels]:
            noun_prhase_chunks.append(subtree)

    return noun_prhase_chunks


if __name__ == "__main__":
    main()
