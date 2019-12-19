
import os
import time
from newswatcher import NewsWatcher
from database import Database
from ldamodel import LDAModel
from dataviewer import Dataviewer
from topicsclassifier import TopicsClassifier
from SeverityClassifier import SeverityClassifier
from SentimentsClassifier import SentimentsClassifier
from fileeventhandler import DNDFileEventHandler
import toml
from hdpmodel import HDPAModel


config = toml.load('./config.toml')

def main():
    print('started ......')

    src_path = './input' #This is for input files for program
    db_path = './data'   #This is for storing database files and temp files
    repository_path = './repository'  #This is for test files

    #These folders and its contents are mandatory
    if not os.path.exists(src_path):
        print("ERROR: The requierd folder '{}'doesn't exist".format(src_path))
        raise

    if not os.path.exists(repository_path):
        print("ERROR: The requierd folder '{}'doesn't exist".format(repository_path))
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
    # unseen_text = 'How Wells Fargo and Federal Reserve Struck Deal to Hold Bank’s Board Accountable'
    # tptest = topic_classifier.run_unseendata(unseen_text)
    # print(tptest)

    print('.......Severity Classification Model started......')
    severity_classifier.train_severity_classifier()
    print('.......Severity Classification Model Completed......')

    # #Severity classifier test
    # unseen_text = 'How Wells Fargo and Federal Reserve Struck Deal to Hold Bank’s Board Accountable'
    # svtest = severity_classifier.run_unseendata(unseen_text)
    # print(svtest)


    print('.......Sentiment Classifier Model started......')
    sentiment_classifier.train_sentiments_classifier()
    print('.......Sentiment Classifier Model Completed......')

    # # SentimentClassifier test
    # unseen_text = 'How Wells Fargo and Federal Reserve Struck Deal to Hold Bank’s Board Accountable'
    # sntest = sentiment_classifier.run_unseendata(unseen_text)
    # print(sntest )

    print('.......Application is Ready......')

    #this will test the applciation with a bunch of test files
    if is_batch_run == 1:

        all_files = os.listdir("./repository/")

        json_input_files = filter(lambda x: x[-8:] == 'WFC.json', all_files)

        filelist = []
        for x in json_input_files:
            filelist.append(x)

        filelist.sort()

        file_handler = DNDFileEventHandler(db, ldamodel, topic_classifier, severity_classifier,
                                                   sentiment_classifier, config)

        for file in filelist:
            filepath = os.path.join('./repository/', file)
            file_handler.process(filepath)

            time.sleep(2)

        topic_to_watch = config['Settings']['topic-to-watch']

        #Plot Graph
        print('Started Graph .......')
        dataviewer = Dataviewer(db, config)
        dataviewer.plot(topic_to_watch)
        print('Completed Graph .......')

    else: #This is for interactive mode user can add news files to input folder and see how it is getting analyzed
        NewsWatcher(src_path, db, ldamodel, topic_classifier, severity_classifier, sentiment_classifier, config).run()

    #Plot the stock graph for the given period
    if config['Settings']['show-stock-graph']  == 1:
        dataviewer = Dataviewer(db, config)
        graph_legent = 'Stock Price'
        print('Started Stock Graph .......')
        dataviewer.plot_stock(graph_legent)
        print('Completed Stock Graph .......')


if __name__ == '__main__':
    main()