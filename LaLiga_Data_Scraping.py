#import all the required libraries
import time

import bs4 as bs
import pandas as pd
import requests

all_teams = [] #List of all the teams in La Liga

html  = requests.get('https://fbref.com/en/comps/12/La-Liga-Stats').text #getting the html of the website
soup = bs.BeautifulSoup(html, 'lxml')
table = soup.find_all('table', class_='stats_table')[0]#only want the first table, therefore the first index

links = table.find_all('a') #find all links in the table
links = [l.get('href') for l in links] #parsing through links
links = [l for l in links if '/squads/' in l] ## filtering through links to only get squads

team_urls = [f"https://fbref.com{l}" for l in links] ##formatting back to links

for team_url in team_urls:
    ##Get the name of the team by going over the url starting from the end and splitting it on every /,
    # and remove the -Stats portion of the url for a cleaner header of the table
    team_name = team_url.split('/')[-1].replace("-Stats","")
    data = requests.get(team_url).text
    soup = bs.BeautifulSoup(data,'lxml') # Use the lxml parser to manage the html in the team_url
    stats = soup.find_all('table', class_='stats_table')[0] #only want the first table

    if stats and stats.columns: stats.columns = stats.columns.droplevel()#formatting the stats

    ##Assuming 'team_data' is a BeautifulSoup tag
    ##Convert it into a DataFrame
    team_data = pd.read_html(str(stats))[0]
    team_data['Team'] = team_name
    all_teams.append(team_data) ##Appending data to our list of all teams
    time.sleep(5) ##making sure we don't get blocked from scraping by delaying each loop by 5 sec.

stat_df = pd.concat(all_teams) #concatenating all the stats
stat_df.to_csv('LaLiga_Stats.csv') ##importing to csv






