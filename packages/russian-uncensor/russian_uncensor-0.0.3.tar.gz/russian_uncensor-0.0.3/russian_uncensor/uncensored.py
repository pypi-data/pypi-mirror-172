from pathlib import Path
import re, string, itertools, marisa_trie
from russian_uncensor.rd_wr_util import rd_wr_module

path_current_file = Path(__file__).parent


class Uncensor:
    def __init__(self, dict_path=None, freq_letter_fn=None, bi_grams_fn=None, tri_grams_fn=None):
        """ Init Uncensor class.

        :param dict_path: path to dictionaries directory.
        :param freq_letter_fn: frequent letters in obscene words filename.
        :param bi_grams_fn: bi-grams in obscene words filename.
        :param tri_grams_fn: tri-grams in obscene words filename.
        :param win_len: sliding window length.
        :return:
        """
        # Paths:
        self.dict_path = Path.joinpath(path_current_file, Path('data')) if dict_path is None else dict_path
        self.freq_letters_fn = self.dict_path/'ngrams/freq_letters.txt' if freq_letter_fn is None else self.dict_path/freq_letter_fn
        self.bi_grams_fn = self.dict_path/'ngrams/bi_grams.txt' if bi_grams_fn is None else self.dict_path/bi_grams_fn
        self.tri_grams_fn = self.dict_path/'ngrams/tri_grams.txt' if tri_grams_fn is None else self.dict_path/tri_grams_fn
        # Dictionaries:
        self.freq_letters = marisa_trie.Trie(rd_wr_module(path_dict=self.freq_letters_fn))
        self.bi_grams = marisa_trie.Trie(rd_wr_module(path_dict=self.bi_grams_fn))
        self.tri_grams = marisa_trie.Trie(rd_wr_module(path_dict=self.tri_grams_fn))
        # Parameters:
        self.win_len = 3
        self.delimiters = string.punctuation


    def moving_window(self, seq):
        """ Moving window with length equal 3 letters and step 1 letter to divide word on windows.

        :param seq: input word.
        :return: divided part of word - window.
        """
        iterator = iter(seq)
        result = tuple(itertools.islice(iterator, self.win_len))
        if len(result) == self.win_len:
            yield result
        for elem in iterator:
            result = result[1:] + (elem, )
            yield result


    def find_variants(self, word):
        """ Find all possible bi- and tri-grams in masked places of the word.

        :param word: input word.
        :return: positions and variant possible bi- and tri-grams.
        """
        if word.find('*') != -1:
            tri_grams_slices = [''.join(gram) for gram in self.moving_window(seq=word)]
            n_win = 0
            possible_letters = dict()
            for gram in tri_grams_slices:
                if gram.find('*') != -1:
                    ind_symbol = [s.start() for s in re.finditer('\*', gram)]
                    ind_enable = [i for i in range(self.win_len) if i not in ind_symbol]
                    letters_cond = [gram[ind] if ind in ind_enable else '' for ind in range(self.win_len)]
                    variants = [tri_gram for tri_gram in self.tri_grams if letters_cond[0] in tri_gram[0] and
                                letters_cond[1] in tri_gram[1] and letters_cond[2] in tri_gram[2]]
                    for ind in ind_symbol:
                        letters = [*set([var[ind] for var in variants if var[ind] in self.freq_letters])]
                        if len(letters) > 0:
                            possible_letters.update({ind + n_win: letters})
                n_win += 1

            return possible_letters

        return None


    def uncensor_masked(self, word):
        """ Find obscene words in hidden (masked) text.

        :param word: input text.
        :return: uncensored (unmasked) variants.
        """
        word = word.lower()
        word = word.translate({ord(ch): "*" for ch in self.delimiters})
        variants = self.find_variants(word=word)
        if variants is None:
            return False, word
        k = list(variants.keys())
        k.append(0)
        uncensored_variants = list()
        particles = list()
        ind_particles = list()
        particles_tmp = None
        ind_tmp = None
        cnt_sequence = 0
        for i in range(len(k) - 1):
            if k[i + 1] - k[i] == 1:
                cnt_sequence += 1
            else:
                if cnt_sequence > 0:
                    particles.append(particles_tmp)
                    ind_particles.append(ind_tmp)
                else:
                    particles.append(variants[k[i]])
                    ind_particles.append(k[i])
                cnt_sequence = 0
            if cnt_sequence == 1:
                particles_tmp = [bi_gram for bi_gram in self.bi_grams if bi_gram[0] in variants[k[i]] and
                                 bi_gram[1] in variants[k[i + 1]]]
                ind_tmp = [k[i], k[i + 1]]
            elif cnt_sequence == 2:
                particles_tmp = [tri_gram for tri_gram in self.tri_grams if tri_gram[0] in variants[k[i - 1]] and
                                 tri_gram[1] in variants[k[i]] and tri_gram[2] in variants[k[i + 1]]]
                ind_tmp = [k[i - 1], k[i], k[i + 1]]

        if len(ind_particles) > 1:
            combs = list(itertools.product(*particles))
            for comb in combs:
                word_listed = list(word)
                order = 0
                for ind in ind_particles:
                    try:
                        sub_order = 0
                        for sub_ind in ind:
                            word_listed[sub_ind] = comb[order][sub_order]
                            sub_order += 1
                    except TypeError:
                        word_listed[ind] = comb[order]
                    order += 1
                uncensored_variants.append(''.join(word_listed))
        else:
            for comb in particles[0]:
                word_listed = list(word)
                try:
                    ind_tmp = 0
                    for ind in ind_particles[0]:
                        word_listed[ind] = comb[ind_tmp]
                        ind_tmp += 1
                    uncensored_variants.append(''.join(word_listed))
                except TypeError:
                    word_listed[ind_particles[0]] = comb
                    uncensored_variants.append(''.join(word_listed))

        return True, uncensored_variants


    def uncensor_splitted(self, sequence):
        """ Find obscene words in splitted text.

        :param sentence: input text.
        :return: uncensored (united) variants.
        """
        words = re.split(f'[{self.delimiters} ]', sequence.lower())
        variants = list()
        for i in range(len(words) - 1):
            prev_word = words[0]
            sentence_str = prev_word
            ind = i
            ind_words = [ind]
            words.pop(0)
            for word in words:
                if prev_word[-1] in self.freq_letters and word[0] in self.freq_letters and prev_word[-1] + word[0] in self.bi_grams:
                    sentence_str += word
                    ind_words.append(ind + 1)
                    variants.append((sentence_str, ind_words.copy()))
                    ind += 1
                    prev_word = word
                else:
                    break

        return variants
