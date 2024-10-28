import csv
import pandas as pd
import unicodedata
import requests
from bs4 import BeautifulSoup
import random

# Read the hitters_hot_update_first.csv file
batter_team_matchups_data = pd.read_csv('mlb_battervpitcher_hth_data_d.csv')


def main():
    # Collecting data into a list
    data_rows = []

    # Process each row in hitters_hot_update_first.csv
    for index, row in batter_team_matchups_data.iterrows():
        batter_name = row['Batter']
        opposing_pitcher = row['Opposing Pitcher']
        throw = row['Throw']
        batter_location = row['Batter Location']
        batter_spot = row['Batter Spot']
        batting_orientation = row['Batting Orientation']

        against_pa = row['B Against PA']
        against_h = row['B Against H']
        throw_pa = row['B Throw PA']
        throw_h = row['B Throw H']
        location_pa = row['B Location PA']
        location_h = row['B Location H']
        season_pa = row['B Season PA']
        season_h = row['B Season H']
        recent_pa = row['B Recent PA']
        recent_h = row['B Recent H']

        pitcher_recent_pa = row['P Recent PA']
        pitcher_recent_h = row['P Recent H']
        pitcher_throw_pa = row['P Throw PA']
        pitcher_throw_h = row['P Throw H']
        pitcher_local_pa = row['P Location PA']
        pitcher_local_h = row['P Location H']
        pitcher_season_pa = row['P Season PA']
        pitcher_season_h = row['P Season H']
        pitching_outs = row['Pitching Outs']
        if not pd.isna(batter_spot):
            batter_spot = int(batter_spot)

        pitcher_pitching_outs = (pitching_outs / 3)

        pitcher_recent_h_pa = pitcher_recent_h / pitcher_recent_pa
        pitcher_season_h_pa = pitcher_season_h / pitcher_season_pa
        pitcher_throw_h_pa = pitcher_throw_h / pitcher_throw_pa
        pitcher_local_h_pa = pitcher_local_h / pitcher_local_pa

        pitcher_h_pa = pitcher_throw_h_pa * 0.4 + pitcher_recent_h_pa * 0.4 + pitcher_local_h_pa * 0.2


        batter_recent_h_pa = recent_h / recent_pa
        batter_season_h_pa = season_h / season_pa
        batter_local_h_pa = location_h / location_pa
        batter_throw_h_pa = throw_h / throw_pa


        if recent_pa > 0:
            batter_h_pa = batter_throw_h_pa * 0.4 + batter_local_h_pa * 0.2 + batter_recent_h_pa * 0.4
        else:
            batter_h_pa = batter_throw_h_pa * 0.5 + batter_local_h_pa * 0.3 + batter_season_h_pa * 0.2


        if against_pa > 0:
            against_h_pa = against_h / against_pa
            against_weight = against_pa / (against_pa + 160)
        else:
            against_weight = 0
            against_h_pa = 0

        batter_pitcher_matchup_h_pa = ((against_h_pa * against_weight) +
                                    (batter_h_pa * (0.5 - (against_weight / 2))) +
                                    (pitcher_h_pa * (0.5 - (against_weight / 2))))

        batter_h_pa = round(batter_h_pa, 2)
        pitcher_h_pa = round(pitcher_h_pa, 2)
        against_h_pa = round(against_h_pa, 2)
        batter_pitcher_matchup_h_pa = round(batter_pitcher_matchup_h_pa, 2)
        pitcher_pitching_outs = round(pitcher_pitching_outs, 2)







        data_rows.append([
            batter_name,
            opposing_pitcher,
            throw,
            batter_location,
            batter_spot,
            batting_orientation,
            pitcher_pitching_outs,
            batter_h_pa,
            pitcher_h_pa,
            against_h_pa,
            batter_pitcher_matchup_h_pa
        ])

    # Writing collected data to a CSV file
    with open('mlb_battervpitcher_hth_data_e.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([
            'Batter', 'Opposing Pitcher', 'Throw', 'Batter Location', 'Batter Spot', 'Batting Orientation', 'P Pitching Outs',
            'Batter H/PA', 'Pitcher H/PA', 'Against H/PA', 'Batter Pitcher Matchup H/PA'
        ])
        csv_writer.writerows(data_rows)

if __name__ == '__main__':
    main()
