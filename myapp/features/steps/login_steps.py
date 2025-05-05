# d:\Term-4\Advanced sw\Nan-Project-Phase-1\NU_advanced_SW_Nano_Project\your_app\features\steps\login_steps.py
from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.urls import reverse
import time # Sometimes needed for waits, but prefer explicit waits

# Note: The 'context' object is passed around by behave.
# 'context.browser' is typically initialized in environment.py (see next step)
# 'context.get_url()' is provided by django-behave to get absolute URLs

@given('I am on the login page')
def step_impl(context):
    # Assuming you have a URL name 'login' in your urls.py
    login_url = context.get_url()
    context.browser.get(login_url)

@when('I fill in "{field_name}" with "{value}"')
def step_impl(context, field_name, value):
    # Assumes input fields have 'name' attributes matching field_name
    element = context.browser.find_element(By.ID, field_name)
    element.send_keys(value)

@when('I press "{button_text}"')
def step_impl(context, button_text):
    # Find button by text or a more robust selector (like ID or CSS selector)
    # This example finds a submit button within a form
    # Adjust selector as needed!
    button = context.browser.find_element(By.XPATH,button_text)
    button.click()


@then('I should see on "{message_id}" the message "{text}"') # Corrected decorator
def step_impl(context, message_id, text):
    # Wait for the text to be present in the body
    # The wait condition returns the WebElement once the condition is met
    element = WebDriverWait(context.browser, 10).until(
        # Wait for the EXPECTED text from the feature file
        EC.text_to_be_present_in_element((By.ID, message_id), text)
    )