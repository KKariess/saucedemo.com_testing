import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
link = "https://www.saucedemo.com/"

class TestSmoke():
    def setup_method(self):
        #print("\nLaunching new browser for test...")
        self.browser = webdriver.Chrome()
    def teardown_method(self):
        #print("\nClosing browser...")
        self.browser.quit()
    def test_smoke_page_opens(self):
        self.browser.get(link)
        assert self.browser.title in "Swag Labs", "Incorrect page title/Page is not opened"
    def test_smoke_login(self):
        self.browser.get(link)
        self.browser.find_element(By.CSS_SELECTOR, "#user-name").send_keys("standard_user")
        self.browser.find_element(By.CSS_SELECTOR, "#password").send_keys("secret_sauce")
        self.browser.find_element(By.CSS_SELECTOR, "#login-button").click()
        assert self.browser.find_element(By.CSS_SELECTOR, "#react-burger-menu-btn"), "Login failed"

class TestCriticalPath():
    def setup_method(self):
        #print("\nLaunching new browser for test...")
        self.browser = webdriver.Chrome()
    def teardown_method(self):
        #print("\nClosing browser...")
        self.browser.quit()
    def test_locked_user_access(self):
        self.browser.get(link)
        self.browser.find_element(By.CSS_SELECTOR, "#user-name").send_keys("locked_out_user")
        self.browser.find_element(By.CSS_SELECTOR, "#password").send_keys("secret_sauce")
        self.browser.find_element(By.CSS_SELECTOR, "#login-button").click()
        assert self.browser.find_element(By.CSS_SELECTOR, ".error-message-container"), \
            "No Locked User error message was displayed"
        assert self.browser.find_element(By.CSS_SELECTOR, ".error-button").text in \
               "Epic sadface: Sorry, this user has been locked out.", "Locked User error message is incorrect"
    def test_username_placeholder(self):
        self.browser.get(link)
        assert self.browser.find_element(By.CSS_SELECTOR, "#user-name").get_attribute("placeholder") \
               in "Username", "Incorrect Username field placeholder"
    def test_password_placeholder(self):
        self.browser.get(link)
        assert self.browser.find_element(By.CSS_SELECTOR, "#password").get_attribute("placeholder") \
               in "Password", "Incorrect Password field placeholder"


