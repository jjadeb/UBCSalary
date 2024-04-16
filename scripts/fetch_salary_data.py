# author: Jade Bouchard
# date: 2024-04-15
#
# This script collects current and past salary data from The University of British Columbia's financial reports website:
# https://finance.ubc.ca/reporting-planning-analysis/financial-reports
# The script then saves the data in a dictionary format to a pickle file in the data folder
#
# Usage: python scripts/fetch_salary_data.py data/salary_data/raw_salary_data.pickle


from bs4 import BeautifulSoup
import requests
from pypdf import PdfReader
import pickle
import click
import regex as re
import io


def find_current_financial_report_links(financial_reports_link, financial_reports_header):
    ''' Fetches links to all available Financial Information Act Reports published by 
    The University of British Columbia. These reports should contain staff salary data.
    
    Parameters:
    ----------
    financial_reports_link : str
        A hyperlink to the University of British Columbia's financial reports page.
    financial_reports_header : str
        The header on the webpage, under which are the Financial Information Act Report links.

    Returns:
    -------
    links : dict
        A dictionary where the key is a year and the value is a link to that year's financial report.
        (ex: {year: link})
        
    Examples:
    --------
    >>> import regex as re
    >>> import requests
    >>> import from bs4 import BeautifulSoup
    >>>
    >>> financial_reports_link = 'https://finance.ubc.ca/reporting-planning-analysis/financial-reports'
    >>> financial_reports_header = 'Financial Information Act'
    >>> links = find_current_financial_report_links(financial_reports_link, financial_reports_header)
    '''
    # create an empty dictionary to hold financial report links for each year availible
    links = {}
    # go to financial report webpage
    r = requests.get(financial_reports_link, financial_reports_header) 
    # use BeautifulSoup to parse through the webpage elements
    soup = BeautifulSoup(r.content, 'html.parser')
    # find the "Financial Information Act" header
    finance_section = soup.find('h3', string = re.compile(financial_reports_header))
    # find the elements under the header with the financial report links links
    salary_link_elements = finance_section.find_next_sibling('ul').findAll('li') 
    for element in salary_link_elements: # loop through elements that contain links
        salary_link = element.find('a').get('href') # get link from element
        year = "20" + re.search("FY([0-9][0-9])", salary_link).group(1) # use regex to get the year in each link
        links[year] = salary_link # add year and link to dictionary 
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
@click.argument('raw_salary_data_output_folder', type=str)
def main(raw_salary_data_output_folder):
    '''collect and save salary data from The University of British Columbia's financial reports'''
    
    # Fetch links to all available Financial Act reports
    links = find_current_financial_report_links('https://finance.ubc.ca/reporting-planning-analysis/financial-reports', 'Financial Information Act')
    
    # Create an empty dictionary to store the raw salary text data
    raw_salary_dictionary = {}
    
    for year, link in links.items(): # for each year that UBC has data for
        salary_text_data = fetch_salary_data(link) # retrieve the text from the year's pdf
        raw_salary_dictionary[year] = salary_text_data # add the text to the raw data dictionary

    # Save the raw data dictionary
    with open(raw_salary_data_output_folder, 'wb') as f:
        pickle.dump(raw_salary_dictionary, f)
            
if __name__ == "__main__":
    main()

