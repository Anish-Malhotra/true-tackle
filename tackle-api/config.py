import connexion

from flask_cors import CORS
from swagger_ui_bundle import swagger_ui_3_path
from errors import not_found_handler
from errors import DataNotFoundException

from configuration import db, ma


def register_error_handlers(app):
    app.add_error_handler(DataNotFoundException, not_found_handler)


options = {"swagger_path": swagger_ui_3_path}

app = connexion.App(__name__, specification_dir='./../')

app.add_api('swagger.yaml',
            arguments={'title': 'Tackle.Io API'},
            options=options,
            pythonic_params=True)
flask_app = app.app
flask_app.config.from_pyfile('./configuration/db_config.py')
CORS(flask_app)

db.init_app(flask_app)
ma.init_app(flask_app)
register_error_handlers(app)
