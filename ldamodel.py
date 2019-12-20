'''
This class uses Latent Dirichlet method.

'''
import os
import pickle
import nltk
import pandas as pd
from pandas import DataFrame
nltk.download('stopwords')
import gensim.corpora as corpora
from gensim.models import CoherenceModel
from nltk.corpus import stopwords
import gensim
from gensim.utils import simple_preprocess
from nltk.stem import WordNetLemmatizer, SnowballStemmer

nltk.download('wordnet')

stemmer = SnowballStemmer("english")

class LDAModel(object):
    processed_docs = []
    rev_train = None
    stop_words = None
    dictionary = None
    lda_train4 = None

    def __init__(self):

        self.rev_train = pd.read_json(os.path.join('.', 'input', 'input_train.json'), encoding="utf-8")
        self.rev_train['text_len'] = self.rev_train['title'].apply(lambda x: len(x.split()))

        self.stop_words = stopwords.words('english')

        self.stop_words.extend(
            ['wells', 'fargo', 'deutsch', 'ubs', 'glaxo', 'million','citigroup', 'billion', 'america', 'bancorp', 'deutsche', 'cole', 'anthoni' ])

    def strip_newline(self, series):
        return [review.replace('\n', '') for review in series]

    def sent_to_words(self, sentences):
        for sentence in sentences:
            yield (gensim.utils.simple_preprocess(str(sentence), deacc=True))

    def remove_stopwords(self, texts):
        return [[word for word in simple_preprocess(str(doc)) if word not in self.stop_words] for doc in texts]

    def bigrams(self, words, bi_min=15, tri_min=10):
        bigram = gensim.models.Phrases(words, min_count=bi_min)
        bigram_mod = gensim.models.phrases.Phraser(bigram)
        return bigram_mod

    def lemmatize_stemming(self, text):
        return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

    # Tokenize and lemmatize
    def preprocess(self, text):


        result = []
        for token in gensim.utils.simple_preprocess(text):
            if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
                result.append(self.lemmatize_stemming(token))

        return " ".join(result)

    def get_corpus(self, df):
        """
        Get Bigram Model, Corpus, id2word mapping
        """
        df['title'] = self.strip_newline(df.title)
        words = list(self.sent_to_words(df.title))
        words = self.remove_stopwords(words)
        bigram = self.bigrams(words)
        bigram = [bigram[review] for review in words]
        id2word = gensim.corpora.Dictionary(bigram)
        id2word.filter_extremes(no_below=0, no_above=0.5, keep_n=1000)
        id2word.compactify()
        corpus = [id2word.doc2bow(text) for text in bigram]
        return corpus, id2word, bigram

    def train_lda_model(self):

        print('**************Training data for LDA before pre-processing********************')
        for txt in self.rev_train['title'] :
            print(txt)
        print('*****************************************************************************')

        self.rev_train['title'] = self.rev_train.title.apply(lambda x: self.preprocess(x))

        print('**************Training data for LDA after pre-processing********************')
        for txt in self.rev_train['title'] :
            print(txt)
        print('*****************************************************************************')

        train_corpus4, train_id2word4, bigram_train4 = self.get_corpus(self.rev_train)

        with open(os.path.join('.', 'data', 'train_corpus4.pkl'), 'wb') as f:
            pickle.dump(train_corpus4, f)
        with open(os.path.join('.', 'data', 'train_id2word4.pkl'), 'wb') as f:
            pickle.dump(train_id2word4, f)
        with open(os.path.join('.', 'data', 'bigram_train4.pkl'), 'wb') as f:
            pickle.dump(bigram_train4, f)

        self.lda_train4 = gensim.models.LdaModel(corpus=train_corpus4,
                                            num_topics=2,
                                            id2word=train_id2word4,
                                            chunksize=100,
                                            passes=50,
                                            random_state= 1000,
                                            eval_every=1,
                                            per_word_topics=True)

        print('----------Topics are -------------')

        for idx, topic in self.lda_train4.print_topics(-1):
            print("Topic: {} \nWords: {}".format(idx, topic))
            print("\n")

        print('-----------------------------------')

        self.lda_train4.save(os.path.join('.', 'data','lda_train4.model'))

        # self.lda_model = lda_train4
        self.dictionary = train_id2word4

    def get_bigram(self, df):
        df['title'] = self.strip_newline(df.title)
        words = list(self.sent_to_words(df.title))
        words = self.remove_stopwords(words)
        bigram = self.bigrams(words)
        bigram = [bigram[review] for review in words]
        return bigram

    def run_unseendata(self, text):

        # Data preprocessing step for the unseen document
        # bow_vector = self.dictionary.doc2bow(self.preprocess(text))

        testdata = {'title': [text]}

        testdataframe = DataFrame(testdata, columns=['title'])

        bigram_test = self.get_bigram(testdataframe)

        test_corpus = [self.dictionary.doc2bow(text) for text in bigram_test]

        test_vecs1 = []
        top_topics1 = self.lda_train4.get_document_topics(test_corpus[0], minimum_probability=0.0)

        print(top_topics1)

        # topic_vec1 = [top_topics1[i][1] for i in range(2)]
        #
        # test_vecs1.append(topic_vec1)
        #
        # for index, score in sorted(self.lda_train4[test_vecs1], key=lambda tup: -1*tup[1]):
        #     print("Score: {}\t Topic: {}".format(score, self.lda_train4.print_topic(index, 5)))

        print('***************************************************')
