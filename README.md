# Simple Lesson Booking site

This is a simple Python Flask web application for booking sabre lessons, styled using TailwindCSS and with a few additional packages to help make life easier for future upgrades, such as flask-migrate.

0. Make a new directory and initialise venv: 

```
python3 -m venv .venv
source .venv/bin/activate
which python
```

1. Clone the repository using git clone.
2. pip install -r requirements.txt
3. Create a .env file in the project root with the key:pair APP_SECRET_KEY = "<your-own-secret-key>".

- You can generate your secret key by running the following command in the terminal:
- ```echo APP_SECRET_KEY=\"`python -c 'import secrets; print(secrets.token_hex())'`\" >> .env```

4. Initialise the db migration: flask db migrate
5. Upgrade the database: flask db upgrade
6. Install Tailwindcss
7. Compile Tailwindcss file: npx tailwindcss -i ./app/static/src/style.css -o ./app/static/css/main.css
8. Run program: python main.py

For the local version, the code will automatically make the first user you register into an admin. Then you can administer the database via flask-admin by browsing to the /admin/ route in your browser.
