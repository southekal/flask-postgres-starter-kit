import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import datetime as dt
import shutil
import tempfile
import uuid

from icalendar import (
	Calendar,
	Event
)
import pytz

from app.email import MailGunEmailService
from log_config.custom_logger import logger


def create_event(title, description, event_end_timedelta, reminder_date, reminder_time, user_email, user_timezone):
	
	uid = uuid.uuid4()
	time_to_convert = f"{reminder_date} {reminder_time}"
	# %I instead of %H to recognize %p- AM/PM
	clean_time = dt.datetime.strptime(time_to_convert, "%m/%d/%Y %I:%M%p")
	local_date_time_obj = pytz.timezone(user_timezone).localize(clean_time)
	end_date_time_obj = local_date_time_obj + dt.timedelta(minutes= event_end_timedelta)

	logger.info(f"creating ical with start time {local_date_time_obj}")
	logger.info(f"creating ical with end time {end_date_time_obj}")

	cal = Calendar()
	cal.add('prodid', '-//nindio product//mxm.dk//')
	cal.add('version', '2.0')
	
	event = Event()
	event.add('summary', title)
	event.add('dtstart', local_date_time_obj)
	event.add('dtend', end_date_time_obj)
	event.add('dtstamp', dt.datetime.now(tz=pytz.utc))
	event.add('attendee', user_email)
	event.add('organizer', "calendar+noreply@nindio.com")
	event.add('status', "confirmed")
	event.add('category', "Event")
	event.add('description', description)	
	event['uid'] = uuid.uuid4()
	event.add('priority', 5)

	cal.add_component(event)
	return cal


def email_calendar_event(cal_obj, title, description, user_email):

	uid = uuid.uuid4()
	temp_dir = tempfile.mkdtemp(prefix='nindio_calendar_event_')
	cwf = f"{temp_dir}/example_{uid}.ics"
	logger.info(f"temp calendar file location; {cwf}")

	with open(cwf, "wb") as f:
		f.write(cal_obj.to_ical())

	m = MailGunEmailService()
	m.send_calendar_reminder(
		user_email=user_email, 
		title=title, 
		description=description,
		temp_calendar_file=cwf
	)

	shutil.rmtree(temp_dir)
	logger.info(f"deleted temp calendar file location; {cwf}")
