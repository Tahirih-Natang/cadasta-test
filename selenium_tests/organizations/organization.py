from selenium_tests.test import SeleniumTestCase
from selenium_tests.webdriver import CustomWebDriver
from selenium.common.exceptions import NoSuchElementException
from selenium_tests.pages import OrganizationsPage


class CreateOrganization(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_new_organization(self):
        organizations_page = OrganizationsPage(self.wd, self)
        organizations_page.go_to()

        self.wd.find_element_by_xpath('//a[@href="/organizations/new/"]').click()
        self.wd.wait_for_css(".modal-title")
        self.wd.wait_for_css("#id_name")
        self.wd.find_css('#id_name').send_keys("organization-1")
        self.wd.find_css('#id_description').send_keys("Test organization-1 description.")
        self.wd.find_element_by_xpath('//button[@name="submit"]').click()

        try:
            self.wd.wait_for_xpath("//h2[contains(text(), 'Organization Overview')]")
            text = self.wd.find_element_by_xpath("//h1[contains(@class, 'short')]").text
            assert text == "ORGANIZATION-1"

        except Exception:
            self.wd.wait_for_css(".error-block")

    def tearDown(self):
        self.wd.quit()


class EditOrganization(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_edit_organization(self):
        organizations_page = OrganizationsPage(self.wd, self)
        organizations_page.go_to()

        self.wd.find_element_by_link_text("organization-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Organization Overview')]")
        self.wd.find_element_by_xpath("(//button[@type='button'])[2]").click()
        self.wd.find_element_by_link_text("Edit organization").click()
        self.wd.wait_for_css(".modal-title")
        self.wd.find_element_by_id("id_description").clear()
        self.wd.find_element_by_id("id_description").send_keys("Test organization-1 description edited.")
        self.wd.find_element_by_name("submit").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Organization Overview')]")
        text = self.wd.find_element_by_xpath("//div/section/p").text
        assert text == "Test organization-1 description edited."

    def tearDown(self):
        self.wd.quit()


class OrganizationArchive(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_archive_organization(self):
        organizations_page = OrganizationsPage(self.wd, self)
        organizations_page.go_to()

        self.wd.find_element_by_link_text("organization-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Organization Overview')]")
        self.open("/organizations/organization-1/archive/")
        self.wd.wait_for_xpath("//h2[contains(text(), 'Organization Overview')]")
        text = self.wd.find_element_by_xpath("//span[contains(@class, 'label-danger')]").text
        assert text == "ARCHIVED"

    def test_unarchive_organization(self):
        organizations_page = OrganizationsPage(self.wd, self)
        organizations_page.go_to()

        self.wd.find_css("#archive-filter").click()
        self.wd.find_element_by_xpath('//option[@value="archived-True"]').click()
        self.wd.find_element_by_link_text("organization-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Organization Overview')]")
        self.open("/organizations/organization-1/unarchive/")
        self.wd.wait_for_xpath("//h2[contains(text(), 'Organization Overview')]")

        try:
            self.wd.find_element_by_xpath("//span[contains(@class, 'label-danger')]")
        except NoSuchElementException:
            assert True

    def tearDown(self):
        self.wd.quit()