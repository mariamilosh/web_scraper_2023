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
        # for index, link in enumerate([self.company_links[0]]):
        for index, link in enumerate(self.company_links):
            print(link)
            # self.driver.get(secrets.SITE_URL + link)
            page = self._get_company_detail_page_for_company_link(index)
            # self._write_page_to_file(page, index)
            self.company_detail_pages.append(page)
        return self.company_detail_pages

    def _get_company_detail_page_for_company_link(self, index):
        """Use the requests session to get the company detail page."""
        self.driver.get(secrets.SITE_URL + self.company_links[index])
        # page = self.driver.find_element(By.CLASS_NAME, 'companyshell').get_attribute('innerHTML')
        # page = self.driver.find_element(By.CLASS_NAME, 'companyshell')
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "profilecontent")))
        page = self.driver.find_element(By.ID, "profilecontent").get_attribute('innerHTML')
        # page = self.driver.find_element(By.ID, 'profilecontent')
        return page
    
    # def _write_page_to_file(self, page, index):
    #     """Write the company detail page to a pickle file."""
    #     file_path = os.path.join(self.root_dir, 'pages', self.state, self.county)
    #     if not os.path.exists(file_path):
    #         os.mkdir(file_path)
    #     company_page_file = os.path.join(file_path, (self.county + '_' + str(index)))
    #     pickle_file = open(company_page_file, 'wb')
    #     pickle.dump(page, pickle_file)
    #     pickle_file.close()
    #     # print('Saved file: ', company_page_file)