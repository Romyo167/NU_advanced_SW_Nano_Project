from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.urls import reverse
from django.contrib.auth.models import User

use_step_matcher("parse")

@given('I am on the signup page')
def step_impl(context):
    # Make sure you have a URL pattern named 'signup' in your urls.py
    login_url = context.get_url()
    context.browser.get(login_url)
    button = context.browser.find_element(By.XPATH, '//*[@id="login-section"]/p/button')
    button.click()


@when('I press the signup button')
def step_impl(context):
    # Find the signup button by its ID (adjust 'signup-button-id' if needed)
    # You might need to change By.ID to By.XPATH or By.CSS_SELECTOR if it's not an ID
    button_id = '//*[@id="signup-section"]/button' # <<< CHANGE THIS TO YOUR ACTUAL SIGNUP BUTTON ID/SELECTOR
    button = WebDriverWait(context.browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, button_id))
    )
    button.click()

@then('I should see a message "{message}"')
def step_impl(context, message):
    # Look for the message within an element.
    # Adjust the XPath selector to match where messages appear (e.g., a div with class 'alert' or 'message')
    try:
        # Correct usage: Pass locator tuple first, then the expected text
        element = WebDriverWait(context.browser, 10).until( # Reduced wait time
            EC.text_to_be_present_in_element((By.ID, "signup-message"), message)
        )
        assert message in element.text, f"Expected message '{message}' not found in element text: '{element.text}'"
    except Exception as e:
        # If the element isn't found or visible, check the whole page source as a fallback
        assert message in context.browser.page_source, f"Expected message '{message}' not found anywhere on the page. Error finding specific element: {e}"
        # If the element isn't found or visible, check the whole page source as a fallback
        assert message in context.browser.page_source, f"Expected message '{message}' not found anywhere on the page. Error finding specific element: {e}"