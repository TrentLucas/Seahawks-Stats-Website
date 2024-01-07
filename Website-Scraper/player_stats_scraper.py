# Website Scraper for Player Data (outputs tables below)
# Kicker_Performance, Wide_Receiver_Performance, Quarterback_Performance, Cornerback_Performance
# 
# Pulls data from URLs, converts the data the SQL database's desired format, 
#        merges with sea_all_players.csv, and exports to CSV files
# Sleep times needed to not overload websites the scraper reads from
#
#         ***ALL CODE TO BE USED TO VIEWING PURPOSES ONLY. NO REUSING CODE FROM PROJECT***
##################################################################################################

import pandas as pd
import random
import time



# set years
seasons = [str(season) for season in range(1976, 2024)]

# initialize all DFs
all_kicker_stats_df = pd.DataFrame()
all_receiver_stats_df = pd.DataFrame()
all_quarterback_stats_df = pd.DataFrame()
all_cornerback_stats_df = pd.DataFrame()

# read player numbers data gathered by player_numbers_scraper.py
all_player_numbers_df = pd.read_csv("F:\\475\\csv_files\\sea_all_players.csv")
all_player_numbers_df.rename(columns={'Years' : 'Year', 'Name' : 'Player'}, inplace=True)



# URLs that are only used once
url1 = 'https://www.pro-football-reference.com/teams/sea/single-season-passing.htm'
url2 = 'https://www.pro-football-reference.com/teams/sea/single-season-receiving.htm'

# table: Quarterback_Performance
all_quarterback_stats_df = pd.read_html(url1)[0]
all_quarterback_stats_df = all_quarterback_stats_df[all_quarterback_stats_df['Pos'] == 'QB']
all_quarterback_stats_df = all_quarterback_stats_df[['Year', 'Player', 'TD', 'Int']]

time.sleep(random.randint(4, 5))



# table: Wide_Receiver_Performance
all_receiver_stats_df = pd.read_html(url2)[0]
all_receiver_stats_df = all_receiver_stats_df[all_receiver_stats_df['Pos'] == 'WR']
all_receiver_stats_df = all_receiver_stats_df[['Year', 'Player', 'TD', 'Rec', 'Yds']]

time.sleep(random.randint(4, 5))
    


# recursive tables
for season in seasons:
    # recursive URLs
    url3 = 'https://www.pro-football-reference.com/years/' + season + '/kicking.htm'
    url4 = 'https://www.pro-football-reference.com/years/' + season + '/defense.htm'
    
    
    
    # print loop iteration in console
    print(url3)
        
    # table: Kicker_Performance
    kicker_stats_df = pd.read_html(url3, header=1, attrs={'id':'kicking'})[0]
    kicker_stats_df = kicker_stats_df[(kicker_stats_df['Tm'] == 'SEA') & (kicker_stats_df['Pos'] == 'K')]
    kicker_stats_df = kicker_stats_df[['Player', 'FG%', 'Lng']]
    kicker_stats_df['FG%'] = kicker_stats_df['FG%'].str.rstrip('%').astype('float')
    kicker_stats_df.insert(loc=0, column='Year', value=season)
    all_kicker_stats_df = pd.concat([all_kicker_stats_df, kicker_stats_df], ignore_index=True)
    
    time.sleep(random.randint(4, 5))
    
    
    
    # table: Cornerback_Performance
    cornerback_stats_df = pd.read_html(url4, header=1, attrs={'id':'defense'})[0]
    cornerback_stats_df = cornerback_stats_df[(cornerback_stats_df['Tm'] == 'SEA') & (cornerback_stats_df['Pos'].str.contains('CB'))]
    cornerback_stats_df = cornerback_stats_df[['Player', 'Int', 'FF', 'PD']]
    cornerback_stats_df.insert(loc=0, column='Year', value=season)
    all_cornerback_stats_df = pd.concat([all_cornerback_stats_df, cornerback_stats_df], ignore_index=True)

    time.sleep(random.randint(20, 30))



