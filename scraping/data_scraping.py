"""
Script for scraping AP Polls such as:
'http://www.collegepollarchive.com/football/ap/seasons.cfm?appollid=1#.W-yFSpNKiMr

.. moduleauthor:: Kevin Cass <kcass6@gatech.edu>
"""

from bs4 import BeautifulSoup as BS
from urllib.request import urlopen
import pandas as pd


def gen_scraped_df():
    # load poll index template
    all_ap_index = pd.read_csv('AP_index_template.csv')
    # define how many polls to grab. 1 = October 19, 1936, 1147 = Most Recent(November 11, 2018)
    polls_to_scrape = range(1022, 1145)
    urls = []
    # create a list containing the URLs for each poll to scrape
    for i in polls_to_scrape:
        urls.append('{0}{1}{2}'.format('http://www.collegepollarchive.com/football/ap/seasons.cfm?appollid=',
                                       str(i),
                                       '#.W-yFSpNKiMr'))
    ap_dict = dict()
    rows_count = 0
    poll_count = 0
    for url in urls:
        poll_count += 1
        ap_index = all_ap_index.iloc[(poll_count - 1), :]
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
        row_count = 0
        for row in ap_table_rows[8:]:
            if row.text.strip() != '':
                row_count += 1
                cells = row.find_all('td')
                col_count = 0
                for cell in cells:
                    feature = features[col_count]
                    text = cell.text.strip().encode().decode('utf-8')
                    if col_count == 1:
                        text = text[2:]
                    if feature in ap_dict:
                        ap_dict[feature].append(str(text))
                    else:
                        ap_dict[feature] = ['na'] * (rows_count + row_count - 1)
                        ap_dict[feature].append(str(text))
                    col_count += 1
            else:
                rows_count += row_count
                break

        # replace non-numeric ranks
        if rows_count == row_count:
            ap_dict['Rank'] = list(range(1, row_count + 1))
        else:
            ap_dict['Rank'] = ap_dict['Rank'][:-row_count] + list(range(1, row_count + 1))

        # add week column for data pairing
        if 'Week' in ap_dict:
            ap_dict['Week'].extend([str(ap_index.Week)] * row_count)
        else:
            ap_dict['Week'] = [str(ap_index.Week)] * row_count

        # add year column for data pairing
        if 'Year' in ap_dict:
            ap_dict['Year'].extend([str(ap_index.Year)] * row_count)
        else:
            ap_dict['Year'] = [str(ap_index.Year)] * row_count

        # fill missing data
        for missing_f in list(set(ap_dict.keys()).difference(features)):
            if missing_f not in ['Week', 'Year']:
                ap_dict[missing_f].extend(['na'] * row_count)

    # generate a pandas dataframe
    s_df = pd.DataFrame.from_dict(ap_dict, dtype=str)
    # clean team column
    s_df['Team'] = s_df['Team (FPV)'].apply(lambda team_fpv: team_fpv.split(" (", 1)[0])
    # clean rank column
    s_df.loc[s_df.Pts == '0', 'Rank'] = '50'
    return s_df


def print_csv(df, name):
    # print to csv file in root directory
    df.to_csv(name)


def read_csv(name):
    # print to csv file in root directory
    return pd.read_csv(name)


def create_training_dataset(s_df):
    t_df = pd.read_csv('training_data_template.csv')
    # join to match rank to team
    t_df['Match_Rank'] = t_df['Team'] + t_df['Year'].map(str) + t_df['Week'].map(str)
    s_df['Match_Rank'] = s_df['Team'] + s_df['Year'].map(str) + s_df['Week'].map(str)
    t_df_2 = pd.merge(t_df, s_df[['Match_Rank', 'Rank']], on='Match_Rank', how='left')
    # join to match PrevRank to team
    s_df['Week'] = pd.to_numeric(s_df['Week'], errors='coerce')
    s_df['PrevWeek'] = s_df['Week'] + 1
    s_df['PrevRank'] = s_df['Rank']
    t_df_2['Match_PrevRank'] = t_df_2['Match_Rank']
    s_df['Match_PrevRank'] = s_df['Team'] + s_df['Year'].map(str) + s_df['PrevWeek'].map(str)
    t_df_3 = pd.merge(t_df_2, s_df[['Match_PrevRank', 'PrevRank']], on='Match_PrevRank', how='left')
    # join to match PrevRankOpp to team
    t_df_4 = t_df_3.copy()
    t_df_3['Match_RankDiff'] = t_df_3['Match_Rank']
    t_df_4['Match_RankDiff'] = t_df_4['OppTeam'] + t_df_4['Year'].map(str) + t_df['Week'].map(str)
    t_df_3['PrevRankOpp'] = t_df_3['PrevRank']
    final_t_df = pd.merge(t_df_4, t_df_3[['Match_RankDiff', 'PrevRankOpp']], on='Match_RankDiff', how='left')
    # replace all nan values with 50
    final_t_df.loc[:, ['Rank', 'PrevRank', 'PrevRankOpp']] = final_t_df[['Rank', 'PrevRank', 'PrevRankOpp']].fillna(50)
    # calculate RankDiff
    final_t_df['RankDiff'] = final_t_df['PrevRank'] - final_t_df['PrevRankOpp']
    return final_t_df[['Year', 'Team', 'Week', 'RankDiff', 'OppTeam', 'Rank', 'PrevRank']]


scraped_df = gen_scraped_df()
print_csv(scraped_df, 'scraped_data.csv')
training_df = create_training_dataset(scraped_df)
print_csv(training_df, 'training_data.csv')
