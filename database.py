from datetime import datetime
from tinydb import TinyDB

class Database:
    def __init__(self, db_path):
        self.db_unprocessed = TinyDB(db_path + '\\db_unprocessed.json')
        self.db_preprocessed = TinyDB(db_path + '\\db_processed.json')
        self.db_analyzed = TinyDB(db_path + '\\db_analyzed.json')

    def clear_alldata(self):
        self.db_unprocessed.purge()
        self.db_preprocessed.purge()
        self.db_analyzed.purge()

    def insert_unprocessed(self, filename, data):
        docid = self.db_unprocessed.insert({'file_name': filename, 'rec_created': datetime.now().__str__(), 'site': str(data['site']), 'organization': str(data['organization']), 'published': str(data['published']), 'title': str(data['title']), 'text': str(data['text'])  })
        return docid

    def insert_preprocessed(self, unprocessed_doc_id):
        rec = self.db_unprocessed.get(doc_id=unprocessed_doc_id)
        docid = self.db_preprocessed.insert({'unproc_id': unprocessed_doc_id, 'organization':  rec["organization"], 'published': rec["published"], 'title': rec["title"], 'text': "" })
        return docid

    def insert_analyzed(self, processed_doc_id):
        rec = self.db_preprocessed.get(doc_id=processed_doc_id)
        docid = self.db_analyzed.insert({'document_id': processed_doc_id, 'published': rec["published"], 'text': rec["text"], 'severity': "", 'sentiments': "" })
        return docid

    def get_unpreprocessed_text(self, unprocessed_doc_id):
        rec = self.db_unprocessed.get(doc_id=unprocessed_doc_id)
        unprocessed_text = rec["text"]
        return unprocessed_text

    def update_preprocessed_text(self, processed_doc_id, preprocessed_text):
        self.db_preprocessed.update({'text': preprocessed_text}, doc_ids=[processed_doc_id])

    def update_anlyzed(self, documnet_id, severity, sentiments):
        self.db_analyzed.update({'severity': severity, 'sentiments': sentiments}, doc_ids=[documnet_id])

    def get_preprocessed_text(self, processed_doc_id):
        rec = self.db_preprocessed.get(doc_id=processed_doc_id)
        processed_text = rec["text"]
        return processed_text