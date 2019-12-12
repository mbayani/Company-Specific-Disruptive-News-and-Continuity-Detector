import os
import json
from watchdog.events import PatternMatchingEventHandler
from preprocessor import PreProcessor
from analyzer import Analyzer
from dataviewer import Dataviewer

class DNDFileEventHandler(PatternMatchingEventHandler):
    patterns = ["*.json"]

    def __init__(self, db):
        super().__init__()
        self.__db = db
        self.__preprocessor = PreProcessor(db)
        self.__analyzer = Analyzer(db)
        self.__dataviewer = Dataviewer(db)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

    def process(self, event):
        #print(f'event type: {event.event_type}  path : {event.src_path}')

        file_name = os.path.basename(event.src_path)

        with open(event.src_path, 'r') as myfile:
            data = myfile.read()

            obj = json.loads(data)
            upproc_docid = self.__db.insert_unprocessed(file_name, obj)

            #PRE-PROCESSING
            print('Started Pre-Processsing .......')
            preproc_docid = self.__preprocessor.preprocess(upproc_docid)
            print('Completed Pre-Processsing .......')

            #ANALYZE
            print('Started Analyzing .......')
            self.__analyzer.analyze(preproc_docid)
            print('Completed Analyzing .......')

            #UPDATE VIEWER
            print('Started Graph .......')
            self.__dataviewer.plot()
            print('Completed Graph .......')
