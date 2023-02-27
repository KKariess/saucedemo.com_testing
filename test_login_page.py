import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

link = "https://www.saucedemo.com/"


@pytest.fixture(scope="function")
def browser():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()


@pytest.mark.smoke
class TestSmoke:

    def test_smoke_page_opens(self, browser):
        browser.get(link)
        assert browser.title in "Swag Labs", "Incorrect page title/Page is not opened"

    def test_smoke_login(self, browser):
        browser.get(link)
        browser.find_element(By.CSS_SELECTOR, "#user-name").send_keys("standard_user")
        browser.find_element(By.CSS_SELECTOR, "#password").send_keys("secret_sauce")
        browser.find_element(By.CSS_SELECTOR, "#login-button").click()
        assert browser.find_element(By.CSS_SELECTOR, "#react-burger-menu-btn"), "Standard_user login failed"


@pytest.mark.criticalpath
class TestCriticalPath:

    def test_locked_user_login(self, browser):
        browser.get(link)
        browser.find_element(By.CSS_SELECTOR, "#user-name").send_keys("locked_out_user")
        browser.find_element(By.CSS_SELECTOR, "#password").send_keys("secret_sauce")
        browser.find_element(By.CSS_SELECTOR, "#login-button").click()
        assert browser.find_element(By.CSS_SELECTOR, ".error-message-container"), \
            "No Locked User error message was displayed"
        assert browser.find_element(By.CSS_SELECTOR, ".error-button").text in \
               "Epic sadface: Sorry, this user has been locked out.", "Locked User error message is incorrect"

    def test_problem_user_login(self, browser):
        browser.get(link)
        browser.find_element(By.CSS_SELECTOR, "#user-name").send_keys("problem_user")
        browser.find_element(By.CSS_SELECTOR, "#password").send_keys("secret_sauce")
        browser.find_element(By.CSS_SELECTOR, "#login-button").click()
        assert browser.find_element(By.CSS_SELECTOR, "#react-burger-menu-btn"), "Problem_User login failed"

    def test_performance_glitch_user_login(self, browser):
        browser.get(link)
        browser.find_element(By.CSS_SELECTOR, "#user-name").send_keys("performance_glitch_user")
        browser.find_element(By.CSS_SELECTOR, "#password").send_keys("secret_sauce")
        browser.find_element(By.CSS_SELECTOR, "#login-button").click()
        assert browser.find_element(By.CSS_SELECTOR, "#react-burger-menu-btn"), \
            "Performance_glitch_user login failed"

    def test_username_placeholder(self, browser):
        browser.get(link)
        assert browser.find_element(By.CSS_SELECTOR, "#user-name").get_attribute("placeholder") \
               in "Username", "Incorrect Username field placeholder"

    def test_password_placeholder(self, browser):
        browser.get(link)
        assert browser.find_element(By.CSS_SELECTOR, "#password").get_attribute("placeholder") \
               in "Password", "Incorrect Password field placeholder"


@pytest.mark.negative
class TestNegativeScenarios:

    def test_no_username_input(self, browser):
        browser.get(link)
        browser.find_element(By.CSS_SELECTOR, "#password").send_keys("secret_sauce")
        browser.find_element(By.CSS_SELECTOR, "#login-button").click()
        assert browser.find_element(By.CSS_SELECTOR, ".error-message-container"), \
            "No error message was displayed for username input"
        assert browser.find_element(By.CSS_SELECTOR, "[data-test='error']").text in \
               "Epic sadface: Username is required", "'No username input' error message is incorrect"

    def test_no_password_input(self, browser):
        browser.get(link)
        browser.find_element(By.CSS_SELECTOR, "#user-name").send_keys("standard_user")
        browser.find_element(By.CSS_SELECTOR, "#login-button").click()
        assert browser.find_element(By.CSS_SELECTOR, ".error-message-container"), \
            "No error message was displayed for password input"
        assert browser.find_element(By.CSS_SELECTOR, "[data-test='error']").text in \
               "Epic sadface: Password is required", "'No username input' error message is incorrect"

    def test_incorrect_username(self, browser):
        browser.get(link)
        browser.find_element(By.CSS_SELECTOR, "#user-name").send_keys("user")
        browser.find_element(By.CSS_SELECTOR, "#password").send_keys("secret_sauce")
        browser.find_element(By.CSS_SELECTOR, "#login-button").click()
        assert browser.find_element(By.CSS_SELECTOR, ".error-message-container"), \
            "No error message was displayed for incorrect username input"
        assert browser.find_element(By.CSS_SELECTOR, "[data-test='error']").text in \
               "Epic sadface: Username and password do not match any user in this service", \
            "'Incorrect username/password input' error message is incorrect"

    def test_incorrect_password(self, browser):
        browser.get(link)
        browser.find_element(By.CSS_SELECTOR, "#user-name").send_keys("standard_user")
        browser.find_element(By.CSS_SELECTOR, "#password").send_keys("pass")
        browser.find_element(By.CSS_SELECTOR, "#login-button").click()
        assert browser.find_element(By.CSS_SELECTOR, ".error-message-container"), \
            "No error message was displayed for incorrect password input"
        assert browser.find_element(By.CSS_SELECTOR, "[data-test='error']").text in \
               "Epic sadface: Username and password do not match any user in this service", \
            "'Incorrect username/password input' error message is incorrect"
