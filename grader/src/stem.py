"""
this class ues nltk to remove stop word and tokenize/lemmatize the ans.
compare two stem seq/sentence and return confidence value of similarities between them

"""
import math


from difflib import SequenceMatcher
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.stem import PorterStemmer



class Stemmer():
    # lang = 'english'
    def remove_stop_word(self, sent):        
        """
        removes stop words from the sentence.
        returns list of word without stop words.
        """
        sent = sent.lower()
        tokenizer = RegexpTokenizer(r'\w+')
        word_list = tokenizer.tokenize(sent)
        clean_list = word_list[:]
        for word in word_list:
            # if word in stopwords.words('english'):
            if word in stopwords.words('german'):
                clean_list.remove(word)
        return clean_list

    def create_stem(self, word_seq):
        """
        create stem seq of a given word seq 
        """
        stemmer = PorterStemmer()
        stems = [stemmer.stem(x) for x in word_seq]
        return stems

    def sent_2_stem(self, sent):
        return self.create_stem(self.remove_stop_word(sent))

    def get_confidence(self, stem_seq, students_ans):
        """
        compare students ans with stem seq (probably examiners ans stem) and return confidence level 
        based on how many stems are common in students ans in compare to examiners ans
        """
        w_seq = self.remove_stop_word(students_ans)
        stems = self.create_stem(w_seq)
        stem_syn = self.add_syn(stems)
        count = 0
        for stem in stem_seq:
            if stem in stem_syn:
                count +=1
        return round((count/len(stem_seq)), 2)

    def compare_sentence(self, sent1, sent2):
        """
        crate stem seq of two given sentences and compare the 2nd one with the first one and 
        return confidence based on how many words from the 1st sentence is present in the 2nd sentence.
        for the purpose of ahes 1st sentence is examiner ans and 2nd sentence is students ans.
        """
        word_seq_1 = self.remove_stop_word(sent1)
        word_seq_2 = self.remove_stop_word(sent2)
        stems_1 = self.create_stem(word_seq_1)
        stems_2 = self.create_stem(word_seq_2)
        count = 0
        for stem in stems_1:
            if stem in stems_2:
                count +=1
        return (count/len(stems_1))

    def get_synonyms(self, word):
        """
        returns list of synonyms of a given word
        """
        synonyms = []
        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                synonyms.append(l.name())
        return synonyms

    def add_syn(self, word_seq):
        """
        return list adding all synonyms of all words in the given word list
        """
        words = []
        for word in word_seq:
            words.append(word)
            syn_list = self.get_synonyms(word)
            for syn in syn_list:
                words.append(syn)
        return set(words)



if __name__ == "__main__":
    sent1 = "a process or set of rules to be followed in calculations or other problem-solving operations, especially by a computer."
    sent2 = "An algorithm is a step by step method of solving a problem. It is commonly used for data processing, calculation and other related computer and mathematical operations.An algorithm is also used to manipulate data in various ways, such as inserting a new data item, searching for a particular item or sorting an item."
    sent3 = "i really dont dont know what algorithm is. but i certainly know it is used in computer to solve a porblem."

    stemmer = Stemmer()
    # examiners_ans = stemmer.remove_stop_word(sent1)
    # examiners_ans = stemmer.create_stem(examiners_ans)
    # confidence = stemmer.get_confidence(examiners_ans, sent2)
    # print(confidence)
    # confidence = stemmer.get_confidence(examiners_ans, sent3)
    # print(confidence)

    stems = stemmer.sent_2_stem(sent1)
    print(stems)
