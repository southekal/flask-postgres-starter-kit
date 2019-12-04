import os
from flask import (
	Flask, 
	flash,
	redirect,
	render_template, 
	request, 
	url_for
)
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import (
	CSRFError,
	CSRFProtect
)
from mixpanel import Mixpanel

from config import Config
from log_config.custom_logger import logger

app = Flask(__name__)
app.config.from_object(os.environ.get('APP_SETTINGS', Config))
csrf = CSRFProtect(app)
login = LoginManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# setup mixpanel tracking
mp = Mixpanel(os.environ.get("MIXPANEL_PROJECT_ID"))

# Sample HTTP error handling
@app.errorhandler(401)
def unauthorized(error):
    logger.error(f'unauthorized access {error} - {request.url}')
    flash("please login to view this page")
    return redirect(url_for('auth.login'))


@app.errorhandler(404)
def not_found(error):
    logger.warning(f'page not found {error} - {request.url}')
    return render_template('error_pages/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    logger.error(f'server error {error} - {request.url}')
    return render_template('error_pages/500.html'), 500


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
	logger.error(f"csrf error; {e}")
	return render_template('error_pages/csrf_error.html', reason=e.description), 400


from app.mod_auth.controller import mod_auth as auth_module
from app.mod_home.controller import mod_home as home_module

app.register_blueprint(auth_module)
app.register_blueprint(home_module)


