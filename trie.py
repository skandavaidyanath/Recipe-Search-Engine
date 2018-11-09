import pickle
from functools import reduce


class TrieNode(object):
    """
    Implementation of a trie data-structure
    """

    def __init__(self, char):
        self.char = char
        self.children = []
        # Is it the last character of the word.
        self.word_finished = False
        # How many times this character appeared in the addition process
        self.counter = 1

    def add(self, word):
        '''
        Adding a word in the trie structure
        '''
        node = self
        for char in word:
            found_in_child = False
            # Search for the character in the children of the present `node`
            for child in node.children:
                if child.char == char:
                        # We found it, increase the counter by 1 to keep track that another
                    # word has it as well
                    child.counter += 1
                    # And point the node to the child that contains this char
                    node = child
                    found_in_child = True
                    break
            # We did not find it so add a new chlid
            if not found_in_child:
                new_node = TrieNode(char)
                node.children.append(new_node)
                # And then point node to the new child
                node = new_node
        # Everything finished. Mark it as the end of a word.
        node.word_finished = True

    def find_prefix(self, prefix):
        '''
        Check and return 
          1. If the prefix exists in any of the words we added so far
          2. If yes then how may words actually have the prefix
        '''
        node = self
        # If the root node has no children, then return False.
        # Because it means we are trying to search in an empty trie
        if not self.children:
            return False, 0
        for char in prefix:
            char_not_found = True
            # Search through all the children of the present `node`
            for child in node.children:
                if child.char == char:
                    # We found the char existing in the child.
                    char_not_found = False
                    # Assign node as the child containing the char and break
                    node = child
                    break
            # Return False anyway when we did not find a char.
            if char_not_found:
                return False, 0
        # Well, we are here means we have found the prefix. Return true to indicate that
        # And also the counter of the last node. This indicates how many words have this
        # prefix
        return True, node.counter

    def all_suffixes(self, prefix):
        '''
        Finds all the suffixes possible of a given input string from any given node
        '''
        results = set()
        if self.word_finished:
            results.add(prefix)
        if not self.children:
            return results
        return results | reduce(lambda a, b: a | b,  [node.all_suffixes(prefix + node.char) for node in self.children])

    def autocomplete(self, prefix):
        '''
        Finds all the possible autocomplete options of a given string, by making use of the all_suffixes function.
        First we traverse the trie for the letters in the prefix we have then call all_suffixes
        We refine the list to make sure that the returned results have only letters of the alphabet
        '''
        node = self
        for char in prefix:
            if char not in [child.char for child in node.children]:
                return None
            for child in node.children:
                if child.char == char:
                    node = child
        auto_list = list(node.all_suffixes(prefix))
        refined_auto_list = list()
        for word in auto_list:
            flag = 0
            for char in word:
                if not (('a' <= char <= 'z') or ('A' <= char <= 'Z') or (char == ' ')):
                    flag = 1
            if flag == 0:
                refined_auto_list.append(word)
        return refined_auto_list


def main():
    '''
    Building the trie on our vocabulary and storing it.
    '''
    print('Building Trie Object...', end=' ')
    import json
    fileNames = ['ingredients', 'directions', 'dish_names', 'recipe_links']

    trie = TrieNode('*')
    for fileName in fileNames[:-1]:
        with open("vocabulary/{}_autocomplete.json".format(fileName), 'r') as fp:
            vocab_list = json.load(fp)
        for word in vocab_list:
            trie.add(word)
    with open("my_trie.pickle", "wb") as fp:
        pickle.dump(trie, fp)
    print('Done.')


if __name__ == '__main__':
    main()
