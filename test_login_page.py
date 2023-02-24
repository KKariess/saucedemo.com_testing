import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

link = "https://www.saucedemo.com/"


class TestSmoke():

    def setup_method(self):
        # print("\nLaunching new browser for test...")
        self.browser = webdriver.Chrome()

    def teardown_method(self):
        # print("\nClosing browser...")
        self.browser.quit()

    def test_smoke_page_opens(self):
        self.browser.get(link)
        assert self.browser.title in "Swag Labs", "Incorrect page title/Page is not opened"

    def test_smoke_login(self):
        self.browser.get(link)
        self.browser.find_element(By.CSS_SELECTOR, "#user-name").send_keys("standard_user")
        self.browser.find_element(By.CSS_SELECTOR, "#password").send_keys("secret_sauce")
        self.browser.find_element(By.CSS_SELECTOR, "#login-button").click()
        assert self.browser.find_element(By.CSS_SELECTOR, "#react-burger-menu-btn"), "Standard_user login failed"


class TestCriticalPath():

    def setup_method(self):
        # print("\nLaunching new browser for test...")
        self.browser = webdriver.Chrome()

    def teardown_method(self):
        # print("\nClosing browser...")
        self.browser.quit()

    def test_locked_user_login(self):
        self.browser.get(link)
        self.browser.find_element(By.CSS_SELECTOR, "#user-name").send_keys("locked_out_user")
        self.browser.find_element(By.CSS_SELECTOR, "#password").send_keys("secret_sauce")
        self.browser.find_element(By.CSS_SELECTOR, "#login-button").click()
        assert self.browser.find_element(By.CSS_SELECTOR, ".error-message-container"), \
            "No Locked User error message was displayed"
        assert self.browser.find_element(By.CSS_SELECTOR, ".error-button").text in \
               "Epic sadface: Sorry, this user has been locked out.", "Locked User error message is incorrect"

    def test_problem_user_login(self):
        self.browser.get(link)
        self.browser.find_element(By.CSS_SELECTOR, "#user-name").send_keys("problem_user")
        self.browser.find_element(By.CSS_SELECTOR, "#password").send_keys("secret_sauce")
        self.browser.find_element(By.CSS_SELECTOR, "#login-button").click()
        assert self.browser.find_element(By.CSS_SELECTOR, "#react-burger-menu-btn"), "Problem_User login failed"

    def test_performance_glitch_user_login(self):
        self.browser.get(link)
        self.browser.find_element(By.CSS_SELECTOR, "#user-name").send_keys("performance_glitch_user")
        self.browser.find_element(By.CSS_SELECTOR, "#password").send_keys("secret_sauce")
        self.browser.find_element(By.CSS_SELECTOR, "#login-button").click()
        assert self.browser.find_element(By.CSS_SELECTOR, "#react-burger-menu-btn"), \
            "Performance_glitch_user login failed"

    def test_username_placeholder(self):
        self.browser.get(link)
        assert self.browser.find_element(By.CSS_SELECTOR, "#user-name").get_attribute("placeholder") \
               in "Username", "Incorrect Username field placeholder"

    def test_password_placeholder(self):
        self.browser.get(link)
        assert self.browser.find_element(By.CSS_SELECTOR, "#password").get_attribute("placeholder") \
               in "Password", "Incorrect Password field placeholder"


class TestNegativeScenarios():

    def setup_method(self):
        # print("\nLaunching new browser for test...")
        self.browser = webdriver.Chrome()

    def teardown_method(self):
        # print("\nClosing browser...")
        self.browser.quit()

    def test_no_username_input(self):
        self.browser.get(link)
        self.browser.find_element(By.CSS_SELECTOR, "#password").send_keys("secret_sauce")
        self.browser.find_element(By.CSS_SELECTOR, "#login-button").click()
        assert self.browser.find_element(By.CSS_SELECTOR, ".error-message-container"), \
            "No error message was displayed for username input"
        assert self.browser.find_element(By.CSS_SELECTOR, "[data-test='error']").text in \
               "Epic sadface: Username is required", "'No username input' error message is incorrect"

    def test_no_password_input(self):
        self.browser.get(link)
        self.browser.find_element(By.CSS_SELECTOR, "#user-name").send_keys("standard_user")
        self.browser.find_element(By.CSS_SELECTOR, "#login-button").click()
        assert self.browser.find_element(By.CSS_SELECTOR, ".error-message-container"), \
            "No error message was displayed for password input"
        assert self.browser.find_element(By.CSS_SELECTOR, "[data-test='error']").text in \
               "Epic sadface: Password is required", "'No username input' error message is incorrect"

    def test_incorrect_username(self):
        self.browser.get(link)
        self.browser.find_element(By.CSS_SELECTOR, "#user-name").send_keys("user")
        self.browser.find_element(By.CSS_SELECTOR, "#password").send_keys("secret_sauce")
        self.browser.find_element(By.CSS_SELECTOR, "#login-button").click()
        assert self.browser.find_element(By.CSS_SELECTOR, ".error-message-container"), \
            "No error message was displayed for incorrect username input"
        assert self.browser.find_element(By.CSS_SELECTOR, "[data-test='error']").text in \
               "Epic sadface: Username and password do not match any user in this service", \
            "'Incorrect username/password input' error message is incorrect"

    def test_incorrect_password(self):
        self.browser.get(link)
        self.browser.find_element(By.CSS_SELECTOR, "#user-name").send_keys("standard_user")
        self.browser.find_element(By.CSS_SELECTOR, "#password").send_keys("pass")
        self.browser.find_element(By.CSS_SELECTOR, "#login-button").click()
        assert self.browser.find_element(By.CSS_SELECTOR, ".error-message-container"), \
            "No error message was displayed for incorrect password input"
        assert self.browser.find_element(By.CSS_SELECTOR, "[data-test='error']").text in \
               "Epic sadface: Username and password do not match any user in this service", \
            "'Incorrect username/password input' error message is incorrect"

