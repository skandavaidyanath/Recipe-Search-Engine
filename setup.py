import build_corpus_dict
import build_inverted_index
import build_norm_scores
import build_preprocessed_corpus
import build_tfidf_vectors
import build_vocabulary
import trie
import spellcheck
import update_database


def main():
    '''
    runs all the setup scripts.
    '''
    build_corpus_dict.main()
    build_preprocessed_corpus.main()
    build_vocabulary.main()
    build_inverted_index.main()
    build_tfidf_vectors.main()
    build_norm_scores.main()
    trie.main()
    spellcheck.main()
    update_database.setup_db()


if __name__ == '__main__':
    main()
