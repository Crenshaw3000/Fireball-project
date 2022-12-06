# Fireball Finder <br />
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/Crenshaw3000/Fireball-project)
![GitHub all releases](https://img.shields.io/github/downloads/Crenshaw3000/Fireball-project/total)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Crenshaw3000/Fireball-project)
![GitHub issues](https://img.shields.io/github/issues/Crenshaw3000/Fireball-project)
![GitHub contributors](https://img.shields.io/github/contributors/Crenshaw3000/Fireball-project)
![GitHub Repo stars](https://img.shields.io/github/stars/Crenshaw3000/Fireball-project?style=social)

Fireball Finder is a full stack web app that allows users view NASA's fireball and bolide events and save an event details to their favorites. The user can also
interact with the linear regression supervised learning model, a machine learning model, to see predictions of fireball and bolide events per year. 

The web app can be visited [here](http://fireballfinder.com/)

![Homepage](/static/images/homepage.gif "Homepage") <br />


## Contents
* [Technologies](#technologies)
* [API](#api)
* [Features] (#features)
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
