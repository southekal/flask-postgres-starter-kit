from flask_login import current_user

from app.models import (
	BaseUser
)


# ================== USER ================== #

def get_user_record():
	user_record = BaseUser.query.filter_by(id=current_user.id).first()
	return user_record


def get_user_record_by_id(user_id):
	user_record = BaseUser.query.filter_by(id=user_id).first()
	return user_record


def get_user_timezone():
	user_record = BaseUser.query.filter_by(id=current_user.id).first()
	user_timezone = user_record.time_zone
	return user_timezone

# ================== END USER ================== #
