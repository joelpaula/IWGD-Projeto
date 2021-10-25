# Web Interfaces for Data Management - Project

> ISCTE-IUL | Data Science Bsc | Ciência de dados (PL)
> 
> Teacher: Jorge Louçã
> 
> Year: 2021 | 5th semester
> 
> Authors: Catarina Castanheira | João Martins | Joel Paula | (CD1PL)

## Whats is it?

A Python Django website, that handles music collections and reviews.

## How to run

 1. Clone the repo.

 1. Create your environment:
    
    `python -m venv env`
 
 1. Install/upgrade pip in the virtual environment:
    
    `python -m pip install --upgrade pip`

 1. Install Django in the virtual environment:
    
    `python -m pip install django`

 1. Install the needed requirements:
    
    `pip install -r requirements.txt`

 1. Go into the project's folder (`music_website`) and make sure you have the database ready:
    
    `python manage.py migrate`

 1. Still on the project's folder (`music_website`) run the server:
    
    `python manage.py runserver`

 1. Before you begin, you might wan't to create a super user, because they are considered "staff" and they can create and manage "staff picks" that are displayed prominently on the home page. You will be prompted for a password (don't forget it):
 
    `python manage.py createsuperuser --username=superfun  --email=superfun@example.com`

 1. Now open your browser at http://127.0.0.1:8000/
