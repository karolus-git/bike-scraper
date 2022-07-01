#Libraries
import requests
import re
import unidecode
from datetime import datetime
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# Modules
import browser

# Constants
from config import WAIT_TIME_S
from config import SCRAP_DICT
from config import FMT_DATETIME
#


class ScrapDefault():
    """Main Scrap class

    Stores the url and the name
    """

    def __init__(self, name, parameters):

        self.name = name
        self.url = parameters.get("url")
        self.size = parameters.get("size")
        self.WAIT_TIME = 15
    
    def make_soup(self, extra_url=None):
        """Convert url to soup

        Returns:
            bs4.BeautifulSoup: soup
        """


        url = self.url + extra_url if extra_url else self.url

        response = requests.get(url)
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')

        return soup


    def convert_price(self, price_str):
        """Convert price to float

        #TODO make that cleaner with regex ?

        Args:
            price_str (str): string with a price inside

        Returns:
            float: price
        """

        return float(unidecode.unidecode(price_str).replace("\n","").replace(" ","").replace("EUR","").replace(",", "."))


class ScrapPBS(ScrapDefault):
    """Scrapper for ProBikeShop

    Args:
        ScrapDefault (ScrapDefault): parent class
    """

    def __init__(self, name, url):
        
        super().__init__(name, url) 

        self.source = "ProBikeShop"
        

    def parse_selenium(self,):
        """Extract data with selenium

        Returns:
            dict: data parsed with selenium
        """

        return {}

    def parse_bs(self):
        """Extract data from the soup

        Returns:
            dict: data parsed with bs4
        """

        try:
            soup = self.make_soup()

            #Get the price and convert it
            price_str = soup.find('div', {'class':'productPageContentInfosTopPrices_price'})
            price = self.convert_price(price_str.string)

            available_str = soup.find('div', {'class':'productPageContentInfosTop_stock'})
            available = "en stock" in available_str.string.lower()
            
            return {
                    "comments" : None,
                    "name" : self.name,
                    "source" : self.source,
                    "size" : self.size,
                    "url" : self.url,
                    "available" : available,
                    "price" : price,
                    "datetime" : datetime.now().strftime(FMT_DATETIME)
                }

        except Exception as exce:
            print(exce)
            return {
                    "comments" : "unable to parse with bs",
                    "name" : self.name,
                    "source" : self.source,
                    "size" : self.size,
                    "url" : self.url,
                    "datetime" : datetime.now().strftime(FMT_DATETIME)
                }
            


class ScrapAT(ScrapDefault):
    """Scrapper for Alltricks

    Args:
        ScrapDefault (ScrapDefault): parent class
    """

    def __init__(self, name, url):
        super().__init__(name, url) 

        self.source = "Alltricks"

    def parse_bs(self):
        """Extract data from the soup

        Returns:
            dict: data parsed with bs4
        """

        try:
            soup = self.make_soup()
            
            #Get the price and convert it
            price_str = soup.find('p', {'class':'price'})
            price = self.convert_price(price_str.text)

            return {
                    "comments" : None,
                    "name" : self.name,
                    "source" : self.source,
                    "size" : self.size,
                    "url" : self.url,
                    "price" : price,
                    "datetime" : datetime.now().strftime(FMT_DATETIME)
                }

        except Exception as exce:
                return {
                    "comments" : "unable to parse with bs",
                    "name" : self.name,
                    "source" : self.source,
                    "size" : self.size,
                    "url" : self.url,
                    "datetime" : datetime.now().strftime(FMT_DATETIME)
                }   

    def parse_selenium(self,):
        """Extract data with selenium

        Returns:
            dict: data parsed with selenium
        """ 
        return {}

