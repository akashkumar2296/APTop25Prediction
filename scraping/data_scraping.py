"""
Script for scraping AP Polls such as:
'http://www.collegepollarchive.com/football/ap/seasons.cfm?appollid=1#.W-yFSpNKiMr

.. moduleauthor:: Kevin Cass <kcass6@gatech.edu>
"""

from bs4 import BeautifulSoup as BS
from urllib.request import urlopen
import pandas as pd


def gen_df():
    # define how many polls to grab. 1 = October 19, 1936, 1147 = Most Recent(November 11, 2018)
    polls_to_scrape = range(1, 100)
    urls = []
    # create a list containing the URLs for each poll to scrape
    for i in polls_to_scrape:
        urls.append('{0}{1}{2}'.format('http://www.collegepollarchive.com/football/ap/seasons.cfm?appollid=',
                                       str(i),
                                       '#.W-yFSpNKiMr'))
    pre_df = dict()
    for url in urls:
        # load html using BeautifulSoup
        soup = BS(urlopen(url).read(), features='html.parser')
        ap_table = soup.find_all('table')[4]
        ap_table_rows = ap_table.find_all('tr')
        features = []
        # dynamically determine the headers in the table
        for header in ap_table_rows[7].find_all('th'):
            features.append(header.text.strip().encode().decode('utf-8'))
        features.insert(1, 'Last Rank')
        # store data from ap poll in a dict
        for row in ap_table_rows[8:]:
            if row.text.strip() != '':
                cells = row.find_all('td')
                count = 0
                for cell in cells:
                    feature = features[count]
                    text = cell.text.strip().encode().decode('utf-8')
                    if count == 1:
                        text = text[2:]
                    if feature in pre_df:
                        pre_df[feature].append(str(text))
                    else:
                        pre_df[feature] = [text]
                    count += 1
            else:
                break
    # generate a pandas dataframe
    df = pd.DataFrame.from_dict(pre_df, dtype=str)
    return df


def print_csv():
    df = gen_df()
    # print to csv file in root directory
    df.to_csv('scraped_data.csv')


print_csv()
