import csv
import pandas as pd
import unicodedata
import requests
from bs4 import BeautifulSoup
import random

# Read the hitters_hot_update_first.csv file
batter_matchups_data = pd.read_csv('mlb_batter_hit_data_a.csv')

pa_batter_spot = {
    1: 4.65,
    2: 4.55,
    3: 4.43,
    4: 4.33,
    5: 4.24,
    6: 4.13,
    7: 4.01,
    8: 3.90,
    9: 3.77
}

def main():
    # Collecting data into a list
    data_rows = []

    # Process each row in hitters_hot_update_first.csv
    for index, row in batter_matchups_data.iterrows():
        batter_name = row['Batter']
        batter_spot = row['Batter Spot']
        batter_pitcher_h_pa = row['Batter Pitcher Matchup H/PA']
        pitcher_innings = row['P Pitching Outs']
        batter_team_h_pa = row['Batter Team Matchup H/PA']
        team_innings = row['T Pitching Outs']
        if not pd.isna(batter_spot):
            batter_spot = int(batter_spot)


        pas_batter_spot = pa_batter_spot.get(batter_spot, 0)

        batter_pitcher_h = batter_pitcher_h_pa * pas_batter_spot * pitcher_innings / 9
        batter_team_h = batter_team_h_pa * pas_batter_spot * team_innings / 9

        batter_matchup_h = batter_pitcher_h + batter_team_h


        batter_pitcher_h = round(batter_pitcher_h, 2)
        batter_team_h = round(batter_team_h, 2)
        batter_matchup_h = round(batter_matchup_h, 2)

        data_rows.append([
            batter_name,
            batter_spot,
            batter_pitcher_h,
            batter_team_h,
            batter_matchup_h
        ])

    # Writing collected data to a CSV file
    with open('mlb_batter_hit_data_b.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([
            'Batter', 'Batter Spot',
            'Batter Pitcher xH', 'Batter Team xH', 'Batter xH'
        ])
        csv_writer.writerows(data_rows)

if __name__ == '__main__':
    main()
