class Analyzer(object):
    def __init__(self, db, ldamodel, topic_classifier, severity_classifier, sentiment_classifier, config):
        self.__db = db
        self.__ldamodel = ldamodel
        self.__topic_classifier = topic_classifier
        self.__severity_classifier = severity_classifier
        self.__sentiment_classifier = sentiment_classifier
        self.__config = config

    def analyze(self, preproc_docid, upproc_docid):
        analyze_docid = self.__db.insert_analyzed(preproc_docid, upproc_docid)

        text = self.__db.get_unpreprocessed_text(upproc_docid)
        result = self.analyze_text(analyze_docid, text)
        return result

    def analyze_text(self, analyze_docid, text):

        #processed_text = self.__db.get_preprocessed_text(preproc_docid)
        result = False
        topic = self.__topic_classifier.run_unseendata(text)

        print("Topic: {}".format(topic))

        topic_to_watch =  self.__config['Settings']['topic-to-watch']

        if topic == topic_to_watch :

            print("topic: {} matched, started analyzing the topic".format(topic))

            severity =   self.__severity_classifier.run_unseendata(text)
            sentiments = self.__sentiment_classifier.run_unseendata(text)

            #print("Text: {}".format(text))
            print("Severity: {}".format(severity))
            print("Sentiment: {}".format(sentiments))

            self.__db.update_anlyzed(analyze_docid, severity, sentiments, topic)

            result = True

        else:
            print("topic: {} for this news is not same as topic interested: {}, skipping analysis".format(topic, topic_to_watch))
            print("Text: {}".format(text))
            severity = ''
            sentiments = ''
            self.__db.update_anlyzed(analyze_docid, severity, sentiments, topic)

        return result