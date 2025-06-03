IMPORTANT:
In order for the email to work you need to run:
export EMAIL_HOST_USER='siebrandkokke64@gmail.com'
export EMAIL_HOST_PASSWORD='lbcsqxggicdjafma'
Prior to doing python manage.py runserver.
If you get 403 Forbidden, log into the Django admin and ensure that your user is a member of the ‘Journalist’ group, and that the group has all required permissions.
Try this in django shell:
from users.signals import setup_groups_permissions
setup_groups_permissions(None)

The tweets do not actually post to an account because the free API twitter provides does not allow for it.
It is functional within the code but without paying it wont actually post. 

FEATURES:
- Role-based system: Reader, Journalist, Editor
- Article and Newsletter management (create, edit, approve, delete)
- Subscriptions to journalists and publishers
- Newsletters sent via email to subscribers
- RESTful API endpoints (see code)
- MariaDB database integration

Clone and Install Dependancies
    "```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt"

MARIADB SETUP:
CREATE USER 'siebrand'@'localhost' IDENTIFIED BY 'news_password123';
CREATE DATABASE news_project;
GRANT ALL PRIVILEGES ON news_project.* TO 'siebrand'@'localhost';
FLUSH PRIVILEGES;

Running the Application with Docker:

1. Build and start the containers:
   ```bash
   docker-compose up --build
   docker-compose exec web python manage.py migrate

Sphinx Documentation:

Viewing Documentation:

Sphinx-generated documentation is included in the `/docs` directory.

- To view the documentation, open:  
  `docs/_build/html/index.html`  
  in your web browser.

- To rebuild the docs (optional, requires Sphinx):
   ```bash
   cd docs
   make html

run pip freeze > requirements.txt