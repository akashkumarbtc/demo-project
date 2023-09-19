# linkintime-be
Linkintime Virtual Assistant Chatbot

## Prerequisites

1. Python 3.8+
   
## Building

To build the project, do the following

```sh
python -m venv venv
```

## Running

#### Using venv

To open and activate the virtual environment in windows

```sh
.\venv\Scripts\activate
```
To open and activate the virtual environment in linux

```sh
source venv/bin/activate
```

To create database migration files
```sh
python manage.py makemigrations
```
To create tables in database
```sh
python manage.py migrate
```
To create document types like Context, Tags, Anvwers, etc
```sh
python manage.py create_db
```
To create user groups
```sh
python manage.py create_groups
```
To create super user 
```sh
python manage.py createsuperuser
```
To run the server
```sh
python manage.py runserver
```


