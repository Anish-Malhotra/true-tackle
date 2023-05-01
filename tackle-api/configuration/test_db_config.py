import os

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.abspath("test/tkldb.sqlite")