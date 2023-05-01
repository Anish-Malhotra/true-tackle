import connexion

from flask_cors import CORS
from swagger_ui_bundle import swagger_ui_3_path
from errors import *

from configuration import db, ma

# We wrap common errors in custom exception handlers that Flask uses when invoking the controllers
def _register_error_handlers(app):
    app.add_error_handler(DataNotFoundException, not_found_handler)
    app.add_error_handler(SqlException, sql_exception_handler)
    app.add_error_handler(InvalidInputException, invalid_input_handler)
    app.add_error_handler(SerializationException, serialization_exception_handler)
    

# We're using the Flask wrapper 'Connexion' to create the app and use the OpenAPI spec
# to register the API endpoints with the controller functions and perform validation
def _register_api(app):
    options = {"swagger_path": swagger_ui_3_path}
    app.add_api('openapi.yaml',
            arguments={'title': 'Tackle.Io API'},
            options=options,
            pythonic_params=True)
    

# Here we pass in a 'test_flag' parameter to determine if we're running in a test environment
# Which uses a separate sqlite3 database for testing purposes
def _register_db(app, test_flag = False):
    flask_app = app.app
    if not test_flag:
        flask_app.config.from_pyfile('./configuration/db_config.py')
    else:
        flask_app.config.from_pyfile('./configuration/test_db_config.py')
    db.init_app(flask_app)
    
    # Ensure FOREIGN KEY constraints for sqlite3, which aren't enfored by SQLAlchemy by default
    if 'sqlite' in flask_app.config['SQLALCHEMY_DATABASE_URI']:
        def _fk_pragma_on_connect(dbapi_con, con_record):
            dbapi_con.execute('pragma foreign_keys=ON')

        with flask_app.app_context():
            from sqlalchemy import event
            event.listen(db.engine, 'connect', _fk_pragma_on_connect)
        

# We register the Marshmallow schemas with the Flask application
# Using Marshmallow schemas in our controllers lets us avoid unnecessary manual JSON serialization
def _register_schemas(app):
    flask_app = app.app
    ma.init_app(flask_app)
    

# Setup CORS   
def _register_cors(app):
    flask_app = app.app
    CORS(flask_app)
    

# A top-level function to create the Flask application
def create_app(test_flag = False):
    app = connexion.App(__name__, specification_dir='./../')
    _register_api(app)
    _register_db(app, test_flag)
    _register_schemas(app)
    _register_cors(app)
    _register_error_handlers(app)
    return app
    

app = create_app()
