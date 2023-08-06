import os, marisa_trie
from pathlib import Path
from collections import Counter
from russian_uncensor.rd_wr_util import rd_wr_module

path_current_file = Path(__file__).parent


class WordStats:
    def __init__(self, dict_path=None, neg_words_fn=None, freq_letters_fn=None, bigrams_fn=None, trigrams_fn=None, debug=False):
        """ Init WordStats class.

        :param dict_path: common path to data files dir (str).
        :param neg_words_fn: obscene components file name (str).
        :param freq_letters_fn: frequent letters used in obscene words file name (str).
        :param bigrams_fn: frequent bi-grams used in obscene words file name (str).
        :param trigrams_fn: frequent tri-grams used in obscene words file name (str).
        :param debug: turn on instruments for debug (bool).
        :return:
        """
        # File paths:
        self.dict_path = Path.joinpath(path_current_file, Path('data')) if dict_path is None else dict_path
        print(self.dict_path)
        self.neg_words_filename = self.dict_path/'obscene_words.txt' if neg_words_fn is None else self.dict_path/neg_words_fn
        self.frequent_letters_filename = self.dict_path/'ngrams/freq_letters.txt' if freq_letters_fn is None else self.dict_path/freq_letters_fn
        self.bi_grams_filename = self.dict_path/'ngrams/bi_grams.txt' if bigrams_fn is None else self.dict_path/bigrams_fn
        self.tri_grams_filename = self.dict_path/'ngrams/tri_grams.txt' if trigrams_fn is None else self.dict_path/trigrams_fn
        # Crete dir (if it doesnt exist)
        if not os.path.exists(path=self.dict_path/'ngrams'):
            os.mkdir(path=self.dict_path/'ngrams')
        # Others:
        self.ru_alphabet = set('абвгдеёжзийклмнопрстуфхцчшщыэюя')
        self.debug = debug


    def frequent_letters_stat(self):
        """ Get counter of the frequent letters in obscene words.

        :return: Counter of the frequent letters in obscene words (dict).
        """
        frequent_letters_cnt = Counter()
        neg_words = marisa_trie.Trie(rd_wr_module(self.neg_words_filename))
        for word in neg_words:
            for letter in word:
                if letter in self.ru_alphabet:
                    frequent_letters_cnt.update([letter])
        frequent_letters_cnt = list(dict(frequent_letters_cnt.most_common()))

        return frequent_letters_cnt


    def bi_grams_stat(self):
        """ Get counter of the bi-grams in obscene words.

        :return: Counter of the bi-grams in obscene words (dict).
        """
        bigrams_cnt = Counter()
        neg_words = marisa_trie.Trie(rd_wr_module(self.neg_words_filename))
        for word in neg_words:
            for i in range(len(word) - 1):
                if word[i] in self.ru_alphabet and word[i + 1] in self.ru_alphabet:
                    bigrams_cnt.update([word[i] + word[i + 1]])
        bigrams_cnt = list(dict(bigrams_cnt.most_common()))

        return bigrams_cnt


    def tri_grams_stat(self):
        """ Get counter of the tri-grams in obscene words.

        :return: Counter of the tri-grams in obscene words (dict).
        """
        trigrams_cnt = Counter()
        neg_words = marisa_trie.Trie(rd_wr_module(self.neg_words_filename))
        for word in neg_words:
            for i in range(len(word) - 2):
                if word[i] in self.ru_alphabet and word[i + 1] in self.ru_alphabet and word[i + 2] in self.ru_alphabet:
                    trigrams_cnt.update([word[i] + word[i + 1] + word[i + 2]])
        trigrams_cnt = list(dict(trigrams_cnt.most_common()))

        return trigrams_cnt


    def get_n_grams(self):
        """ Get tuple of frequent letters, bi-grams and tri-grams based on obscene words.

        :return: frequent letters, bi-grams, tri-grams.
        """
        return self.frequent_letters_stat(), self.bi_grams_stat(), self.tri_grams_stat()


    def save_n_grams(self):
        """ Save stats components in txt. file.

        :return: None.
        """
        filenames = [self.frequent_letters_filename, self.bi_grams_filename, self.tri_grams_filename]
        n_grams = self.get_n_grams()
        for group in zip(n_grams, filenames):
            if self.debug:
                print(f'Filename: {group[1]} Content: {group[0]}')
            rd_wr_module(path_dict=group[1], input_dict=group[0], mode='w')
