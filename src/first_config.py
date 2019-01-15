from os import path

basedir = path. abspath(path.join(path.dirname(__file__), '..'))


class Config(object):

    DATABASE_DIR = 'database'
    DATABASE_JSON = '{}/{}/training_db.json'.format(basedir, DATABASE_DIR)
    TEST_RESOURCE_DIR = '{}/test/resources'.format(basedir)
    DOWNLOADS_DIR = path.expanduser('~/Downloads')
