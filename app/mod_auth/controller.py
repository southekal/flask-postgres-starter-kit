import json

from flask import (
	current_app,
	Blueprint, 
	flash,
	make_response,
	redirect,
	render_template, 
	request,
	url_for
)
from flask_jwt_extended import ( 
    set_access_cookies, 
    unset_jwt_cookies
)
from flask_login import (
	current_user, 
	login_required,
	login_user, 
	logout_user
)
import requests

from app import (
	db, 
	mp
)
from app.forms import (
	LoginForm, 
	RegisterForm,
	SettingsForm
)
from app.email import MailGunEmailService
from app.models import BaseUser
from bin.helper import timestamp_formatter
from bin.helper.models import (
	db_base,
	db_case_insensitive
)
from log_config.custom_logger import logger


mod_auth = Blueprint('auth', __name__, url_prefix='')


@mod_auth.route("/register", methods=['GET', 'POST'])
def register():

	form = RegisterForm()

	if current_user.is_authenticated:
		mp.track(f"user_{current_user.id}", "register visit")
		return redirect(url_for('dashboard.landing'))

	if form.validate_on_submit():	
		user = BaseUser(
			name=form.name.data, 
			email=form.email.data, 
			time_zone=form.time_zone.data
		)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		login_user(user)

		logger.info(f"registering user; {form.name.data}; {form.email.data}")
		m = MailGunEmailService()
		m.send_welcome_email(
			user_email=form.email.data,
			user_name=form.name.data
		)
		flash(f"welcome {form.name.data}")
		return redirect(url_for("dashboard.landing"))

	return render_template(
		"auth/register.html", 
		form=form
	)


@mod_auth.route("/login", methods=['GET', 'POST'])
def login():

	form = LoginForm()

	if current_user.is_authenticated:
		mp.track(f"user_{current_user.id}", "login visit")
		return redirect(url_for('dashboard.landing'))

	if form.validate_on_submit():
		user = db_case_insensitive.get_user(email=form.email.data)
		
		if user is None or not user.check_password(form.password.data):
			flash('Invalid email or password')
			return redirect(url_for('auth.login'))

		login_user(user)
		return redirect(url_for("dashboard.landing"))

	return render_template(
		"auth/login.html", 
		form=form
	)


@mod_auth.route("/logout", methods=['GET', 'POST'])
def logout():
	logout_user()

	form = LoginForm()
	return render_template(
		"auth/login.html", 
		form=form
	)


@mod_auth.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
	user_record = db_base.get_user_record()
	mp.track(f"user_{current_user.id}", "settings visit")
	
	form = SettingsForm()

	if form.validate_on_submit():
		user_record.name = form.name.data
		user_record.time_zone= form.time_zone.data
		db.session.commit()
		flash("settings updated")
		return redirect(url_for("auth.settings"))

	return render_template(
		"auth/settings.html", 
		form=form, 
		user_record=user_record
	)




# --------------API LOGIN/LOGOUT DEMO--------------------------#

@mod_auth.route("/api-login", methods=['GET', 'POST'])
def api_login():

	form = LoginForm()

	if form.validate_on_submit():

		base_api = f"{current_app.config['BASE_URL']}/api/v1/login"
		payload = {
			"email": form.email.data,
			"password": form.password.data
		}

		r = requests.post(base_api, json=payload, timeout=30)
		if r.status_code == 401:
			return render_template("error_pages/401.html")
		access_token_data = r.json()
		logger.info(f"access_token_data; {access_token_data}")

		resp = make_response(render_template("dashboard/landing.html", form=NotesForm()))
		set_access_cookies(resp, access_token_data["access_token"])
		return resp, 200

	return render_template(
		"auth/login.html", 
		form=form
	)


@mod_auth.route("/api-logout", methods=['GET', 'POST'])
def api_logout():
	resp = make_response(render_template(
		"auth/login.html", 
		form=LoginForm())
	)
	unset_jwt_cookies(resp)
	return resp, 200

# --------------END API LOGIN/LOGOUT DEMO--------------------------#

