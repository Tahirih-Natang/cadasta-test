from selenium_tests.test import SeleniumTestCase
from selenium_tests.webdriver import CustomWebDriver
from selenium_tests.entities import Credentials

class PasswordReset(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_password_reset(self):
        self.user_login()
        self.wd.wait_for_css('.btn-user')
        self.open("/account/password/reset/")
        self.wd.find_css('#id_email').send_keys(Credentials.get_test_email())
        self.wd.find_element_by_xpath('//input[@value="Reset password"]').click()
        text = self.wd.find_element_by_xpath("//h1").text
        assert text == "Password reset"

    def tearDown(self):
        self.wd.quit()


class PasswordChange(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_password_change_success(self):
        self.user_login()
        self.wd.wait_for_css('.btn-user')
        self.open("/account/password/change/")
        self.wd.wait_for_css('#id_oldpassword')

        self.wd.find_css('#id_oldpassword').send_keys("XYZ#qwerty")
        self.wd.find_css('#id_password1').send_keys("XYZ#qwertyA")
        self.wd.find_css('#id_password2').send_keys("XYZ#qwertyA")
        self.wd.find_elements_by_xpath("//button[contains(text(), 'Change password')]")[0].click()
        text = self.wd.find_element_by_xpath("//h1").text
        assert text == "Update your profile"
        self.open("/account/logout/")
        self.restore_password("XYZ#qwerty", "XYZ#qwertyA")

    def test_password_change_failure(self):
        self.user_login()
        self.wd.wait_for_css('.btn-user')
        self.open("/account/password/change/")
        self.wd.wait_for_css('#id_oldpassword')

        self.wd.find_css('#id_oldpassword').send_keys("abc")
        self.wd.find_css('#id_password1').send_keys("XYZ#qwertyA")
        self.wd.find_css('#id_password2').send_keys("XYZ#qwertyA")
        self.wd.find_elements_by_xpath("//button[contains(text(), 'Change password')]")[0].click()
        text = self.wd.find_element_by_xpath("//h1").text
        assert text == "Change your password"

    def tearDown(self):
        self.wd.quit()


class UsernameChange(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_username_change(self):
        self.user_login()
        self.wd.wait_for_css('.btn-user')
        self.open("/account/profile/")

        self.wd.find_css('#id_username').clear()
        self.wd.find_css('#id_username').send_keys("cadasta-test-user-Y")
        self.wd.find_element_by_xpath('//button[@name="update"]').click()

        # text = self.wd.find_elements_by_xpath("//span[@class, 'username')]").text
        # print text
        # assert text == "cadasta-test-user-11"

    def tearDown(self):
        self.restore_username(Credentials.get_test_username())
        self.wd.quit()


class FullnameChange(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_fullname_change(self):
        self.user_login()
        self.wd.wait_for_css('.btn-user')
        self.open("/account/profile/")

        self.wd.find_css('#id_full_name').clear()
        self.wd.find_css('#id_full_name').send_keys("cadasta-test-user-1-fullname")
        self.wd.find_element_by_xpath('//button[@name="update"]').click()

    def tearDown(self):
        self.restore_fullname("")
        self.wd.quit()


class EmailChange(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_email_change(self):
        self.user_login()
        self.wd.wait_for_css('.btn-user')
        self.open("/account/profile/")

        self.wd.find_css('#id_email').clear()
        self.wd.find_css('#id_email').send_keys("cadasta-test-user-1@abc.com")
        self.wd.find_element_by_xpath('//button[@name="update"]').click()

    def tearDown(self):
        self.restore_email(Credentials.get_test_email())
        self.wd.quit()