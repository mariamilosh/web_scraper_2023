#!/usr/bin/env python
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import secrets.secrets as secrets
import scrape.get_company_pages as get_company_pages
import scrape.get_company_links as get_company_links
import scrape.parse_pages_to_csv as parse_pages_to_csv

COUNTIES_BY_STATE = {'IN': ['Allen'],
                     'MI': ['Manistee'], 
                     'PA': ['Adams']}

def main():
    chrome_options = Options()
    service = Service(secrets.CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(secrets.SITE_URL)
    login_to_website(driver)
    for state, counties in COUNTIES_BY_STATE.items():
        for county in counties:
            company_links = get_company_links.CompanyLinks(driver, state, county)
            links = company_links.get_links()
            company_pages = get_company_pages.CompanyPages(driver, state, county)
            pages = company_pages.get_pages(links)
            company_csv = parse_pages_to_csv.CompanyCSV(state, county)
            company_csv.create_csv(pages)

    time.sleep(5)

    driver.quit()

def login_to_website(driver):
    """Use webdriver to log in to the site from the login page."""
    driver.get(secrets.SITE_URL + '/login/')
    email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Email")))
    email.send_keys(secrets.EMAIL)

    password = driver.find_element(By.NAME, "Password")
    password.send_keys(secrets.PASSWORD)
    login = driver.find_element(By.ID, "logintableloginbutton")
    login.click()
    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.CLASS_NAME, "dashboardfeaturebox")))

if __name__ == '__main__':
    main()