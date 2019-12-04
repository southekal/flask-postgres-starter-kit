import uuid
from flask import (
	Blueprint, 
	render_template, 
	flash, redirect, 
	url_for
)
from flask_login import current_user

from app import (
	app,
	mp
)
from app.forms import RegisterForm


mod_home = Blueprint('home', __name__, url_prefix='')


@mod_home.route("/", methods=['GET', 'POST'])
def index():

	form = RegisterForm()
	return render_template("home/index.html", form=form)


