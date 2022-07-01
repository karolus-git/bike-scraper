
import scrapers
import time
from datetime import datetime


import mongo_manager

from config import WAIT_TIME_S
from config import SCRAP_DICT
from config import PARSER

# Load the collection from the mongoDB
mongo_collection = mongo_manager.init_db()

def scrap_in_loop(scrap_list,):
    """Scrap data from a website and store it in a database
    """
    
    #Infinite loop
    while True:
        # For object, we launch the scraping process 
        for scrap in scrap_list:
            
            # Launch the selenium scraper
            if PARSER == "selenium":
                result = scrap.parse_selenium()
            # Launch the bs4 scraper
            elif PARSER == "bs":
                result = scrap.parse_bs()
            else:
                result = {}

            # If we got data, we update the object 
            if result:
                mongo_manager.update_db(mongo_collection, result) 

        print(f"database updated at {datetime.now()}")

        # Wait some time
        time.sleep(WAIT_TIME_S)

def build_scrapers():
    """Creation of the scrapers according to keyword found in their urls

    Returns:
        tuple: tuple of scrapers
    """
    scrap_list = []

    for name, parameters in SCRAP_DICT.items():

        #Get the url to scrap
        url = parameters.get("url")

        #Get the correct scraper and push it into a list
        if "probikeshop" in url:
            scrap_list.append(scrapers.ScrapPBS(name, parameters))
        elif "alltricks" in url:
            scrap_list.append(scrapers.ScrapAT(name, parameters))
        elif "chainreaction" in url:
            scrap_list.append(scrapers.ScrapCRC(name, parameters))
        elif "decathlon" in url:
            scrap_list.append(scrapers.ScrapDK(name, parameters))
        elif "bmx" in url:
            scrap_list.append(scrapers.ScrapBMX(name, parameters))
        elif "cyclable" in url:
            scrap_list.append(scrapers.ScrapCYC(name, parameters))

    return scrap_list

if __name__ == "__main__":
    
    
    scrap_list = build_scrapers()
    scrap_in_loop(scrap_list)