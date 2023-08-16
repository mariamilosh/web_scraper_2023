from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import secrets.secrets as secrets

class CompanyPages:
    def __init__(self, driver, state, county):
        self.state = state
        self.county = county.title()
        self.driver = driver
        self.company_links = []
        self.company_detail_pages = []

    def get_pages(self, links):
        """The main method that calls the other methods and loops
        through the list of companies with the result of company detail
        pages being written to files.
        """
        self.company_links = links
        for index, link in enumerate(self.company_links):
            print(link)
            page = self._get_company_detail_page_for_company_link(index)
            self.company_detail_pages.append(page)
        return self.company_detail_pages

    def _get_company_detail_page_for_company_link(self, index):
        """Use the requests session to get the company detail page."""
        self.driver.get(secrets.SITE_URL + self.company_links[index])
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "profilecontent")))
        page = self.driver.find_element(By.ID, "profilecontent").get_attribute('innerHTML')
        return page