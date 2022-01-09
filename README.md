# Cleo Conversations

This project is for the Cleo Hackathon 2022-01 project

## Getting Setup

In order to run the backend API application
you'll need to have Python installed. I built
this with Python 3.10.1, which is the latest version.

I would recommend installing this with the
`pyenv` tool. You might need to `brew upgrad pyenv`
to get the latest version which includes 
information to get Python version 3.10.1.

```console
$ git clone <this repository> to a directory
$ cd <repository directory>
$ pyenv install 3.10.1
$ python -m venv .venv
$ source .venv/bin/activate
(.venv) $ pip install --upgrade pip
(.venv) $ pip install -r requirements.txt
```

## Loading data

There's a script in `backend/bin` called `load_data.py` that will 
populate the database with some bogus, but possibly useful, 
initial data. To run this script the `backend/db` directory should
be empty as this is where the script will create the database.
Run this script with these steps:

```console
$ cd <repository directory>
$ source .venv/bin/activate
$ (.venv) python backend/bin/load_data.py
```

This will create the SQLite database, which you can open and 
view with most database tools.

## Running The backend

To run the backend follow these steps:

```console
$ cd <repository directory>
$ source .venv/bin/activate
(.venv) $ uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

The `source .venv/bin/activate` step is only necessary
if you're not currently in a Python virtual environment.

To access the OpenAPI Documentation navigate to http://localhost:8000/docs

### Database Backup

The database is stored in `backend/db/cleo_forum.sqlite` and the repo version has data
in it so you can some some of how the OpenAPI interface interacts.

There is also a backup of the database file in `backend/db/backup` which you can just copy
to the above location should you want to start over.