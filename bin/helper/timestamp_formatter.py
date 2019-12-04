from datetime import datetime
from dateutil import parser
from email import utils
import pytz

from log_config.custom_logger import logger


def get_week_number(date_value):
	dt = date_value.isocalendar()[1] - date_value.replace(day=1).isocalendar()[1] + 1
	logger.info(f"week number; {dt}")
	return dt


def current_day():
	"""
		converts day of the week in digit to string
	"""
	day_of_week = {0: "mon", 1: "tue", 2: "wed", 3: "thu", 4: "fri", 5: "sat", 6: "sun"}
	today = datetime.today().weekday()
	return day_of_week[int(today)]


def convert_db_day_to_dateutil_day(db_days_list):
	day_of_week_converter = {"mon": "MO", "tue": "TU", "wed": "WE", "thu": "TH", "fri": "FR", "sat": "SA", "sun": "SU"}
	logger.info(f"db_days_list; {db_days_list}")
	# check if its list of list
	if all(isinstance(elem, list) for elem in db_days_list):
		converted_days = [day_of_week_converter[item] for sublist in db_days_list for item in sublist]
	else: 
		converted_days = [day_of_week_converter[db_day] for db_day in db_days_list]
	logger.info(f"converted days for dateutil; {converted_days}")
	return converted_days


def get_us_timezones():
	time_zones = [tz for tz in pytz.common_timezones if "US/" in tz]
	return time_zones


def dst_converter(dst_val):
	dst_values = {1: True, 0: False, -1: False}
	if dst_val in dst_values:
		return dst_values[dst_val]
	return False


def convert_to_utc(time_to_convert, time_zone):
	utc = pytz.utc
	tz_setup = pytz.timezone(time_zone)

	# %I instead of %H to recognize %p- AM/PM
	clean_time = datetime.strptime(time_to_convert, "%m/%d/%Y %I:%M%p")
	localized_time = pytz.timezone(time_zone).localize(clean_time)
	
	# check if dst is in effect
	is_dst = dst_converter(localized_time.timetuple().tm_isdst)
	logger.info(f"is_dst; {is_dst}")

	# re-check for localized time taking dst into account
	localized_time_with_dst = tz_setup.localize(clean_time, is_dst=is_dst)
	logger.info(f"localized_time_with_dst; {localized_time_with_dst}")

	# convert to UTC
	utc_time = localized_time_with_dst.astimezone(utc)
	utc_str = utc_time.strftime ("%Y-%m-%d %H:%M:%S")
	logger.info(f"utc_str_time; {utc_str}")

	return utc_str


def convert_utc_to_localtime(utc_time, time_zone):
	localtime = pytz.utc.localize(utc_time, is_dst=None).astimezone(pytz.timezone(time_zone))
	logger.info(f"utc to local time; {localtime}")
	return localtime


def current_utc_datetime():
	d = datetime.now(tz=pytz.utc)
	logger.info(f"current utc datetime; {d}")
	return d 


def current_utc_naive_datetime():
	d = datetime.utcnow()
	logger.info(f"current utc naive datetime; {d}")
	return d


def current_utc_str_time():
	ts = datetime.now(tz=pytz.utc).strftime('%m/%d/%Y: %H:%M:%S')
	logger.info(f"current utc str time; {ts}")
	return ts


def convert_utc_str_to_datetime(str_datestamp):
	ts = parser.parse(str_datestamp)
	logger.info(f"utc str time to datetime; {ts}")
	return ts


def readable_date(datestamp):
	clean_date = datetime.strftime(datestamp, "%m/%d/%Y")
	logger.info(f"readable_date; {clean_date}")
	return clean_date


def convert_tz_for_select_field():
	"""
		SelectField in Forms requires a list of tuples.
		get_us_timezones() generates only a list of timezones.
		convert a list into a list of tuples to pass into SelectField.
	"""
	time_zones = get_us_timezones()
	tuple_tz = {}
	for tz in time_zones:
		tuple_tz[tz] = tz
	clean_tz = list(tuple_tz.items())

	return clean_tz


def convert_db_timestamp_to_readable_format(timestamp):
	"""
		convert to MM/DD/YY from the db format of YY/MM/DD - HH/MM/SS
	"""
	try:
		clean_date = datetime.strptime(str(timestamp), '%Y-%m-%d %H:%M:%S.%f').strftime('%m/%d/%Y')
	except ValueError as e:
		logger.info(f"errored timestamp; {timestamp}")
		logger.error(e)
		clean_date = None
	return clean_date


def convert_datetime_to_rfc2822(datestamp):
	datetuple = datestamp.timetuple()
	epoch = datetime.utcfromtimestamp(0)
	timestamp = (datestamp - epoch).total_seconds()
	ts = utils.formatdate(timestamp)
	logger.info(f"datetime to rfc2822; {ts}")
	return ts