class ScrapDK(ScrapDefault):
    """Scrapper for Decathlon

    Args:
        ScrapDefault (ScrapDefault): parent class
    """
    
    def __init__(self, name, url):
        super().__init__(name, url) 

        self.source = "Decathlon"

    def parse_bs(self):
        """Extract data from the soup

        Returns:
            dict: data parsed with bs4
        """

        try:
            soup = self.make_soup()

            #Get the price and convert it
            price_str = soup.find('div', {'class':'prc__active-price'})
            price = self.convert_price(price_str.text)

            return {
                    "comments" : None,
                    "name" : self.name,
                    "source" : self.source,
                    "size" : self.size,
                    "url" : self.url,
                    "price" : price,
                    "datetime" : datetime.now().strftime(FMT_DATETIME)
                }
        except Exception as exce:
                return {
                    "comments" : "unable to parse with bs",
                    "name" : self.name,
                    "source" : self.source,
                    "size" : self.size,
                    "url" : self.url,
                    "datetime" : datetime.now().strftime(FMT_DATETIME)
                }   


    def parse_selenium(self):
        """Extract data with selenium

        Returns:
            dict: data parsed with selenium
        """

        # Load a browser
        driver = browser.run("--lang=fr", type_="firefox")

        # Go to url
        driver.get(self.url)

        #Click on reject cookies in the cookies popup
        WebDriverWait(driver, self.WAIT_TIME).until(EC.element_to_be_clickable((By.CLASS_NAME, "didomi-continue-without-agreeing"))).click()

        #Click on size dropdown
        size_dropdown = driver.find_element("xpath", "//button[contains(@class,'svelte-1cr01ag')]")
        size_dropdown.click()

        #Search your size
        size_items = size_dropdown.find_elements("xpath", "//li[contains(@class,'svelte-1cr01ag')]")

        #Loop over the sizes
        not_available = True
        for size_item in size_items:
            # Get the size and the 
            size, available_str = size_item.text.split("\n")
            
            # Your size is in the dropdown
            size_ok = size.lower() == self.size.lower()
            if size_ok:
                not_available = any([word in available_str.lower() for word in ["outofstock", "rupture"]])

        #Get the price and convert it
        price_str = driver.find_element("xpath", "//div[contains(@class,'prc__active-price')]")
        price = self.convert_price(price_str.text)

        driver.close()

        return {
                "name" : self.name,
                "source" : self.source,
                "size" : self.size,
                "url" : self.url,
                "available" : not not_available,
                "price" : price,
                "datetime" : datetime.now().strftime(FMT_DATETIME)
            }

class ScrapCRC(ScrapDefault):
    """Scrapper for ChainReactionCyles

    Args:
        ScrapDefault (ScrapDefault): parent class
    """
    
    def __init__(self, name, parameters):
        super().__init__(name, parameters) 

        self.source = "ChainReactionCycles"

    def parse_selenium(self,):
        """Extract data with selenium

        Returns:
            dict: data parsed with selenium
        """
        return {}

    def parse_bs(self):
        """Extract data from the soup

        Returns:
            dict: data parsed with bs4
        """

        try:
            soup = self.make_soup()

            #Get the price and convert it
            price_str = soup.find('span', {'class':'crcPDPPriceHidden'})
            price = self.convert_price(price_str.text)

            return {
                    "comments" : None,
                    "name" : self.name,
                    "source" : self.source,
                    "size" : self.size,
                    "url" : self.url,
                    "price" : price,
                    "datetime" : datetime.now().strftime(FMT_DATETIME)
                }
        except Exception as exce:
                return {
                    "comments" : "unable to parse with bs",
                    "name" : self.name,
                    "source" : self.source,
                    "size" : self.size,
                    "url" : self.url,
                    "datetime" : datetime.now().strftime(FMT_DATETIME)
                }   

