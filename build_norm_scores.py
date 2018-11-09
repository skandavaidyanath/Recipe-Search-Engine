import json
from collections import defaultdict

fileNames = ['ingredients', 'directions', 'dish_names', 'recipe_links']


def main():
    '''
    Computes length normalization scores for 3 corpuses.
    '''
    print('Building Length Normalization scores...', end=' ')
    for fileName in fileNames[:-1]:
        tfidf_vectors = dict()
        with open("tfidf-vectors/{}.json".format(fileName), 'r') as fp:
            tfidf_vectors = json.load(fp)
        norm = defaultdict(int)
        for docId in tfidf_vectors:
            for term in tfidf_vectors[docId]:
                norm[docId] += tfidf_vectors[docId][term] ** 2
            norm[docId] **= 0.5
        with open("document_norms/{}.json".format(fileName), 'w') as fp:
            json.dump(norm, fp)
    print('Done.')


if __name__ == '__main__':
    main()
