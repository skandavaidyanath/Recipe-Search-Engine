import json
from math import log


fileNames = ['ingredients', 'directions', 'dish_names', 'recipe_links']


def term_frequency(text, word):
    return log((1 + text.count(word)), 2)


def inverse_document_frequency(word, inverted_index, numDocs):
    return log((1 + (numDocs/len(inverted_index[word]))), 2)


def main():
    '''
    Builds the tfidf vectors for 3 corpuses.
    '''
    print('Building tfidf vectors...', end=' ')
    for fileName in fileNames[:-1]:
        with open("inverted-index/{}.json".format(fileName), 'r') as fp:
            inverted_index = json.load(fp)
        with open("preprocessed-corpus/{}.json".format(fileName), 'r') as fp:
            corpus = json.load(fp)
        tfidf_vectors = dict()
        numDocs = len(corpus)
        for docId in corpus.keys():
            tfidf_scores = dict()
            for word in inverted_index.keys():
                score = term_frequency(
                    corpus[docId], word) * inverse_document_frequency(word, inverted_index, numDocs)
                tfidf_scores[word] = score
            tfidf_vectors[docId] = tfidf_scores
        with open("tfidf-vectors/{}.json".format(fileName), 'w') as fp:
            json.dump(tfidf_vectors, fp)
    print('Done.')


if __name__ == '__main__':
    main()
