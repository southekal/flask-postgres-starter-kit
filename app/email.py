import os

from jinja2 import Environment, PackageLoader
import requests

from log_config.custom_logger import logger


class MailGunEmailService:

	def __init__(self):
		self.mailgun_domain = os.environ.get('MAILGUN_DOMAIN', None)
		self.mailgun_api = os.environ.get('MAILGUN_API', None)
		self.timeout = 20

	def _base_email_logger(self, from_address, to_address, subject, request_data):

		logger.info('attempting to send email from {}'.format(from_address))
		logger.info('attempting to send email to {}'.format(to_address))
		logger.info('attempting to send email with subject {}'.format(subject))
		logger.info('email status {}'.format(request_data.status_code))
		logger.info('email response text {}'.format(request_data.text))


	def base_email(self, from_address, to_address, bcc, subject, html):
		
		r = requests.post(
			f"https://api.mailgun.net/v3/{self.mailgun_domain}/messages",
			auth=("api", self.mailgun_api),
			data={
					"from": from_address,
					"to": to_address, 
					"bcc": bcc,
					"subject": subject,
					"html": html
				}, 
			timeout=self.timeout
		)

		r.raise_for_status()
		self._base_email_logger(
			from_address=from_address, 
			to_address=to_address, 
			subject=subject, 
			request_data=r
		)
		
		return r

	def base_email_with_delivery_time(self, from_address, to_address, bcc, subject, html, delivery_time):
		
		r = requests.post(
			f"https://api.mailgun.net/v3/{self.mailgun_domain}/messages",
			auth=("api", self.mailgun_api),
			data={
					"from": from_address,
					"to": to_address, 
					"bcc": bcc,
					"subject": subject,
					"html": html, 
					"o:deliverytime": delivery_time
				}, 
			timeout=self.timeout
		)

		r.raise_for_status()
		self._base_email_logger(
			from_address=from_address, 
			to_address=to_address, 
			subject=subject, 
			request_data=r
		)
		
		return r


	def send_welcome_email(self, user_email, user_name):
		env = Environment(
			loader=PackageLoader('app', 'templates')
		)
		welcome = env.get_template("email/welcome.html")

		from_address = "hello@example.com"
		to_address = user_email
		bcc = os.environ.get('SEND_EMAIL_ACCOUNT', None)
		subject = "Welcome!"
		html = welcome.render(user_name=user_name)

		email_action = self.base_email(
				from_address=from_address,
				to_address=to_address,
				bcc=bcc,
				subject=subject,
				html=html
			)