# remove unwanted characters from player names
all_kicker_stats_df['Player'] = all_kicker_stats_df['Player'].str.replace('*', '')
all_kicker_stats_df['Player'] = all_kicker_stats_df['Player'].str.replace('+', '')
all_receiver_stats_df['Player'] = all_receiver_stats_df['Player'].str.replace('*', '')
all_receiver_stats_df['Player'] = all_receiver_stats_df['Player'].str.replace('+', '')
all_quarterback_stats_df['Player'] = all_quarterback_stats_df['Player'].str.replace('*', '')
all_quarterback_stats_df['Player'] = all_quarterback_stats_df['Player'].str.replace('+', '')
all_cornerback_stats_df['Player'] = all_cornerback_stats_df['Player'].str.replace('*', '')
all_cornerback_stats_df['Player'] = all_cornerback_stats_df['Player'].str.replace('+', '')



# change year values to int(value) to merge with all_player_numbers_df
all_kicker_stats_df['Year'] = all_kicker_stats_df['Year'].astype(int)
all_receiver_stats_df['Year'] = all_receiver_stats_df['Year'].astype(int)
all_quarterback_stats_df['Year'] = all_quarterback_stats_df['Year'].astype(int)
all_cornerback_stats_df['Year'] = all_cornerback_stats_df['Year'].astype(int)

# merge: add player_number column to all positional DFs
all_kicker_stats_df = pd.merge(all_kicker_stats_df, all_player_numbers_df, on=['Year', 'Player'])
all_receiver_stats_df = pd.merge(all_receiver_stats_df, all_player_numbers_df, on=['Year', 'Player'])
all_quarterback_stats_df = pd.merge(all_quarterback_stats_df, all_player_numbers_df, on=['Year', 'Player'])
all_cornerback_stats_df = pd.merge(all_cornerback_stats_df, all_player_numbers_df, on=['Year', 'Player'])



# rename columns
all_kicker_stats_df.rename(columns={'Year':'STP_year', 'Player':'Name', 'FG%':'FG_percentage', 'Lng':'Longest_FG_made'}, inplace=True)
all_receiver_stats_df.rename(columns={'Year':'OFF_year', 'Player':'Name', 'TD':'Touchdowns', 'Rec':'Receptions', 'Yds':'Yards'}, inplace=True)
all_quarterback_stats_df.rename(columns={'Year':'OFF_year', 'Player':'Name', 'TD':'Touchdowns', 'Int':'Interceptions'}, inplace=True)
all_cornerback_stats_df.rename(columns={'Year':'DEF_year', 'Player':'Name', 'Int':'Interceptions', 'FF':'Forced_fumbles', 'PD':'Pass_defended'}, inplace=True)

# restructure columns
all_kicker_stats_df = all_kicker_stats_df[['STP_year', 'Name', 'Player_number', 'FG_percentage', 'Longest_FG_made']]
all_receiver_stats_df = all_receiver_stats_df[['OFF_year', 'Name', 'Player_number', 'Touchdowns', 'Receptions', 'Yards']]
all_quarterback_stats_df = all_quarterback_stats_df[['OFF_year', 'Name', 'Player_number', 'Touchdowns', 'Interceptions']]
all_cornerback_stats_df = all_cornerback_stats_df[['DEF_year', 'Name', 'Player_number', 'Interceptions', 'Forced_fumbles', 'Pass_defended']]



# console log all tables
print(all_kicker_stats_df)
print(all_receiver_stats_df)
print(all_quarterback_stats_df)
print(all_cornerback_stats_df)



# save files to CSVs
all_kicker_stats_df.to_csv("F:\\475\\csv_files\\sea_all_kicker_stats.csv", index=False)
all_receiver_stats_df.to_csv("F:\\475\\csv_files\\sea_all_receiver_stats.csv", index=False)
all_quarterback_stats_df.to_csv("F:\\475\\csv_files\\sea_all_quarterback_stats.csv", index=False)
all_cornerback_stats_df.to_csv("F:\\475\\csv_files\\sea_all_cornerback_stats.csv", index=False)
