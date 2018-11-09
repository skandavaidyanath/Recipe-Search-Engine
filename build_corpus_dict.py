import json

fileNames = ['ingredients', 'directions', 'dish_names', 'recipe_links']


def main():
    '''
    Builds a dictionary representation of each of the 3 corpuses.
    '''
    print('Building Corpus Dict...', end=' ')
    for fileName in fileNames:
        i = 1
        corpus_list = list()
        corpus_dictionary = dict()
        with open("corpus/{}.json".format(fileName), 'r') as fp:
            corpus_list = json.load(fp)
        for document in corpus_list:
            corpus_dictionary[i] = document
            i = i + 1
        with open("corpus/{}_dict.json".format(fileName), 'w') as fp:
            json.dump(corpus_dictionary, fp)
    print('Done.')


if __name__ == '__main__':
    main()
