import re
import json
from collections import defaultdict
import pickle


class SpellChecker(object):
    '''
    A class that has methods to correct spellings of words based on a probability and edit-distance based algorithm.
    '''
    def __init__(self, vocabulary):
        self.vocabulary = vocabulary

    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    def _edits1(self, word):
        '''
        Edits are of the form of adding a new letter, deleting an existing letter, replacing a letter by another letter,
        or swapping two adjacent letters.
        '''
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [a + b[1:] for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
        replaces = [a + c + b[1:]
                    for a, b in splits for c in self.alphabet if b]
        inserts = [a + c + b for a, b in splits for c in self.alphabet]
        return set(deletes + transposes + replaces + inserts)

    def _known_edits2(self, word):
        '''
        We make a second edit to all the words we edited once.
        We only consider the new words formed by correction, that are in our vocabulary. All other meaningless words are discarded.
        '''
        return set(e2 for e1 in self._edits1(word) for e2 in self._edits1(e1) if e2 in self.vocabulary)

    def _known(self, words):
        '''
        Filters all the words and returns only the words in our vocabulary
        '''
        return set(w for w in words if w in self.vocabulary)

    def correct_token(self, token):
        '''
        Checks all the candidates and returns only the one with maximum probability of occurence
        '''
        candidates = self._known([token]) or self._known(
            self._edits1(token)) or self._known_edits2(token) or [token]
        return max(candidates, key=self.vocabulary.get)

    def correct_phrase(self, text):
        '''
        To correct a string of words and not just one word
        '''
        tokens = text.split()
        return [self.correct_token(token) for token in tokens]


def words(text):
    '''
    Regular expression identifies words in a line of text.
    '''
    return re.findall('[a-z]+', text.lower())


def train(model, features):
    '''
    Finds and stores the frequency of each word in the vocabulary.
    '''
    for f in features:
        model[f] += 1


def main():
    '''
    Opens up all the vocabulary files, creates the spellchecker object and then stores it.
    '''
    print('Building Spellcheck Object...', end=' ')
    spell_vocabulary = defaultdict(int)
    with open("corpus/directions.json", "r") as fp:
        unstemmed_corpus = json.load(fp)
        for item in unstemmed_corpus:
            train(spell_vocabulary, words(item))
    with open("corpus/dish_names.json", "r") as fp:
        unstemmed_corpus = json.load(fp)
        for item in unstemmed_corpus:
            train(spell_vocabulary, words(item))
    with open("corpus/ingredients.json", "r") as fp:
        unstemmed_corpus = json.load(fp)
        for item in unstemmed_corpus:
            train(spell_vocabulary, words(item))
    spellchecker = SpellChecker(spell_vocabulary)
    with open("my_spellchecker.pickle", "wb") as fp:
        pickle.dump(spellchecker, fp)
    print('Done.')


if __name__ == '__main__':
    main()
