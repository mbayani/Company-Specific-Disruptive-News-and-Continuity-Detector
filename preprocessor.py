
#from gensim.parsing.preprocessing import remove_stopwords
import nltk
from nltk.tokenize import word_tokenize
#from nltk.stem import PorterStemmer

# Download nltk packages used in this example
nltk.download('stopwords')
nltk.download('punkt')

class PreProcessor:
    def __init__(self, db):
        self.__db = db

    def preprocess(self, unproc_docid):
        preproc_docid = self.__db.insert_preprocessed(unproc_docid)

        self.preprocess_text(unproc_docid, preproc_docid)
        return preproc_docid


    def preprocess_text(self, unproc_docid, preproc_docid):
        unprocessed_text = self.__db.get_unpreprocessed_text(unproc_docid)
        preprocessed_text = '' #remove_stopwords(unprocessed_text)

        # set of stop words
        stop_words = nltk.corpus.stopwords.words('english') + [
            '.',
            ',',
            '--',
            '\'s',
            '?',
            ')',
            '(',
            ':',
            '\'',
            '\'re',
            '"',
            '-',
            '}',
            '{',
            u'—',
        ]

        # tokens of words
        word_tokens = word_tokenize(unprocessed_text)

        filtered_sentence = []

        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)

                #print(preprocessed_text)

        # Stem_words = []
        # ps = PorterStemmer()
        # for w in filtered_sentence:
        #     rootWord = ps.stem(w)
        #     Stem_words.append(rootWord)
        #print(filtered_sentence)
        #print(Stem_words)

        #preprocessed_text =   " ".join(Stem_words) # " ".join(filtered_sentence)

        preprocessed_text = " ".join(filtered_sentence)

        self.__db.update_preprocessed_text(preproc_docid, preprocessed_text)


