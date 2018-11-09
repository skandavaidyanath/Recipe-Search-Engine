from spellcheck import SpellChecker
from trie import TrieNode
import pickle


def check_spellings(spellchecker, input_query):
    '''
    Function that uses our spell-chcker to correct spellings.
    '''
    return ' '.join(spellchecker.correct_phrase(input_query))


def bar(spellchecker, my_trie, input_query):
    '''
    Returns a list of autocomplete suggestions given an input query.
    Uses our trie and our spell-checker simultaneously.
    It tries to auto complete the entire input query and if it cannot, it spell corrects the input query
    and then tries to auto-complete it.
    '''
    list_of_suggestions = set()
    input_query_tokens = input_query.split(' ')
    if my_trie.autocomplete(input_query) is not None:
        for word in my_trie.autocomplete(input_query[:10]):
            if len(input_query.split(' ')) == 1:
                list_of_suggestions.add(word)
                continue
            list_of_suggestions.add(
                str(' '.join(input_query_tokens[:-1])) + ' ' + str(word))
        return list(list_of_suggestions)
    else:
        input_query = check_spellings(spellchecker, input_query)
        list_of_suggestions.add(input_query)
        input_query_tokens = input_query.split(' ')
        last_token = input_query_tokens[-1]
        if my_trie.autocomplete(last_token) is not None:
            for word in my_trie.autocomplete(last_token)[:10]:
                if len(input_query_tokens) == 1:
                    list_of_suggestions.add(word)
                    continue
                list_of_suggestions.add(
                    str(' '.join(input_query_tokens[:-1])) + ' ' + str(word))
            return list(list_of_suggestions)
        return []


def main():
    '''
    Sample function to test our auto-completer
    '''
    with open('my-trie.txt', 'rb') as fp:
        my_trie = pickle.load(fp)
    with open('my-spell-checker.txt', 'rb') as fp:
        spellchecker = pickle.load(fp)
    while True:
        input_query = input('Enter your query: ')
        if input_query == 'quit':
            break
        print(bar(spellchecker, my_trie, input_query))
        print('*********************')


if __name__ == '__main__':
    main()
