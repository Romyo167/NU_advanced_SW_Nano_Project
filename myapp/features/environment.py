# d:\Term-4\Advanced sw\Nan-Project-Phase-1\NU_advanced_SW_Nano_Project\your_app\features\environment.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
# Or use FirefoxDriverManager, EdgeChromiumDriverManager etc.

def before_all(context):
    # Setup WebDriver using webdriver-manager
    options = webdriver.ChromeOptions()
    # Add options like --headless if you don't want the browser UI to pop up
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu') # Often needed for headless
    service = ChromeService(executable_path=ChromeDriverManager().install())
    context.browser = webdriver.Chrome(service=service, options=options)
    context.browser.implicitly_wait(3) # Optional implicit wait

def after_all(context):
    context.browser.quit()

# You can also add before_feature, after_feature, before_scenario, after_scenario hooks
