import os, time
from selenium.webdriver.common.by import By

import secrets.secrets as secrets

class CompanyLinks:
    def __init__(self, driver, state, county):
        self.state = state
        self.county = county.title()
        self.driver = driver
        self.company_links = []
        self.root_dir = os.getcwd()
        self.company_count = 0

    def get_links(self):
        # self.company_links = self._read_list_of_pickled_company_links_from_file()
        # self._configure()
        # self._login_to_website()
        self._input_county_to_search_on_list_page()
        self._navigate_to_list_of_companies_page()
        self._scrape_links_from_paginated_list_of_companies()
        self._clean_up_county_search()

        # for index, link in enumerate(self.company_links):
        #     page = self._get_company_detail_page_for_company_link(index)
        #     self._write_page_to_file(page, index)
        # self.driver.close()
        print('There are {0} companies in {1} county.'.format(len(self.company_links), self.county))
        # print(self.company_links)
        return self.company_links
    
    def _input_county_to_search_on_list_page(self):
        """Use webdriver to input the county that is to be searched
        from the list page.
        """
        self.driver.get(secrets.SITE_URL + '/list/geography')
        time.sleep(2)
        previous_counties_to_remove = self.driver.find_elements(By.CLASS_NAME, 'listed')
        for county in previous_counties_to_remove:
            county.click()

        # state_input_field = self.driver.find_element_by_id('statesearch')
        county_input_field = self.driver.find_element(By.ID, 'countysearch')
        county = self.county
        county_and_state = self.county + ' County, ' + self.state
        county_input_field.send_keys(county)
        time.sleep(2)
        js_string = "e=$('.ui-menu-item-wrapper:contains({})'); e.click()".format(county_and_state)
        self.driver.execute_script(js_string)
        self.driver.execute_script(js_string) # need to do this twice because it clicks on the first element the first time

    def _navigate_to_list_of_companies_page(self):
        """Use webdriver to click the link that results in navigation
        to the list of companies page.
        """
        time.sleep(3)
        list_of_companies_count_button = self.driver.find_element(By.ID, 'listcounttab')
        count_str = list_of_companies_count_button.text
        self.company_count = int(''.join(filter(str.isdigit, count_str)))
        print(self.company_count)
        list_of_companies_count_button.click()

    def _scrape_links_from_paginated_list_of_companies(self):
        """Call the method that scrapes the company links for each
        paginated list of companies while using webdriver to navigate
        through the pagination.
        """
        self._scrape_links_from_single_page()
        try:
            while len(self.company_links) < self.company_count:
                js_string = "e=$('span:contains(Next)'); e.click();"
                self.driver.execute_script(js_string)
                time.sleep(2)
                self._scrape_links_from_single_page()
        except:
            pass

    def _scrape_links_from_single_page(self):
        """Use webdriver to get the company links."""
        companies = self.driver.find_elements(By.CLASS_NAME, 'listresultstabletdcompany')

        for i in range(1, len(companies)):
            link = companies[i].find_element(By.TAG_NAME, 'a')
            clean_link = self._clean_up_link(link)
            self.company_links.append(clean_link)

    def _clean_up_county_search(self):
        """Use webdriver to remove county that was just searched. This is to
        avoid a message appearing on subsequent runs.
        """
        self.driver.get(secrets.SITE_URL + '/list/geography')
        time.sleep(2)
        previous_counties_to_remove = self.driver.find_elements(By.CLASS_NAME, 'listed')
        for county in previous_counties_to_remove:
            county.click()

    def _clean_up_link(self, link):
        """Remove everything but the path that we need
        from a string that contained a link.
        """
        raw_href = link.get_attribute('href')
        # raw_href = link['href']
        # left_stripped_href = raw_href.lstrip("javascript:EZOpen('")
        left_stripped_href = raw_href.lstrip("javascript:Open('")
        clean_link = left_stripped_href.rstrip("');")
        return clean_link