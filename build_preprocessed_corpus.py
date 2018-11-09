import json
from preprocessing import preprocess

fileNames = ['ingredients', 'directions', 'dish_names', 'recipe_links']


def main():
    '''
    Builds the preprocessed corpus for 3 corpuses.
    '''
    print('Building Preprocessed Corpus...', end=' ')
    for fileName in fileNames[:-1]:
        i = 1
        corpus_list = list()
        corpus_dictionary = dict()
        with open("corpus/{}.json".format(fileName), 'r') as fp:
            corpus_list = json.load(fp)
        for document in corpus_list:
            corpus_dictionary[i] = preprocess(document)
            i = i + 1
        with open("preprocessed-corpus/{}.json".format(fileName), 'w') as fp:
            json.dump(corpus_dictionary, fp)
    print('Done.')


if __name__ == '__main__':
    main()
