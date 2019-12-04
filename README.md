## flask-postgres-starter-kit


### Info

- flask-postgres starter kit
- includes helpers for:
  - email using Mailgun
  - file uploads/deletes to AWS S3 bucket
  - tracking using Mixpanel


### Web Application

- create `.env` with environment variables required (example `.env.example`)

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ source .env
$ python app.py
```

- access `http://localhost:5000`


### Database Setup

- [Postgresql Installation](https://www.postgresql.org/download/)
-  Login as default `postgres` user

#### Linux

```
sudo -u postgres psql postgres
```

- Create database, user with password

```
CREATE DATABASE exdb;
CREATE USER flask_user WITH ENCRYPTED PASSWORD '<pw>';
GRANT ALL PRIVILEGES ON DATABASE exdb TO exuser;
```

- Login to postgresql shell

```
sudo -u postgres psql exdb
```

#### Mac

- Download [postgres MacOS client](https://postgresapp.com/)

```
createdb exdb
psql exdb
createuser exuser
```


### Postgres Basics

- \l (list all databases)
- \dt (view tables)
- \q (quit)
- \x pretty view


### Flask DB Helpers

- flask db migrate
- flask db upgrade
- flask db --help


### Heroku 

- heroku pg:psql



