'''
A utility class to handle all Database operation. A file is used as database here.
'''
import os
from datetime import datetime

from tinydb import TinyDB


class Database(object):
    def __init__(self, db_path):
        self.db_unprocessed = TinyDB(os.path.join(db_path, 'db_unprocessed.json'))
        self.db_preprocessed = TinyDB(os.path.join(db_path, 'db_processed.json'))
        self.db_analyzed = TinyDB(os.path.join(db_path, 'db_analyzed.json'))

    def clear_alldata(self):
        self.db_unprocessed.purge()
        self.db_preprocessed.purge()
        self.db_analyzed.purge()

    def insert_unprocessed(self, filename, data):
        docid = self.db_unprocessed.insert(
            {'file_name': filename, 'rec_created': datetime.now().__str__(), 'site': str(data['site']),
             'organization': str(data['organization']), 'published': str(data['published']),
             'title': str(data['title']), 'text': str(data['text'])})
        return docid

    def insert_preprocessed(self, unprocessed_doc_id):
        rec = self.db_unprocessed.get(doc_id=unprocessed_doc_id)
        docid = self.db_preprocessed.insert(
            {'unproc_id': unprocessed_doc_id, 'organization': rec["organization"], 'published': rec["published"],
             'title': rec["title"], 'text': ""})
        return docid

    def insert_analyzed(self, processed_doc_id, upproc_docid):
        rec = self.db_unprocessed.get(doc_id=upproc_docid)
        docid = self.db_analyzed.insert(
            {'unproc_doc_id': upproc_docid, 'proc_doc_id': processed_doc_id, 'published': rec["published"],
             'title': rec["title"], 'topic': '', 'severity': '', 'sentiments': '', 'text': rec["text"]})
        return docid

    def get_unpreprocessed_text(self, unprocessed_doc_id):
        rec = self.db_unprocessed.get(doc_id=unprocessed_doc_id)
        unprocessed_text = rec["title"]
        return unprocessed_text

    def update_preprocessed_text(self, processed_doc_id, preprocessed_text):
        self.db_preprocessed.update({'text': preprocessed_text}, doc_ids=[processed_doc_id])

    def update_anlyzed(self, documnet_id, severity, sentiments, topic):
        self.db_analyzed.update({'topic': topic, 'severity': str(severity), 'sentiments': str(sentiments)},
                                doc_ids=[documnet_id])

    def get_preprocessed_text(self, processed_doc_id):
        rec = self.db_preprocessed.get(doc_id=processed_doc_id)
        processed_text = rec["text"]
        return processed_text
