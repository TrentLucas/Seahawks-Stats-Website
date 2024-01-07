# Website Scraper for Team Data (outputs tables below)
# Seasonal_Performance, Offensive_Team_Performance, Defensive_Team_Performance, Special_Team_Performance
# 
# Pulls data from URLs, converts the data the SQL database's desired format, and exports to CSV files
# Sleep times needed to not overload websites the scraper reads from
#
#         ***ALL CODE TO BE USED TO VIEWING PURPOSES ONLY. NO REUSING CODE FROM PROJECT***
##########################################################################################################

import pandas as pd
import random
import time



# set years
seasons = [str(season) for season in range(1976, 1980)]

# initialize all DFs
all_team_stats_df = pd.DataFrame()
all_spc_stats_df = pd.DataFrame()
all_off_stats_df = pd.DataFrame()
all_def_stats_df = pd.DataFrame()

# URLs that are only used once
url1 = 'https://www.pro-football-reference.com/teams/sea/'
url2 = 'https://www.pro-football-reference.com/teams/sea/single-season-returns.htm'
url3 = 'https://www.pro-football-reference.com/teams/sea/single-season-kicking.htm'



# table: Seasonal_Performance
all_seasons_stats_df = pd.read_html(url1, header=1, attrs={'id':'team_index'})[0]
all_seasons_stats_df = all_seasons_stats_df[['Year', 'W', 'T', 'L', 'Playoffs']]
all_seasons_stats_df = all_seasons_stats_df.drop([30, 31])
all_seasons_stats_df.columns = ['Year', 'Reg_season_win', 'Reg_season_ties', 'Reg_season_losses', 'Playoff_appearance']

time.sleep(random.randint(4, 5))



# table: Special_Team_Performance
spc_returns_df = pd.read_html(url2, header=1)[0]
spc_returns_df = spc_returns_df[['Year', 'Y/R', 'Y/Rt']]

time.sleep(random.randint(4, 5))

spc_kicks_df = pd.read_html(url3, header=1)[0]
spc_kicks_df = spc_kicks_df[['Year', 'FG%']]
spc_kicks_df = spc_kicks_df.drop([29])
spc_kicks_df['FG%'] = spc_kicks_df['FG%'].str.rstrip('%').astype('float')
spc_stats_df = pd.merge(spc_returns_df, spc_kicks_df, on='Year')
spc_stats_df['Y/R'] = pd.to_numeric(spc_stats_df['Y/R'], errors='coerce')
spc_stats_df['Y/Rt'] = pd.to_numeric(spc_stats_df['Y/Rt'], errors='coerce')
spc_stats_df = spc_stats_df.groupby(['Year'])[['Y/R', 'Y/Rt', 'FG%']].mean().round(1)
spc_stats_df = spc_stats_df.reset_index()
all_spc_stats_df = pd.concat([all_spc_stats_df, spc_stats_df], axis=1)
    


for season in seasons:
    # recursive URL
    url4 = 'https://www.pro-football-reference.com/teams/sea/' + season + '.htm'
    
    
    
    # print loop iteration in console
    print(url4)
        
    # contains 'season' year tuple for Offensive_Team_Performance and Defensive_Team_Performance
    team_stats_df = pd.read_html(url4, header=1, attrs={'id':'team_stats'})[0]
    team_stats_df['TD'] = team_stats_df['TD'] + team_stats_df['TD.1']
    team_stats_df = team_stats_df[['PF', 'Yds', 'TD', 'Int']]
    team_stats_df = team_stats_df.drop([2, 3])
    team_stats_df.insert(loc=0, column='Year', value=season)
    all_team_stats_df = pd.concat([all_team_stats_df, team_stats_df], ignore_index=True)
    
    time.sleep(random.randint(4, 5))
    
    
    
    # table: Offensive_Team_Performance
    off_stats_df = team_stats_df.iloc[0]
    off_stats_df = off_stats_df.drop('Int')
    all_off_stats_df = pd.concat([all_off_stats_df, off_stats_df], axis=1)
    
    
    
    # table: Defensive_Team_Performance
    def_stats_df = team_stats_df.iloc[1]
    def_stats_df = def_stats_df.drop('TD')
    def_stats_df = def_stats_df[['Year', 'Int', 'Yds', 'PF']]
    all_def_stats_df = pd.concat([all_def_stats_df, def_stats_df], axis=1)   

    time.sleep(random.randint(20, 30))



# restructure DFs
all_off_stats_df = all_off_stats_df.transpose()
all_def_stats_df = all_def_stats_df.transpose()

# rename columns
all_spc_stats_df.rename(columns={'Y/R':'Avg_punt_return_yards', 'Y/Rt':'Avg_kick_return_yards', 'FG%':'FG_percentage'}, inplace=True)
all_off_stats_df.rename(columns={'PF':'Points_per_game', 'Yds':'Total_yards', 'TD':'Total_touchdowns'}, inplace=True)
all_def_stats_df.rename(columns={'Int':'Total_interceptions', 'Yds':'Total_yards_allowed', 'PF':'Points_allowed_per_game'}, inplace=True)



# console log all tables
print(all_seasons_stats_df)
print(all_spc_stats_df)
print(all_off_stats_df)
print(all_def_stats_df)



# save files to CSVs
all_seasons_stats_df.to_csv("F:\\475\\csv_files\\sea_all_seasons_stats.csv", index=False)
all_spc_stats_df.to_csv("F:\\475\\csv_files\\sea_all_spc_stats.csv", index=False)
all_off_stats_df.to_csv("F:\\475\\csv_files\\sea_all_off_stats.csv", index=False)
all_def_stats_df.to_csv("F:\\475\\csv_files\\sea_all_def_stats.csv", index=False)
