import math
import nltk
import os
import string
import sys

from operator import itemgetter


FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {filename: tokenize(files[filename]) for filename in files}
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    # Create dictionary to map all the filenames with its content.
    files = dict()
    for filename in os.listdir(directory):
        # Open and load each file found in 'directory'.
        with open(os.path.join(directory, filename)) as f:
            files[filename] = f.read()

    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # Process document.
    words_in_document = [
        word.lower()
        for word in nltk.word_tokenize(document)
        if word not in string.punctuation
        and word not in nltk.corpus.stopwords.words("english")
    ]

    return words_in_document


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # Create a set of all the words that exist in the corpus.
    words_in_documents = set([word for words in documents.values() for word in words])

    # Create a dictionary to map each word to its IDF value.
    idfs = dict()
    for word in words_in_documents:
        # Determine the number of documents in the corpus that contain 'word'.
        matched_documents = [
            document for document in documents if word in documents[document]
        ]

        # Determine the IDF value for each word.
        idfs[word] = math.log(len(documents) / len(matched_documents))

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    # Process query.
    query = set(
        [
            word.lower()
            for word in query
            if word not in string.punctuation
            and word not in nltk.corpus.stopwords.words("english")
        ]
    )

    # Create a list tuples (filename, sum_tfidfs) to sort the filenames.
    filenames = []
    for file in files:
        # Determine the total sum of TF-IDF values for each file.
        sum_tfidfs = 0
        for word in query:
            tf = files[file].count(word)
            idf = idfs[word]
            sum_tfidfs += tf * idf

        filenames.append((file, sum_tfidfs))

    # Sort filenames by their total sum of TF-IDF values.
    ranked_filenames = [
        filename
        for filename, sum_tfidfs in sorted(filenames, key=itemgetter(1), reverse=True)
    ]

    # Return the 'n' top filenames.
    return ranked_filenames[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # Process query.
    query = set(
        [
            word.lower()
            for word in query
            if word not in string.punctuation
            and word not in nltk.corpus.stopwords.words("english")
        ]
    )

    # Create a list tuples (sentence, sum_idfs, qt_density) to sort the sentences.
    results = []
    for sentence, words in sentences.items():
        # Determine the total sum of IDF values and query term density for each
        # sentence.
        sum_idfs = 0
        for word in query:
            if word in words:
                sum_idfs += idfs[word]
        qt_density = sum(words.count(word) for word in query) / len(words)

        results.append((sentence, sum_idfs, qt_density))

    # Sort sentences by their total sum of IDF values and query term density.
    ranked_sentences = [
        sentence
        for sentence, sum_idfs, qt_density in sorted(
            results, key=itemgetter(1, 2), reverse=True
        )
    ]

    # Return the 'n' top sentences.
    return ranked_sentences[:n]


if __name__ == "__main__":
    main()
