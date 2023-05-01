import connexion

from swagger_ui_bundle import swagger_ui_3_path

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


options = {"swagger_path": swagger_ui_3_path}

app = connexion.App(__name__, specification_dir='./../')

app.add_api('swagger.yaml',
            arguments={'title': 'Tackle.Io API'},
            options=options,
            pythonic_params=True)
flask_app = app.app
flask_app.config.from_pyfile('db_config.py')
CORS(flask_app)

db = SQLAlchemy(flask_app)
