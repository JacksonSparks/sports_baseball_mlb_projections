import csv
import pandas as pd
import unicodedata
import requests
from bs4 import BeautifulSoup
import random

# Read the hitters_hot_update_first.csv file
batter_team_matchups_data = pd.read_csv('batter_team_matchups_f.csv')


def main():
    # Collecting data into a list
    data_rows = []

    # Process each row in hitters_hot_update_first.csv
    for index, row in batter_team_matchups_data.iterrows():
        batter_name = row['Batter']
        opposing_team = row['Opposing Team']
        batter_location = row['Batter Location']
        batter_spot = row['Batter Spot']
        batting_orientation = row['Batting Orientation']

        against_pa = row['Against PA']
        against_h = row['Against H']
        location_pa = row['Location PA']
        location_h = row['Location H']
        season_pa = row['Season PA']
        season_h = row['Season H']
        recent_pa = row['Recent PA']
        recent_h = row['Recent H']
        team_recent_pa = row['T Recent PA']
        team_recent_h = row['T Recent H']
        team_throw_pa = row['T Throw PA']
        team_throw_h = row['T Throw H']
        team_local_pa = row['T Local PA']
        team_local_h = row['T Local H']
        pitching_outs = row['Pitching Outs']
        if not pd.isna(batter_spot):
            batter_spot = int(batter_spot)

        team_pitching_outs = 9 - (pitching_outs / 3)

        team_recent_h_pa = team_recent_h / team_recent_pa
        team_throw_h_pa = team_throw_h / team_throw_pa
        team_local_h_pa = team_local_h / team_local_pa

        team_h_pa = team_throw_h_pa * 0.4 + team_recent_h_pa * 0.4 + team_local_h_pa * 0.2


        batter_recent_h_pa = recent_h / recent_pa
        batter_season_h_pa = season_h / season_pa
        batter_local_h_pa = location_h / location_pa

        if recent_pa > 0:
            batter_h_pa = batter_local_h_pa * 0.4 + batter_season_h_pa * 0.2 + batter_recent_h_pa * 0.4
        else:
            batter_h_pa = batter_local_h_pa * 0.6 + batter_season_h_pa * 0.4


        if against_pa > 0:
            against_h_pa = against_h / against_pa
            against_weight = against_pa / (against_pa + 280)
        else:
            against_weight = 0
            against_h_pa = 0

        batter_team_matchup_h_pa = ((against_h_pa * against_weight) +
                                    (batter_h_pa * (0.5 - (against_weight / 2))) +
                                    (team_h_pa * (0.5 - (against_weight / 2))))

        batter_h_pa = round(batter_h_pa, 2)
        team_h_pa = round(team_h_pa, 2)
        against_h_pa = round(against_h_pa, 2)
        batter_team_matchup_h_pa = round(batter_team_matchup_h_pa, 2)
        team_pitching_outs = round(team_pitching_outs, 2)







        data_rows.append([
            batter_name,
            opposing_team,
            batter_location,
            batter_spot,
            batting_orientation,
            team_pitching_outs,
            batter_h_pa,
            team_h_pa,
            against_h_pa,
            batter_team_matchup_h_pa
        ])

    # Writing collected data to a CSV file
    with open('batter_team_matchups_g.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([
            'Batter', 'Opposing Team', 'Batter Location', 'Batter Spot', 'Batting Orientation', 'T Pitching Outs',
            'Batter H/PA', 'Team H/PA', 'Against H/PA', 'Batter Team Matchup H/PA'
        ])
        csv_writer.writerows(data_rows)

if __name__ == '__main__':
    main()
