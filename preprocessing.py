from gensim.parsing.preprocessing import preprocess_string, DEFAULT_FILTERS
from gensim.utils import deaccent


def preprocess(s, stem = True):
    '''
    given a document or query string, returns a list of preprocessed words.
    we can decide whether to stem each word or not.
    '''
    if not stem:
        preprocess_filters = DEFAULT_FILTERS.copy()
        preprocess_filters.pop()  # remove stemming from list of filters
        wordList = preprocess_string(s, filters=preprocess_filters)
    else:
        wordList = preprocess_string(s)
    for i in range(len(wordList)):
        wordList[i] = deaccent(wordList[i])
    return wordList
