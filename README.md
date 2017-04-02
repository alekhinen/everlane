# Everlane Sample App
Will fill this out later.

# Installing the project
- Ensure that `Python 2.7.x` is installed on your machine.
- Ensure that you have `pip` installed.
- Clone this repo.
- `cd` into the repo.
- run `pip install -r requirements.txt`.
- Run `python manage.py migrate` from the top level directory.

# For Database Management
- Run `python manage.py createsuperuser` to create an administrator account.
- Run `python manage.py runserver` and head to `http://127.0.0.1:8000/admin` (or wherever the server is running).
- Log in with the newly created admin account and start adding users, shopping carts, and products.

# API Usage
- `python manage.py add_to_cart <user_id> <product_id> <product_quantity>`
- `python manage.py remove_from_cart <user_id> <product_id>`
- `python manage.py purchase <user_id>`
- `python manage.py view_purchase_history <user_id>`
