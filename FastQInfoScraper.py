import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By

def get_results(search_string):
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
        print(cell.text)
        # A cell is also a WebElement. It has an attribute "href". So, we can extract
        # out the link using get_attribute
        href = cell.get_attribute("href")
        print(href)
        results[cell.text] = href
    browser.close()
    return results

print(get_results("cancer cell free methylation"))