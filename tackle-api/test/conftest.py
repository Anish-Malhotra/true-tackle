from config import create_app

from configuration import db as _db
from util import build_or_refresh_db

import pytest
import webtest as wt

@pytest.fixture(scope='function')
def app():
    _app = create_app(test_flag=True)
    ctx = _app.app.test_request_context()
    ctx.push()
    
    yield _app.app
    ctx.pop()
    
    
@pytest.fixture(scope='function')
def testapp(app):
    """A Webtest app."""
    return wt.TestApp(app)


@pytest.fixture(scope='function', autouse=True)
def db(app):
    """A database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    build_or_refresh_db()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()
    