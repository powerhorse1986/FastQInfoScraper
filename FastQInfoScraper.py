import requests
import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def get_links(search_string):
    """Gets the links to the databases based on the search_string

    Parameters
    ----------
    search_string : str
        The searching keywords. Multiple keywords should be separated
        by whitespaces.

    Returns
    -------
    dictionary
        a dictionary with the key values are the names of the database,
        the values are links to the corresponding databases
    """
    url = "https://ngdc.cncb.ac.cn/"

    # We use the Google Chrome as our driver
    browser = webdriver.Chrome()
    browser.get(url)

    # Locates the search box using id
    search_box = browser.find_element(By.ID, "q")

    # Fills in our search_string and submit the string to the search
    # engine
    search_box.send_keys(search_string)
    search_box.submit()

    # Fetches the rows of the table with id 'DataTables_Table_0'
    entries = browser.find_elements(By.XPATH, "//*[@id='DataTables_Table_0']/tbody/tr")

    # Define a dictionary to store the links
    results = {}

    # A for loop iterates the rows. Each row is a WebElement
    for entry in entries:
        # An entry in fact is a <tr> in a table, and since a hyperlink locates in an
        # <a> tag, we have to fetch the <a> WebElement using find_element by tag name
        cell = entry.find_element(By.TAG_NAME, "a")

        # A cell is also a WebElement. It has an attribute "href". So, we can extract
        # out the link using get_attribute
        href = cell.get_attribute("href")

        results[cell.text] = href
    browser.close()
    return results

def gsa_iteration(gsa_link):
    """Iterates the pages of GSA (Gene Sequence Archive) database and extract the experiment
    information as well as the SRA accession numbers

    Parameters
    ----------
        gsa_link : str
            The link to the page for GSA searching results

    Returns
    -------
        dictionary
            a dictionary stores the experimental accession numbers and the SRA accession numbers.
            with the keys are the experimental accession numbers, the values are lists contain
            SRA accession numbers. one experimental accession numbers could refer to multiple SRA
            accession numbers, but one SRA accession number could only refer to one experimental
            accession number.
    """
    # We use the Google Chrome as our driver
    browser = webdriver.Chrome()
    browser.get(gsa_link)

    # Extract all the <h4> elements. Because the links to the experiments are put in <h4> elements
    # as <h4><a href="link">text</a></h4>
    elements = browser.find_elements(By.XPATH, "//*[@class='ui segment']/h4")

    for ele in elements:
        info = ele.find_element(By.TAG_NAME, "a")
        print(info.text)
        href = info.get_attribute("href")
        print(href)

results = get_links("cancer cell free methylation")
gsa_iteration(results["GSA"])