from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

import geckodriver_autoinstaller

geckodriver_autoinstaller.install()

def run(*args, type_="firefox"):
    """Get a browser with its options

    Args:
        type_ (str, optional): firefox or chrome. Defaults to "firefox".

    Returns:
        webdriver: the browser
    """

    # Choose options according to the browser of choice
    options = ChromeOptions() if type_=="chrome" else FirefoxOptions()
    # Add args to options
    for arg in args:
        options.add_argument(arg)

    #Return the correct webdriver
    if type_ == "firefox":
        return  webdriver.Firefox(options=options)

    elif type_ == "chrome":
        return webdriver.Chrome(chrome_options=opts)

def wait(browser, timeout=10):
    WebDriverWait(browser, timeout=timeout)

