# Bike scraper

## Description

Finding a bike is complicated... This project helps you by :

* track the prices of your favorites bikes
* storing them in a mongo database

For every website, you will have to create your own scraper. Each scraper has two main methods :

* `parse_bs` : uses `BeautifulSoup` to parse items. It's the simplest one
* `parse_selenium` : uses `selenium` to parse items. It's more complicated but also more interesting ! For example, you have the possibility to navigate on your web pages and click on dropdowns to see if your frame size is available

## Installation and initialization

### Installation

To install this project, you only need to have Docker installed and run the build command :

```docker-compose build```

### Initialization

Please look at the `config.py` file and modify the mongo parameters.

To add your favorite bike :

* Add it to the `SCRAP_DICT` dictionary, with a name, a url, and a size if you want to.
* Create a new scraper class in the `scrapers.py` file and adjust it to your needs.
* Don't forget to complete the `build_scrapers` function ;)


## Run the projet

The project runs two containers : 

* the mongo server
* the web scraper

Launch everything with the following command :

```docker-compose up```

Enjoy and be patient !

> **_INFO:_** You can use DB Compass to analyze your database.


## Todos

A lot of things !

* add a `dash` dashboard
* handle the cookie popups that block the navigation with `selenium`
* send notification if your frame size is available or if the price is decreasing