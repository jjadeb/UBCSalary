# author: Jade Bouchard
# date: 2024-04-15
#
# This script collects current and past salary data from The University of British Columbia's financial reports website:
# https://finance.ubc.ca/reporting-planning-analysis/financial-reports
# The script then saves the data in a dictionary format to a pickle file in the data folder
#
# Usage: python scripts/fetch_salary_data.py --raw_salary_data_file=data/salary_data/raw_salary_data.pickle


from bs4 import BeautifulSoup
import requests
from pypdf import PdfReader
import pickle
import click
import regex as re
import io


def find_yearly_links(webpage):
    ''' Fetches links on a webpage between two given h3 string headers. Finds the financial year of the link.
    Returns a dictionary with the financial year as they key and the link as the value.
    
    Parameters:
    ----------
    webpage : str
        A hyperlink to a website. 
    start_header : str
        The header on the webpage, under which we would like to obtain links.
    end_header : str
        The header on the webpage, above which we would like to obtain links.

    Returns:
    -------
    links : dict
        A dictionary where the key is a year and the value is a link for that year.
        (ex: {year: link})
        
    Examples:
    --------
    >>> import regex as re
    >>> import requests
    >>> import from bs4 import BeautifulSoup
    >>>
    >>> webpage = 'https://finance.ubc.ca/reporting-planning-analysis/financial-reports'
    >>> start_header = 'Financial Information Act'
    >>> end_header = 'Task Force on Climate-Related Disclosures Report'
    >>> links = find_yearly_links(webpage, start_header, end_header)
    '''
    # create an empty dictionary to hold financial report links for each year availible
    links = {}
    # go to financial report webpage
    r = requests.get(webpage) 
    # use BeautifulSoup to parse through the webpage elements
    soup = BeautifulSoup(r.content, 'html.parser')
    # find all links on the webpage
    for link in soup.find_all('a'):
        potential_salary_link = link.get('href')
        # If the link is to a faculty salary document (SOFI), add it to the links dictionary
        if (type(potential_salary_link) == str) and (r"%20UBC%20Statement%20of%20Financial%20Information" in potential_salary_link):
            year = "20" + re.search("FY([0-9][0-9])", potential_salary_link).group(1) # use regex to get the year in each link
            links[year] = potential_salary_link # add year and link to dictionary 

    return links
        

def fetch_salary_data(pdf_link):
    '''Given a link to a pdf, return all text from the pdf.
    
    Parameters:
    ----------
    pdf_link : str
        A hyperlink to a pdf.

    Returns:
    -------
    all_text : str
        All the text in a pdf.
        
    Examples:
    --------
    >>> from pypdf import PdfReader
    >>> import io
    >>> import requests
    >>>
    >>> pdf_link = "https://finance.ubc.ca/sites/finserv.ubc.ca/files/FY23%20UBC%20Statement%20of%20Financial%20Information.pdf"
    >>> salary_text_data = fetch_salary_data(pdf_link)
    '''

    # access the content of the pdf link
    r = requests.get(pdf_link)
    f = io.BytesIO(r.content)
    
    all_text = "" # variable to store all text in pdf
    reader = PdfReader(f) # use PageReader to parse the pdf content
    contents = reader.pages # returns a list of pages
    for content in contents: # for each page, extract text
        all_text += content.extract_text() # add text to all_text string
        
    return all_text


@click.command()
@click.option('--raw_salary_data_file', type=str)
def main(raw_salary_data_file):
    ''' This function fetches links to all available Financial Act reports from the University of British Columbia (UBC) 
    website and collects any new salary data from those reports. It saves the raw salary data in a dictionary.

    Parameters:
    -----------
    raw_salary_data_file : str
        Path to the file where the raw salary data will be retrieved and saved.
    '''
    
    # Fetch links to all available Financial Act reports
    links = find_yearly_links('https://finance.ubc.ca/reporting-planning-analysis/financial-reports')
    
    # Create an empty dictionary to store the raw salary text data
    raw_salary_dictionary = {}

    # retrieve raw salary data previously collected
    with open(raw_salary_data_file, "rb") as raw_salary_dict:
        raw_salary_dictionary = pickle.load(raw_salary_dict)
    
    # collect salary data
    for year, link in links.items(): # for each year that UBC has data for
        if year not in raw_salary_dictionary.keys(): # if the salary data for this year hasn't been collected yet,
            print("collecting salary data for fiscal year " + year)
            salary_text_data = fetch_salary_data(link) # retrieve the text from the year's pdf
            raw_salary_dictionary[year] = salary_text_data # add the text to the raw data dictionary

    # Save the raw data dictionary
    with open(raw_salary_data_file, 'wb') as f:
        pickle.dump(raw_salary_dictionary, f)
            
if __name__ == "__main__":
    main()

