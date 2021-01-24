from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import secret
from time import sleep



class InstaBot:
    BASE_URL = "https://www.instagram.com/"

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = Chrome()
        self.wait = WebDriverWait(self.driver, 15)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.driver.get(self.BASE_URL)


    def login(self):
        USERNAME_FIELD = "//input[@type='text']"
        PASSWORD_FIELD = "//input[@type='password']"

        self.driver.find_element_by_xpath(USERNAME_FIELD).send_keys(self.username)
        self.driver.find_element_by_xpath(PASSWORD_FIELD).send_keys(self.password)
        self.driver.find_element_by_xpath(PASSWORD_FIELD).send_keys(Keys.ENTER)
        self.wait.until(EC.url_contains("accounts/"))


    def follow(self, target, quantity=10):
        account_url = self.BASE_URL + f"{target.lower()}" + '/'
        self.driver.get(account_url)
        self.wait.until(EC.title_contains(target))

        FOLLOWING_LINK = f"//a[@href='/{target}/following/']"
        self.driver.find_element_by_xpath(FOLLOWING_LINK).click()
        FOLLOW_BTNS = "//button[text()='Follow']"
        follow_btns = self.driver.find_elements_by_xpath(FOLLOW_BTNS)

        if len(follow_btns) == 0:
            popup = self.driver.find_element_by_class_name('isgrP')
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', popup)
            follow_btns = self.driver.find_elements_by_xpath(FOLLOW_BTNS)

        for btn in follow_btns[:quantity + 1]:
            btn.click()
            sleep(1)


    def close(self):
        self.driver.close()



target_account = ''  # username of the account you want to access
bot = InstaBot(secret.USERNAME, secret.PASSWORD)
bot.login()
bot.follow(target_account)
bot.close()