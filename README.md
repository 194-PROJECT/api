# Item Scheduling - Python

This involves everything you need to build endpoints for the item scheduling application using Flask, SQLAlchemy, and Pydantic.

## Creating a project

Clone this repository then use the following commands to prepare the dependencies

```bash
cd path-to-project/api

# create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\Activate`

# install dependencies
pip install .requirements
```

## Project Structure

Here is the project structure:

```
.
├── /core/
│   ├── . . .
│   └── /scripts
├── /database/
│   ├── /factory
│   ├── /model
│   ├── /postgres
│   └── /scripts
├── /src/
│   ├── /controller
│   ├── /dto
│   ├── /enum
│   ├── /handler
│   ├── /middleware
│   └── /repository
├── /venv
├── .requirements
├── app.py
├── README.md
├── schema.py
├── scripts.py
└── seed.py
```

#### Environment variables

Create a `.env` file with the following content:

> Make sure to replace the values with the actual values for your database

```
ENCRYPTION_KEY="gwbI7/iLikatYxm+cvYwfpC35dvdCUeSYJA0/sB7dxQ=" # THIS IS JUST A DUMMY VALUE
ALGORITHM="aes-256-cbc"

POSTGRESQL_HOST=localhost
POSTGRESQL_PORT=5432
POSTGRESQL_DATABASE=item_scheduling
POSTGRESQL_USER=postgres
POSTGRESQL_PASSWORD=password

SMTP_SERVER_ADDRESS=smtp.gmail.com
SMTP_SERVER_PORT=587
SMTP_SERVER_EMAIL=your_preferred_mail@gmail.com
SMTP_SERVER_PASSWORD="YOUR_APP_PASSWORD"

# THIS SHOULD BE SET TO THE URL OF THE WEBAPP
WEBAPP_URL="http://localhost:5173"
```

> Note: The `SMTP_SERVER_PASSWORD` should be an app password generated from your email provider. For Gmail, you can find instructions [here](myaccount.google.com/apppasswords).

#### Schema and seeding

To create the database schema and seed the database, run the following commands:

> Be sure to have postgres running on your machine and the database credentials are correct

```bash
# create the database schema
python schema.py postgres

# seed the database
python seed.py postgres
```

This will create the necessary tables and seed the database with some initial data. Table definitions can be found in the `database/model` directory. Add more tables as needed.

## Developing

Once you've created a project and installed dependencies, start the development server:

```bash
python app.py
```

## Building

To create a production version of your app, ensure all dependencies are listed in `requirements.txt` and use a WSGI server like Gunicorn:

```bash
pip freeze > requirements.txt
gunicorn app.main:app
```

> To deploy your app, you may need to configure your server and database settings accordingly.
