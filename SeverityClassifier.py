import os
import pickle
import gensim
import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.linear_model import LogisticRegression

class SeverityClassifier(object):
    rev_train = None
    train_id2word = None
    train_corpus4 = None
    lda_train4 = None
    lr = None

    def __init__(self, ldamodel):
        self.__ldamodel = ldamodel

        self.rev_train = pd.read_json(os.path.join('.', 'input', 'input_train.json'), encoding="utf-8")
        self.rev_train['text_len'] = self.rev_train['title'].apply(lambda x: len(x.split()))

        with open(os.path.join('.', 'data', 'train_id2word4.pkl'), 'rb') as f:
            self.train_id2word = pickle.load(f)

        # LOAD IN THE TRAIN LDA MODEL
        self.lda_train4 = gensim.models.LdaModel.load(os.path.join('.', 'data', 'lda_train4.model'))

        with open(os.path.join('.', 'data', 'train_corpus4.pkl'), 'rb') as f:
            self.train_corpus4 = pickle.load(f)

    def train_severity_classifier(self):
        train_vecs = []

        # Train classification model
        for i in range(len(self.rev_train)):
            top_topics = self.lda_train4.get_document_topics(self.train_corpus4[i], minimum_probability=0.0)
            topic_vec = [top_topics[j][1] for j in range(2)]
            train_vecs.append(topic_vec)

        X = np.array(train_vecs)
        y = np.array(self.rev_train.score)

        # Logisitic Regression
        self.lr = LogisticRegression(
            class_weight='balanced',
            solver='newton-cg',
            fit_intercept=True
        ).fit(X, y)

        y_pred = self.lr.predict(X)
        print(y_pred)

    def run_unseendata(self, unseen_text):
        testdata = {'title': [unseen_text]}
        testdataframe = DataFrame(testdata, columns=['title'])
        bigram_test = self.__ldamodel.get_bigram(testdataframe)

        test_corpus = [self.train_id2word.doc2bow(text) for text in bigram_test]

        test_vecs1 = []
        top_topics1 = self.lda_train4.get_document_topics(test_corpus[0], minimum_probability=0.0)

        topic_vec1 = [top_topics1[i][1] for i in range(2)]
        # topic_vec.extend([rev_test.iloc[i].real_counts]) # counts of reviews for restaurant
        # topic_vec1.extend([len(rev_test.iloc[0].title)]) # length review
        test_vecs1.append(topic_vec1)

        y_pred = self.lr.predict(test_vecs1)

        return y_pred[0]
