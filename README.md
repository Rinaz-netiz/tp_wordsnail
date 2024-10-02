# Game wordsnail
Getting started
1. Clone the repo to your local machine
2. Create venv python -m venv env and activate it
3. Create .env in project and fill it

SECRET_KEY=

    Install requirements.txt pip install -r requirements.txt
    Create migrations python manage.py makemigrations
    Apply migrations python manage.py migrate
    Create super user python manage.py createsuperuser
    Run command python manage.py fill_navbar
    Run test python manage.py test
    Create directory cache and log/application.log
    Run the app python python manage.py runserver

! IMPORTANT: Never push your changes directly to master branch