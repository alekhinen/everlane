# Everlane Sample App
This is a working sample project that solves the specifications from Everlane's take home project.
The decisions for using Django were twofold: familiarity of use and ease of rapidly building and testing database models.

SQLite3 was used because of ease of installation and use. Considering that this project is expected to run on
an ambiguous set of computers, the decision was made to pick a lightweight DB. If this were a production-grade
application, PostgreSQL or MySQL would have been used because these implementations can handle much larger datasets.
Either way, with Django it's relatively painless to port over databases and implement raw SQL statements if needed.

Several API endpoints and database models were created. This could be worked on further, but I made the decision
to stop work after the main features were implemented.

## Installing the project
- Ensure that `Python 2.7.x` is installed on your machine.
- Ensure that you have `pip` installed.
- Clone this repo.
- `cd` into the repo.
- run `pip install -r requirements.txt`.
- Run `python manage.py migrate` from the top level directory.

## To Run Tests
- run `python manage.py test`

## For Database Management
- Run `python manage.py createsuperuser` to create an administrator account.
- Run `python manage.py runserver` and head to `http://127.0.0.1:8000/admin` (or wherever the server is running).
- Log in with the newly created admin account and start adding users, shopping carts, and products.

## API Usage
- `python manage.py add_to_cart <user_id> <product_id> <product_quantity>`
- `python manage.py remove_from_cart <user_id> <product_id>`
- `python manage.py purchase <user_id>`
- `python manage.py view_purchase_history <user_id>`
