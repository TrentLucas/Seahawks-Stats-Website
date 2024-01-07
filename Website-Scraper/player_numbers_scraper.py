# Website Scraper for Team Data 
# Used to get player_number data for player_stats_scraper.py
# 
# Pulls data from URL, converts the data to be ready for merge with positonal tables, and exports to a CSV file
# Sleep times needed to not overload websites the scraper reads from
#
#         ***ALL CODE TO BE USED TO VIEWING PURPOSES ONLY. NO REUSING CODE FROM PROJECT***
##########################################################################################################

import pandas as pd
import random
import time
import re


# function to scrape all player_numbers
def scrape_player_numbers(url):
    
    # initialize DF
    all_player_numbers_df_final = pd.DataFrame()
    
    # add missing source data 
    all_player_numbers_df = pd.DataFrame([{'Player_number' : 2, 'Name' : 'Drew Lock', 'Years' : '2022-2023'},
                                {'Player_number' : 16, 'Name' : 'Tyler Lockett', 'Years' : '2015-2023'},
                                {'Player_number' : 82, 'Name' : 'Amara Darboh', 'Years' : '2017'}])
    
    
    
    # read data from each table in webpage
    for i in range(99):
        
        # read 'i' table
        player_numbers_df = pd.read_html(url)[i]
        
        # add player_number for table
        player_numbers_df['Player_number'] = i + 1
        
        # concat to output table
        all_player_numbers_df = pd.concat([all_player_numbers_df, player_numbers_df])
        
        time.sleep(random.randint(4, 5))
        
        
        
    # edit incorrect values from data    
    all_player_numbers_df.loc[all_player_numbers_df['Name'] == 'Autry Beamon', 'Years'] = '1977-1979'
    all_player_numbers_df.loc[all_player_numbers_df['Name'] == 'Ahman Green', 'Years'] = '1998-1999'
    all_player_numbers_df.loc[all_player_numbers_df['Name'] == 'Joe Norman', 'Years'] = '1979-1981, 1983'
    all_player_numbers_df.loc[all_player_numbers_df['Name'] == 'Bill Sandifer', 'Years'] = '1977-1978'
    all_player_numbers_df.loc[all_player_numbers_df['Name'] == 'Tony Berti', 'Years'] = '1998'
    all_player_numbers_df.loc[all_player_numbers_df['Name'] == 'Carlester Crumpler', 'Years'] = '1995-1998'
    all_player_numbers_df.loc[all_player_numbers_df['Name'] == 'Kevin Pierre-Louis', 'Years'] = '2014-2016'
    all_player_numbers_df.loc[all_player_numbers_df['Name'] == 'Steven Hauschka', 'Name'] = 'Stephen Hauschka'
    
    
    
    # remove multivalued attribute: years
    for index, row in all_player_numbers_df.iterrows():
        
        if pd.notna(row['Years']):
            terms = re.split('[,;]', row['Years'])
            
            for term in terms:
                startEnd = term.split('-')
                startEnd[0] = int(startEnd[0])
                
                if len(startEnd) > 1:
                    
                    if startEnd[1] == '':
                        startEnd[1] = 2023
                        
                    startEnd[1] = int(startEnd[1])
                    for i in range(startEnd[0], startEnd[1] + 1):
                        entry = pd.Series({'Player_number' : row['Player_number'], 'Name' : row['Name'], 'Years' : i})
                        entry.name = None
                        all_player_numbers_df_final = pd.concat([all_player_numbers_df_final, entry.to_frame().T], ignore_index=True)
                else:
                    entry = pd.Series({'Player_number' : row['Player_number'], 'Name' : row['Name'], 'Years' : startEnd[0]})
                    entry.name = None
                    all_player_numbers_df_final = pd.concat([all_player_numbers_df_final, entry.to_frame().T], ignore_index=True)
                
                
    # remove unneccessary tuple
    index_to_remove = all_player_numbers_df_final[all_player_numbers_df_final['Name'] == 'Jim Zorn*'].index
    all_player_numbers_df_final.drop(index_to_remove, inplace=True)
    
    
    
    return(all_player_numbers_df_final)





# use player_number scrape function
url = 'https://www.seahawks.com/team/players-roster/all-time'
result_df = scrape_player_numbers(url)



# console log table
print(result_df)



#save files to CSVs
result_df.to_csv("F:\\475\\csv_files\\sea_all_players.csv", index=False)