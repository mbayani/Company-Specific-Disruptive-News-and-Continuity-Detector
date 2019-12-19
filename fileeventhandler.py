import os
import json
from watchdog.events import PatternMatchingEventHandler
from preprocessor import PreProcessor
from analyzer import Analyzer
from dataviewer import Dataviewer


class DNDFileEventHandler(PatternMatchingEventHandler):
    patterns = ["*.json"]

    def __init__(self, db, ldamodel, topic_classifier, severity_classifier, sentiment_classifier, config):
        super().__init__()
        self.__db = db
        self.__preprocessor = PreProcessor(db)
        self.__analyzer = Analyzer(db, ldamodel, topic_classifier, severity_classifier, sentiment_classifier, config)
        self.__dataviewer = Dataviewer(db, config)
        self.__ldamodel = ldamodel
        self.__config = config

    def on_modified(self, event):
        self.process(event.src_path)

    def on_created(self, event):
        self.process(event.src_path)




    def process(self, filepath):
        #print(f'event type: {event.event_type}  path : {event.src_path}')

        file_name = os.path.basename(filepath)

        with open(filepath, 'r') as myfile:
            data = myfile.read()

            obj = json.loads(data)
            upproc_docid = self.__db.insert_unprocessed(file_name, obj)

            self.__ldamodel.run_unseendata(str(obj['title']))

            #PRE-PROCESSING
            print('Started Pre-Processsing .......')
            preproc_docid = self.__preprocessor.preprocess(upproc_docid)
            print('Completed Pre-Processsing .......')

            #ANALYZE
            print('Started Analyzing .......')
            is_analyzed = self.__analyzer.analyze(preproc_docid, upproc_docid)
            print('Completed Analyzing .......')

            if is_analyzed == True  and  self.__config['Settings']['batch-runner'] == 0:
                topic_to_watch = self.__config['Settings']['topic-to-watch']
                #UPDATE VIEWER
                print('Started Graph .......')
                self.__dataviewer.plot(topic_to_watch)
                print('Completed Graph .......')
