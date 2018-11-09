import json

fileNames = ['ingredients', 'directions', 'dish_names', 'recipe_links']


def main():
    '''
    Builds the inverted indexes for 3 corpuses.
    '''
    print('Building Inverted Index...', end=' ')
    for fileName in fileNames[:-1]:
        corpus = dict()
        vocab = list()
        inverted_index = dict()
        with open("preprocessed-corpus/{}.json".format(fileName), 'r') as fp:
            corpus = json.load(fp)
        with open("vocabulary/{}.json".format(fileName), 'r') as fp:
            vocab = json.load(fp)
        for word in vocab:
            list_of_docs = []
            for docId in corpus.keys():
                if word in corpus[docId]:
                    list_of_docs.append(docId)
            inverted_index[word] = list_of_docs
        with open("inverted-index/{}.json".format(fileName), 'w') as fp:
            json.dump(inverted_index, fp)
    print('Done.')


if __name__ == '__main__':
    main()
