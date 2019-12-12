#import sys
from newswatcher import NewsWatcher
from database import Database

def main():
    src_path = '.\input'
    db_path = '.\data'
    print('started ......')

    db = Database(db_path)
    db.clear_alldata()

    NewsWatcher(src_path, db).run()


if __name__ == '__main__':
    main()