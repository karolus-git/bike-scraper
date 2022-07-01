FROM python:3.8.13-slim

# Creation of the working directory called scrapper
WORKDIR scraper

# Update debian
RUN apt update

# Installation of firefox (for selenium and geckodriver)
RUN apt install -y firefox-esr

# Update pip
RUN pip install --upgrade pip

# Install required packages
RUN pip install webdrivermanager geckodriver-autoinstaller pymongo unidecode selenium requests bs4

RUN webdrivermanager firefox --linkpath /usr/local/bin

# Build a directory for the dbs
RUN mkdir data

# Copy of the required source files in the working folder
COPY src/browser.py .
COPY src/config.py .
COPY src/mongo_manager.py .
COPY src/scrap.py .
COPY src/scrapers.py .

# Run the scrapper with its infinite while loop
CMD [ "python", "scrap.py"]
