

class PreProcessor:
    def __init__(self, db):
        self.__db = db

    def preprocess(self, unproc_docid):
        preproc_docid = self.__db.insert_preprocessed(unproc_docid)

        self.preprocess_text(unproc_docid, preproc_docid)
        return preproc_docid


    def preprocess_text(self, unproc_docid, preproc_docid):
        unprocessed_text = self.__db.get_unpreprocessed_text(unproc_docid)
        preprocessed_text = 'tt'  #TODO remove the hard coded value
        # TODO write code to preprocess text


        self.__db.update_preprocessed_text(preproc_docid, preprocessed_text)