class ScrapBMX(ScrapDefault):
    """Scrapper for BMXAvenue

    Args:
        ScrapDefault (ScrapDefault): parent class
    """
    
    def __init__(self, name, url):
        super().__init__(name, url) 

        self.source = "BMXAvenue"

    def parse_bs(self):
        """Extract data from the soup

        Returns:
            dict: data parsed with bs4
        """
        
        try:
            soup = self.make_soup()
            
            #Get the price and convert it
            price_str = soup.find('span', {'class':'price-cur'})
            price = self.convert_price(price_str.text)

            return {
                "comments" : None,
                "name" : self.name,
                "source" : self.source,
                "url" : self.url,
                "price" : price,
                "datetime" : datetime.now().strftime("%Y-%m-%d %H:%M")
            }
        except Exception as exce:
                return {
                    "comments" : "unable to parse with bs",
                    "name" : self.name,
                    "source" : self.source,
                    "size" : self.size,
                    "url" : self.url,
                    "datetime" : datetime.now().strftime(FMT_DATETIME)
                }   

    def parse_selenium(self):
        """Extract data with selenium

        Returns:
            dict: data parsed with selenium
        """

        # Load a browser
        driver = browser.run("--lang=fr", type_="firefox")

        # Go to url
        driver.get(self.url)

        # Click on reject cookies in the cookies popup
        WebDriverWait(driver, self.WAIT_TIME).until(EC.element_to_be_clickable((By.CLASS_NAME, "wz-rgpd__wrapper__btn__deny"))).click()

        # Select your size in the dropdown
        select_dropdown = Select(driver.find_element("xpath", "//select[contains(@class,'groupVariation1')]"))
        select_dropdown.select_by_visible_text(self.size)

        #Get the price and convert it
        price_str = driver.find_element("xpath", "//span[contains(@class,'price-cur')]")
        price = self.convert_price(price_str.text)

        # Get the stock
        stock_str = driver.find_element("xpath", "//p[contains(@id,'prod-stock')]")
        not_available  = "sur commande" in stock_str.text

        driver.close()

        return {
                "name" : self.name,
                "source" : self.source,
                "url" : self.url,
                "price" : price,
                "available" : not not_available,
                "datetime" : datetime.now().strftime("%Y-%m-%d %H:%M")
            }


class ScrapCYC(ScrapDefault):
    """Scrapper for Cyclable

    Args:
        ScrapDefault (ScrapDefault): parent class
    """
    
    def __init__(self, name, url):
        super().__init__(name, url) 

        self.source = "Cyclable"

    def parse_bs(self):
        """Extract data from the soup

        Returns:
            dict: data parsed with bs4
        """
        
        try:
            extra_url = f"#/taille_du_cadre-{self.size}" if self.size else None
            soup = self.make_soup(extra_url=extra_url)

            #Get the price and convert it
            price_str = soup.find('span', {'id':'our_price_display'})
            price = self.convert_price(price_str.string)

            #TODO get the stock from extra_url

            return {
                "comments" : None,
                "name" : self.name,
                "source" : self.source,
                "url" : self.url,
                "price" : price,
                "datetime" : datetime.now().strftime("%Y-%m-%d %H:%M")
            }
        except Exception as exce:
                return {
                    "comments" : "unable to parse with bs",
                    "name" : self.name,
                    "source" : self.source,
                    "size" : self.size,
                    "url" : self.url,
                    "datetime" : datetime.now().strftime(FMT_DATETIME)
                }   

    def parse_selenium(self):
        """Extract data with selenium

        Returns:
            dict: data parsed with selenium
        """
        return {}


class ScrapCV(ScrapDefault):
    """Scrapper for CultureVelo

    Args:
        ScrapDefault (ScrapDefault): parent class
    """
    
    def __init__(self, name, url):
        super().__init__(name, url) 

        self.source = "CultureVelo"

    def parse_bs(self):
        """Extract data from the soup

        Returns:
            dict: data parsed with bs4
        """
        
        try:
            soup = self.make_soup()

            #Get the price and convert it
            price_str = soup.find('span', {'class':'carac-prix'})
            price = self.convert_price(price_str.string)

            #TODO get the stock from extra_url

            return {
                "comments" : None,
                "name" : self.name,
                "source" : self.source,
                "url" : self.url,
                "price" : price,
                "datetime" : datetime.now().strftime("%Y-%m-%d %H:%M")
            }
        
        except Exception as exce:
                return {
                    "comments" : "unable to parse with bs",
                    "name" : self.name,
                    "source" : self.source,
                    "size" : self.size,
                    "url" : self.url,
                    "datetime" : datetime.now().strftime(FMT_DATETIME)
                }   
    def parse_selenium(self):
        """Extract data with selenium

        Returns:
            dict: data parsed with selenium
        """
        return {}


if __name__ == "__main__":

    from config import SCRAP_DICT

    name = "Orbea terra h40"
    parameters = SCRAP_DICT.get(name)
    scrap = ScrapCV(name, parameters)
