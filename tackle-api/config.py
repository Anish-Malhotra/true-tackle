import connexion

from flask_cors import CORS
from swagger_ui_bundle import swagger_ui_3_path
from errors import *

from configuration import db, ma


def _register_error_handlers(app):
    app.add_error_handler(DataNotFoundException, not_found_handler)
    app.add_error_handler(SqlException, sql_exception_handler)
    app.add_error_handler(InvalidInputException, invalid_input_handler)
    app.add_error_handler(SerializationException, serialization_exception_handler)
    
    
def _register_api(app):
    options = {"swagger_path": swagger_ui_3_path}
    app.add_api('swagger.yaml',
            arguments={'title': 'Tackle.Io API'},
            options=options,
            pythonic_params=True)
    
    
def _register_db(app, test_flag = False):
    flask_app = app.app
    if not test_flag:
        flask_app.config.from_pyfile('./configuration/db_config.py')
    else:
        flask_app.config.from_pyfile('./configuration/test_db_config.py')
    db.init_app(flask_app)
    
    # Ensure FOREIGN KEY for sqlite3
    if 'sqlite' in flask_app.config['SQLALCHEMY_DATABASE_URI']:
        def _fk_pragma_on_connect(dbapi_con, con_record):  # noqa
            dbapi_con.execute('pragma foreign_keys=ON')

        with flask_app.app_context():
            from sqlalchemy import event
            event.listen(db.engine, 'connect', _fk_pragma_on_connect)
        
        
def _register_schemas(app):
    flask_app = app.app
    ma.init_app(flask_app)
    
    
def _register_cors(app):
    flask_app = app.app
    CORS(flask_app)
    
    
def create_app(test_flag = False):
    app = connexion.App(__name__, specification_dir='./../')
    _register_api(app)
    _register_db(app, test_flag)
    _register_schemas(app)
    _register_cors(app)
    _register_error_handlers(app)
    return app
    

app = create_app()
