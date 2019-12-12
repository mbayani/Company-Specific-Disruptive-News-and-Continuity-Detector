

class Analyzer:
    def __init__(self, db):
        self.__db = db

    def analyze(self, preproc_docid):
        preproc_docid = self.__db.insert_analyzed(preproc_docid)
        self.analyze_text(preproc_docid)

    def analyze_text(self, preproc_docid):

        processed_text = self.__db.get_preprocessed_text(preproc_docid)
        severity = "6"  #TODO remove hard coded value
        sentiments = "N" #TODO remove hard coded value

        # TODO write code for analyzis

        self.__db.update_anlyzed(preproc_docid, severity, sentiments)
