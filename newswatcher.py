
import time
from watchdog.observers import polling
from fileeventhandler import DNDFileEventHandler

class NewsWatcher:
    def __init__(self, src_path, db, ldamodel, topic_classifier, severity_classifier, sentiment_classifier, config):
        self.__src_path = src_path
        self.__db = db
        self.__event_handler = DNDFileEventHandler(self.__db, ldamodel, topic_classifier, severity_classifier, sentiment_classifier, config)
        self.__event_observer = polling.PollingObserver()

    def run(self):

        time.sleep(1)
        self.start()

        try:
            while True:
                time.sleep(1)
                #i=0
        except KeyboardInterrupt:

            self.stop()
            print('exception')
        self.__event_observer.join()


    def start(self):
        self.__schedule()
        time.sleep(1)
        self.__event_observer.start()

    def stop(self):
        self.__event_observer.stop()
        self.__event_observer.join()

    def __schedule(self):
        self.__event_observer.schedule(self.__event_handler, path=self.__src_path, recursive=False)



