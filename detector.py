'''
Disruptive News Detector

It reads news to detect any disruptive news about a company.
There are 2 modes to run it (driven by settings)- 1) Batch Mode and 2) Continous Monitoring

1) Batch Mode - It reads already stored news from a folder and process them. It shows on graph the disruptive news
    severity. Along with it, it pulls the stock price for that company during that time period. Trying to depict
    the affect of disruptive news on its stock price.

2) Continous Monitoring - We can run the program to process live news feed. As soon as news is dropped in a folder,
    it will be processed, stock process are pulled to show the affect of news.

Before running this project, please make sure you have all the required python modules installed.
It has Python 3.x dependency defined.
To install python libraries, run below command:
(make sure 'requirements.txt' file is available where you are running it )

pip3 install -r requirements.txt



'''
import os
import time
import nltk
import toml
from SentimentsClassifier import SentimentsClassifier
from SeverityClassifier import SeverityClassifier
from database import Database
from dataviewer import Dataviewer
from fileeventhandler import DNDFileEventHandler
from hdpmodel import HDPAModel
from ldamodel import LDAModel
from newswatcher import NewsWatcher
from topicsclassifier import TopicsClassifier

# Load Stopwords and punkt
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

config = toml.load('./config.toml')


def main():
    print('Started ......')
    src_path = os.path.join('.', 'input')  # This is for input files for program
    db_path = os.path.join('.', 'data')  # This is for storing database files and temp files
    repository_path = os.path.join('.', 'repository')  # This is for test files

    # These folders and its contents are mandatory
    if not os.path.exists(src_path):
        print("ERROR: The required folder '{}'doesn't exist.".format(src_path))
        raise

    print('Input Path: ', os.path.abspath(src_path))

    if not os.path.exists(repository_path):
        print("ERROR: The required folder '{}'doesn't exist".format(repository_path))
        raise

    # Create these folders if doesn't exist
    if not os.path.exists(db_path):
        os.makedirs(db_path)

    is_batch_run = config['Settings']['batch-runner']

    db = Database(db_path)
    db.clear_alldata()

    ldamodel = LDAModel()

    if config['Settings']['run-hdp-model'] == 1:
        hdpmodel = HDPAModel()

        print('.......HDP Modeling started......')
        numtopics = hdpmodel.get_num_topics()

        print("Number of topics estimation by HDP: {}".format(numtopics))
        print('.......HDP Modeling Completed......')

    if config['Settings']['use_preprocessed_models'] == 0:
        #First create the LDA model
        print('.......LDA Modeling started......')
        ldamodel.train_lda_model()
        print('.......LDA Modeling Completed......')

    topic_classifier = TopicsClassifier(ldamodel)
    severity_classifier = SeverityClassifier(ldamodel)
    sentiment_classifier = SentimentsClassifier(ldamodel)

    print('.......Topic Classification Model started......')
    topic_classifier.train_topic_classifier()
    print('.......Topic Classification Model Completed......')

    # #Topic classifier test
    # unseen_text = 'How Wells Fargo and Federal Reserve Struck Deal to Hold Bank's Board Accountable'
    # tptest = topic_classifier.run_unseendata(unseen_text)
    # print(tptest)

    print('.......Severity Classification Model started......')
    severity_classifier.train_severity_classifier()
    print('.......Severity Classification Model Completed......')

    # #Severity classifier test
    # unseen_text = 'How Wells Fargo and Federal Reserve Struck Deal to Hold Bank's Board Accountable'
    # svtest = severity_classifier.run_unseendata(unseen_text)
    # print(svtest)

    print('.......Sentiment Classifier Model started......')
    sentiment_classifier.train_sentiments_classifier()
    print('.......Sentiment Classifier Model Completed......')

    # # SentimentClassifier test
    # unseen_text = 'How Wells Fargo and Federal Reserve Struck Deal to Hold Bank's Board Accountable'
    # sntest = sentiment_classifier.run_unseendata(unseen_text)
    # print(sntest )

    print('.......Application is Ready......')

    # this will test the applciation with a bunch of test files
    if is_batch_run == 1:
        batch_mode(db, ldamodel, repository_path, sentiment_classifier, severity_classifier, topic_classifier)
    else:  # This is for interactive mode user can add news files to input folder and see how it is getting analyzed
        NewsWatcher(src_path, db, ldamodel, topic_classifier, severity_classifier, sentiment_classifier, config).run()

    # Plot the stock graph for the given period
    if config['Settings']['show-stock-graph'] == 1:
        dataviewer = Dataviewer(db, config)
        graph_legent = 'Stock Price'
        print('Started Stock Graph .......')
        dataviewer.plot_stock(graph_legent)
        print('Completed Stock Graph .......')


def batch_mode(db, ldamodel, repository_path, sentiment_classifier, severity_classifier, topic_classifier):
    '''
    This method process all the news availabel in input folder.
    :param db: db instance
    :param ldamodel: LDAModel instance
    :param repository_path: repository Path
    :param sentiment_classifier: Sentiment Classifier instance
    :param severity_classifier: Severity Classifier instance
    :param topic_classifier: Topic Classifier instance
    '''
    print('Running in Batch Mode......')
    all_files = os.listdir(repository_path)
    json_input_files = filter(lambda x: x[-8:] == 'WFC.json', all_files)
    filelist = []
    for x in json_input_files:
        filelist.append(x)
    filelist.sort()
    file_handler = DNDFileEventHandler(db, ldamodel, topic_classifier, severity_classifier,
                                       sentiment_classifier, config)
    for file in filelist:
        filepath = os.path.join(repository_path, file)
        file_handler.process(filepath)

        time.sleep(2)
    topic_to_watch = config['Settings']['topic-to-watch']
    # Plot Graph
    print('Started Graph .......')
    dataviewer = Dataviewer(db, config)
    dataviewer.plot(topic_to_watch)
    print('Completed Graph .......')


if __name__ == '__main__':
    main()
