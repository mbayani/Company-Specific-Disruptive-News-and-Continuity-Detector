import pickle
import gensim
import nltk;
import pandas as pd
import spacy
from gensim.models import HdpModel
nltk.download('stopwords')
import gensim.corpora as corpora
from gensim.utils import simple_preprocess


from nltk.corpus import stopwords

class HDPAModel():

    rev_train = None
    rev_test = None
    stop_words = None

    def __init__(self):
        self.rev_train = pd.read_json('./input/input_train.json', encoding="utf-8")
        self.rev_test = pd.read_json('./input/input_test.json', encoding="utf-8")
        #self.rev_train['text_len'] = self.rev_train['title'].apply(lambda x: len(x.split()))

        self.stop_words = stopwords.words('english')

        self.stop_words.extend(
            ['bank', 'banks', 'wells', 'fargo', 'deutsch', 'billion', 'million', 'ubs', 'glaxo', 'hot', 'citigroup',
             'bancorp', 'water', 'deutsche'])

    def strip_newline(self, series):
        return [review.replace('\n', '') for review in series]


    def sent_to_words(self, sentences):
        for sentence in sentences:
            yield (gensim.utils.simple_preprocess(str(sentence), deacc=True))


    def remove_stopwords(self, texts):
        return [[word for word in simple_preprocess(str(doc)) if word not in self.stop_words] for doc in texts]



    def bigrams(self, words, bi_min=15, tri_min=10):
        bigram = gensim.models.Phrases(words, min_count=bi_min)
        trigram = gensim.models.Phrases(bigram[words], min_count=tri_min)
        bigram_mod = gensim.models.phrases.Phraser(bigram)
        trigram_mod = gensim.models.phrases.Phraser(trigram)
        return bigram_mod, trigram_mod



    def lemmatization(self, texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):

        #nlp = spacy.load('en', disable=['parser', 'ner'])
        nlp = spacy.load('en_core_web_sm')

        texts_out = []
        for sent in texts:
            doc = nlp(" ".join(sent))
            texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
        return texts_out

    def get_num_topics(self):

        self.rev_train['title'] = self.strip_newline(self.rev_train.title)
        self.rev_test['title'] = self.strip_newline(self.rev_test.title)
        #rev_train.text[21:22].values

        words_tr = list(self.sent_to_words(self.rev_train.title))
        words_te = list(self.sent_to_words(self.rev_test.title))

        words_tr = self.remove_stopwords(words_tr)

        bigram_tr, trigram_tr = self.bigrams(words_tr)

        trigrams_tr = [trigram_tr[bigram_tr[review]] for review in words_tr]

        lemma_lg = self.lemmatization(trigrams_tr)

        with open('./data/lemma_lg.pkl', 'wb') as f:
            pickle.dump(lemma_lg, f)

        id2word_lg = gensim.corpora.Dictionary(lemma_lg)
        id2word_lg.filter_extremes(no_below=2, no_above=0.6)
        id2word_lg.compactify()
        id2word_lg.save('./data/train_dict_lg')
        corpus_lg = [id2word_lg.doc2bow(text) for text in lemma_lg]

        with open('./data/corpus_lg.pkl', 'wb') as f:
            pickle.dump(corpus_lg, f)

        hdp = HdpModel(corpus_lg, id2word_lg, chunksize=100)
        n_topics = len(hdp.print_topics())
        hdptopics = hdp.print_topics(num_topics=n_topics)

        for tp in hdptopics:
            print(tp)

        return n_topics