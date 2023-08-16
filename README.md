# web_scraper_2023

### Setup:
Run from a virtual environment (Python 3.9) with installed dependencies listed in ```requirements.txt```.

[Instructions for installing using pip and virtual environments.](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

Install virtual environment: ```python3 -m pip install --user virtualenv```

Create virtual environment in project: ```python3 -m venv env```

Activate virtual environment: ```source env/bin/activate```

To deactivate virtual environment: ```deactivate```

Install required dependencies in virtual environment: ```pip install -r requirements.txt```

You will need chromedriver installed and an up-to-date version of the Chrome browser.

Install chromedriver with Homebrew: ```brew install chromedriver```

Locate chromedriver: ```which chromedriver```

Make your Mac trust chromedriver: ```xattr -d com.apple.quarantine <path_to_chromedriver>```

Add chromedriver path to the secrets module.

Add the website url and credentials to the secrets module.

### To run program:

Put your counties of interest in the list, ```COUNTIES_BY_STATE```, in ```application.py```, then run all of the scripts for the list:

```python application.py```

Program will pause for 2 minutes after entering credentials for user to manually solve CAPTCHAs