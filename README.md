# Fireball Finder <br />
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/Crenshaw3000/Fireball-project)
![GitHub all releases](https://img.shields.io/github/downloads/Crenshaw3000/Fireball-project/total)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Crenshaw3000/Fireball-project)
![GitHub issues](https://img.shields.io/github/issues/Crenshaw3000/Fireball-project)
![GitHub contributors](https://img.shields.io/github/contributors/Crenshaw3000/Fireball-project)
![GitHub Repo stars](https://img.shields.io/github/stars/Crenshaw3000/Fireball-project?style=social)

Fireball Finder is a full stack web app that allows users view NASA's fireball and bolide events and save an event details to their favorites. The user can also
interact with the linear regression supervised learning model, a machine learning model, to see predictions of fireball and bolide events per year. 

Youtube video of the web app  [Fireball Locator App Demo](https://youtu.be/XJpw-U-e_YE?si=BjbB7keiN9bPmtFd)

![Homepage](/static/images/homepage.gif "Homepage") <br />


## Contents
* [Technologies](#technologies)
* [API](#api)
* [Features](#features)
* [Installation](#installation) <br />


## <a name="technologies"></a> Technologies
* Python 3.9
* Flask
* PostgresSQL
* SQL Alchemy
* Jinja
* JavaScript
* Bootstrap
* HTML/CSS
* Anaconda
* Numpy
* Pandas
* Jupyter Notebook
* Matplotlib
* Scikit learn <br />


## <a name="api"></a> APIs
* Cloudinary
* Google Maps <br />


## <a name="features"></a>Features

This is a **Flask web application** that tracks and visualizes meteor fireball data, allowing users to explore fireball locations, save favorites, and manage their profiles.

## Core Functionality

- **Fireball Tracking**: Displays meteor fireball locations on interactive maps using Google Maps API
- **User Accounts**: Registration, login, password recovery with security questions
- **Save System**: Users can save/unsave fireball locations to their personal collection
- **Profile Management**: Photo uploads via Cloudinary, update personal information

## Key Features

- **Interactive Maps**: View fireballs on Google Maps with coordinate data
- **Data Visualization**: Dedicated page for fireball data analysis
- **Prediction Model**: Page for fireball prediction functionality
- **Secure Authentication**: Password validation, security questions for recovery
- **Photo Management**: Upload/delete profile pictures stored in cloud

## Technical Stack

- **Backend**: Flask with SQLAlchemy Object-Relational Mapping
- **Database**: PostgreSQL with three main tables (Users, Locators, Saved)
- **Frontend**: HTML templates with Jinja2, Google Maps integration
- **Cloud Services**: Cloudinary for image storage
- **Data**: JSON-based fireball coordinate dataset

## Database Design

- **Users**: Account info, security questions, profile photos
- **Locators**: Fireball coordinates (lat/lng), dates, energy levels
- **Saved**: Many-to-many relationship linking users to their saved fireballs

The app combines astronomical data with social features, letting space enthusiasts track and collect meteor fireball events in an interactive, user-friendly interface.





## <a name="installation"></a> Installation
#### To run Fireball Finder on your computer

 Clone or fork the repository:
 ```
 $ git clone https://github.com/Crenshaw3000/Fireball-project.git
 ```
Create a virtual environment inside of your fireball finder directory:
```
$ virtualenv env
$ source env/bin/activate
```

Install dependencies:
```
$ pip3 install -r requirements.txt
```

Sign up for a Google Maps API and Cloudinary API key 
and save to a file called secrets.sh with the following format:
```
export GOOGLE_KEY="YOUR_KEY_HERE"
export CLOUDINARY_KEY="YOUR_KEY_HERE"
export CLOUDINARY_SECRET="YOUR_KEY_HERE"
```

Activate the keys:
```
$ source secrets.sh
```

To create the SQL database models run:
```
$ createdb saved
$ python3 model.py
$ python3 seed_database.py
```

Run the web app:
```
$ python3 server.py
```

To view app in web browser, insert into the browser:
```
 localhost:5000
 ```
