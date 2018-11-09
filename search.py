import json
from collections import defaultdict
from preprocessing import preprocess

fileNames = ['ingredients', 'directions', 'dish_names', 'recipe_links']


def cross_corpus_score(score):
    '''
    Returns the combined score from the 3 corpuses.
    '''
    return 0.4*score['dish_names'] + 0.3*score['directions'] + 0.3*score['ingredients']


def search(queryString):
    '''
    Returns a list of document IDs in descending order of scores for a query.
    '''
    queryList = preprocess(queryString)
    for fileName in fileNames[:-1]:
        with open("vocabulary/{}.json".format(fileName), 'r') as fp:
            vocab = json.load(fp)
        # set is faster for checking if an element is present
        vocab = set(vocab)

        tfidf_vectors = dict()
        with open("tfidf-vectors/{}.json".format(fileName), 'r') as fp:
            tfidf_vectors = json.load(fp)

        document_norms = dict()
        with open("document_norms/{}.json".format(fileName), 'r') as fp:
            document_norms = json.load(fp)

        # compute the query score for each document assuming query vector is boolean
        # each element is a document's scores for each fileName
        scores = defaultdict(lambda: defaultdict(lambda: 0))
        for docId in tfidf_vectors:
            if document_norms[docId] == 0:
                continue
            for word in queryList:
                if word in tfidf_vectors[docId]:
                    scores[docId][fileName] += tfidf_vectors[docId][word] / \
                        document_norms[docId]

    # we need to get a combined score from all fileNames
    sortedDocs = list(tfidf_vectors.keys())
    sortedDocs.sort(key=lambda x: cross_corpus_score(scores[x]), reverse=True)
    return sortedDocs


def get_docs(queryString, n=None):
    '''
    Returns a list of documents with their data given a query.
    '''
    docList = search(queryString)
    if not n:
        n = len(docList)
    result = [dict() for i in range(n)]
    for fileName in fileNames:
        corpus_dictionary = dict()
        with open("corpus/{}_dict.json".format(fileName), 'r') as fp:
            corpus_dictionary = json.load(fp)

        # build entity for each of top n documents
        for i in range(n):
            docId = docList[i]
            if 'docId' not in result[i]:
                result[i]['docId'] = docId
            result[i][fileName] = corpus_dictionary[docId]
    return result
