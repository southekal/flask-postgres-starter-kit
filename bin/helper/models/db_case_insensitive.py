from flask_login import current_user
from sqlalchemy import func

from app.models import (
	BaseUser
)


# ================== USER ================== #

def get_user(email):
	user_record = BaseUser.query.filter(func.lower(BaseUser.email) == func.lower(email)).first()
	return user_record


def get_user_meeting_record_by_title(title):
	meeting_title_record = Meeting.query.filter_by(user_id=current_user.id).filter(func.lower(Meeting.title) == func.lower(title)).first()
	return meeting_title_record

# ================== END USER ================== #
