#import sys
from newswatcher import NewsWatcher
from database import Database
import os

def main():
    src_path =  os.path.join('.','input')
    db_path = os.path.join('.', 'data')
    print('started ......')

    if not os.path.exists(src_path):
        os.mkdir(src_path)
    print('Input Path: ', os.path.abspath(src_path))

    db = Database(db_path)
    db.clear_alldata()

    NewsWatcher(src_path, db).run()


if __name__ == '__main__':
    main()