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


# COUNTIES_BY_STATE = {'IN': ['Adams', 'Allen'],
#                         'MI': ['Alcona', 'Ionia'], 
#                         'PA': ['Allegheny']}

COUNTIES_BY_STATE = {'IN': ['Allen'],
                     'MI': ['Manistee'], 
                     'PA': ['Adams']}

def main():
    chrome_options = Options()
    service = Service('/opt/homebrew/bin/chromedriver')
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

    time.sleep(5) # Let the user actually see something!

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

# Ohio Counties
# counties = ['Adams', 'Allen', 'Ashland', 'Ashtabula', 'Athens', 'Auglaize', 
#             'Belmont', 'Brown', 'Butler', 'Carroll', 'Champaign', 'Clark', 
#             'Clermont', 'Clinton', 'Columbiana', 'Coshocton', 'Crawford', 
#             'Cuyahoga', 'Darke', 'Defiance', 'Delaware', 'Erie', 
#             'Fairfield', 'Fayette', 'Franklin', 'Fulton', 'Gallia', 
#             'Geauga', 'Greene', 'Guernsey', 'Hamilton', 'Hancock', 
#             'Hardin', 'Harrison', 'Henry', 'Highland', 'Hocking','Holmes', 
#             'Huron', 'Jackson', 'Jefferson', 'Knox', 'Lake', 'Lawrence', 
#             'Licking', 'Logan', 'Lorain', 'Lucas', 'Madison', 'Mahoning', 
#             'Marion', 'Medina', 'Meigs', 'Mercer', 'Miami', 'Monroe', 
#             'Montgomery', 'Morgan', 'Morrow', 'Muskingum', 'Noble', 
#             'Ottawa', 'Paulding', 'Perry', 'Pickaway', 'Pike', 'Portage', 
#             'Preble', 'Putnam', 'Richland', 'Ross', 'Sandusky', 'Scioto', 
#             'Seneca', 'Shelby', 'Stark', 'Summit', 'Trumbull', 'Tuscarawas', 
#             'Union', 'Van Wert', 'Vinton', 'Warren', 'Washington', 'Wayne', 
#             'Williams', 'Wood', 'Wyandot']
# Michigan Counties
# counties = ['Alcona', 'Ionia', 'Osceola', 'Alger', 'Iosco', 'Oscoda', 
#             'Allegan', 'Iron', 'Otsego', 'Alpena', 'Isabella', 'Ottawa', 
#             'Antrim', 'Jackson', 'Presque Isle', 'Arenac', 'Kalamazoo', 
#             'Roscommon', 'Baraga', 'Kalkaska', 'Saginaw', 'Barry', 'Kent', 
#             'St. Clair', 'Bay', 'Keweenaw', 'St. Joseph', 'Benzie', 'Lake', 
#             'Sanilac', 'Berrien', 'Lapeer', 'Schoolcraft', 'Branch', 
#             'Leelanau', 'Shiawassee', 'Calhoun', 'Lenawee', 'Tuscola', 
#             'Cass', 'Livingston', 'Van Buren', 'Charlevoix', 'Luce', 
#             'Washtenaw', 'Cheboygan', 'Mackinac', 'Wayne', 'Chippewa', 
#             'Macomb', 'Wexford', 'Clare', 'Manistee', 'Clinton', 
#             'Marquette', 'Crawford', 'Mason', 'Delta', 'Mecosta', 
#             'Dickinson', 'Menominee', 'Eaton', 'Midland', 'Emmet', 
#             'Missaukee', 'Genesee', 'Monroe', 'Gladwin', 'Montcalm', 
#             'Gogebic', 'Montmorency', 'Gd. Traverse', 'Muskegon', 'Gratiot', 
#             'Newaygo', 'Hillsdale', 'Oakland', 'Huron', 'Oceana', 
#             'Houghton', 'Ogemaw', 'Ingham', 'Ontonagon']
# Pennsylvania Counties
# counties = ['Adams', 'Allegheny', 'Armstrong', 'Beaver', 'Bedford', 'Berks', 
#             'Blair', 'Bradford', 'Bucks', 'Butler', 'Cambria', 'Cameron', 
#             'Carbon', 'Centre', 'Chester', 'Clarion', 'Clearfield', 
#             'Clinton', 'Columbia', 'Crawford', 'Cumberland', 'Dauphin', 
#             'Delaware', 'Elk', 'Erie', 'Fayette', 'Forest', 'Franklin', 
#             'Fulton', 'Greene', 'Huntingdon', 'Indiana', 'Jefferson', 
#             'Juniata', 'Lackawanna', 'Lancaster', 'Lawrence', 'Lebanon', 
#             'Lehigh', 'Luzerne', 'Lycoming', 'McKean', 'Mercer', 'Mifflin', 
#             'Monroe', 'Montgomery', 'Montour', 'Northampton', 
#             'Northumberland', 'Perry', 'Philadelphia', 'Pike', 'Potter', 
#             'Schuylkill', 'Snyder', 'Somerset', 'Sullivan', 'Susquehanna', 
#             'Tioga', 'Union', 'Venango', 'Warren', 'Washington', 'Wayne', 
#             'Westmoreland', 'Wyoming', 'York']
# Indiana Counties
# counties_by_state = {'IN': ['Adams', 'Allen', 'Bartholomew', 'Benton', 'Blackford', 
#                    'Boone', 'Brown', 'Carroll', 'Cass', 'Clark', 'Clay', 
#                    'Clinton', 'Crawford', 'Daviess', 'Dearborn', 'Decatur', 
#                    'DeKalb', 'Delaware', 'Dubois', 'Elkhart', 'Fayette', 
#                    'Floyd', 'Fountain', 'Franklin', 'Fulton', 'Gibson', 
#                    'Grant', 'Greene', 'Hamilton', 'Hancock', 'Harrison', 
#                    'Hendricks', 'Henry', 'Howard', 'Huntington', 'Jackson', 
#                    'Jasper', 'Jay', 'Jefferson', 'Jennings', 'Johnson', 
#                    'Knox', 'Kosciusko', 'LaGrange', 'Lake', 'LaPorte', 
#                    'Lawrence', 'Madison', 'Marion', 'Marshall', 'Martin', 
#                    'Miami', 'Monroe', 'Montgomery', 'Morgan', 'Newton', 
#                    'Noble', 'Ohio', 'Orange', 'Owen', 'Parke', 'Perry', 
#                    'Pike', 'Porter', 'Posey', 'Pulaski', 'Putnam', 
#                    'Randolph', 'Ripley', 'Rush', 'St. Joseph', 'Scott', 
#                    'Shelby', 'Spencer', 'Starke', 'Steuben', 'Sullivan', 
#                    'Switzerland', 'Tippecanoe', 'Tipton', 'Union', 
#                    'Vanderburgh', 'Vermillion', 'Vigo', 'Wabash', 'Warren', 
#                    'Warrick', 'Washington', 'Wayne', 'Wells', 'White', 
#                    'Whitley'],
#             'MI': ['Alcona', 'Ionia', 'Osceola', 'Alger', 'Iosco', 'Oscoda', 
#                    'Allegan', 'Iron', 'Otsego', 'Alpena', 'Isabella', 
#                    'Ottawa', 'Antrim', 'Jackson', 'Presque Isle', 'Arenac', 
#                    'Kalamazoo', 'Roscommon', 'Baraga', 'Kalkaska', 
#                    'Saginaw', 'Barry', 'Kent', 'St. Clair', 'Bay', 
#                    'Keweenaw', 'St. Joseph', 'Benzie', 'Lake', 'Sanilac', 
#                    'Berrien', 'Lapeer', 'Schoolcraft', 'Branch', 'Leelanau', 
#                    'Shiawassee', 'Calhoun', 'Lenawee', 'Tuscola', 'Cass', 
#                    'Livingston', 'Van Buren', 'Charlevoix', 'Luce', 
#                    'Washtenaw', 'Cheboygan', 'Mackinac', 'Wayne', 
#                    'Chippewa', 'Macomb', 'Wexford', 'Clare', 'Manistee', 
#                    'Clinton', 'Marquette', 'Crawford', 'Mason', 'Delta', 
#                    'Mecosta', 'Dickinson', 'Menominee', 'Eaton', 'Midland', 
#                    'Emmet', 'Missaukee', 'Genesee', 'Monroe', 'Gladwin', 
#                    'Montcalm', 'Gogebic', 'Montmorency', 'Gd. Traverse', 
#                    'Muskegon', 'Gratiot', 'Newaygo', 'Hillsdale', 'Oakland', 
#                    'Huron', 'Oceana', 'Houghton', 'Ogemaw', 'Ingham', 
#                    'Ontonagon'], 
#             'PA': ['Adams', 'Allegheny', 'Armstrong', 'Beaver', 'Bedford', 
#                    'Berks', 'Blair', 'Bradford', 'Bucks', 'Butler', 
#                    'Cambria', 'Cameron', 'Carbon', 'Centre', 'Chester', 
#                    'Clarion', 'Clearfield', 'Clinton', 'Columbia', 
#                    'Crawford', 'Cumberland', 'Dauphin', 'Delaware', 'Elk', 
#                    'Erie', 'Fayette', 'Forest', 'Franklin', 'Fulton', 
#                    'Greene', 'Huntingdon', 'Indiana', 'Jefferson', 
#                    'Juniata', 'Lackawanna', 'Lancaster', 'Lawrence', 
#                    'Lebanon', 'Lehigh', 'Luzerne', 'Lycoming', 'McKean', 
#                    'Mercer', 'Mifflin', 'Monroe', 'Montgomery', 'Montour', 
#                    'Northampton', 'Northumberland', 'Perry', 'Philadelphia', 
#                    'Pike', 'Potter', 'Schuylkill', 'Snyder', 'Somerset', 
#                    'Sullivan', 'Susquehanna', 'Tioga', 'Union', 'Venango', 
#                    'Warren', 'Washington', 'Wayne', 'Westmoreland', 
#                    'Wyoming', 'York']}