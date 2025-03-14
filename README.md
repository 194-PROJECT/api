# Item Scheduling - Python

This involves everything you need to build endpoints for the item scheduling application using Flask, SQLAlchemy, and Pydantic.

## Creating a project

Clone this repository then use the following commands to prepare the dependencies

```bash
cd path-to-project

# create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\Activate`

# install dependencies
pip install requirements.txt
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

Create a `.env` file with the following content

```
ENCRYPTION_KEY="gwbI7/iLikatYxm+cvYwfpC35dvdCUeSYJA0/sB7dxQ=" # THIS IS JUST A DUMMY VALUE
ALGORITHM="aes-256-cbc"

POSTGRESQL_HOST=localhost
POSTGRESQL_PORT=5432
POSTGRESQL_DATABASE=item_scheduling
POSTGRESQL_USER=postgres
POSTGRESQL_PASSWORD=password
```

> ALL OF THESE ARE JUST PLACEHOLDER VALUES

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
