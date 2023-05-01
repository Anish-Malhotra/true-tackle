import os

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.abspath("tkldb.sqlite")
PROPAGATE_EXCEPTIONS = True
