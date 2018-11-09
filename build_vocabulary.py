import json
from preprocessing import preprocess

fileNames = ['ingredients', 'directions', 'dish_names', 'recipe_links']


def main():
    '''
    Builds the stemmed and unstemmed vocabularies for 3 corpuses.
    '''
    print('Building Vocabulary...', end=' ')
    for fileName in fileNames[:-1]:  # we don't need recipe_links
        vocab, autocompleteVocab = set(), set() # one stemmed, one unstemmed
        with open("corpus/{}.json".format(fileName), 'r') as f:
            stringList = json.load(f)
            docList, autocompleteDocList = [], []
            for i in range(len(stringList)):
                docList.append(preprocess(stringList[i]))
                autocompleteDocList.append(
                    preprocess(stringList[i], stem=False))
                for word in docList[i]:
                    vocab.add(word)
                for word in autocompleteDocList[i]:
                    autocompleteVocab.add(word)
            with open('vocabulary/{}.json'.format(fileName), 'w') as vocabFile:
                json.dump(list(vocab), vocabFile)  # set isn't serializable
            with open('vocabulary/{}_autocomplete.json'.format(fileName), 'w') as vocabFile:
                json.dump(list(autocompleteVocab), vocabFile) # set isn't serializable
    print('Done.')


if __name__ == '__main__':
    main()
