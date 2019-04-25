# ShortLinks

ShortLinks is a URL shortening service and a link management platform. Deployed on [Heroku](https://short-links.herokuapp.com).

  - Short links without authentication
  - See link statistics for registered users

Stack:
  - Django
  - JQuery(for AJAX)
  - Chartist.js(for graphics)

# Quick start:
```bash
$ pip install pipevn
$ pipenv install && pipenv shell
```
Create **config/.env** and change to you settings:
```bash
cp config/.env.template config/.env
```
Run migrate db and server:
```bash
(short-links)$ python manage.py migrate
(short-links)$ python manage.py runserver
```

# Use Docker:
```bash
$ docker-compose build
$ docker-compose run --rm web python3 manage.py migrate
$ docker-compose up
```

# Deploying on Heroku:
```bash
heroku create short_links-prod --remote prod && \
    heroku addons:create heroku-postgresql:hobby-dev --app short_links-prod && \
    heroku config:set DJANGO_SECRET=`openssl rand -base64 32` \
        DJANGO_DEBUG="True" \
        --app short_links-prod
```