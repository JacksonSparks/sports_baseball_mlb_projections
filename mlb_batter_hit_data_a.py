import pandas as pd

def main():
    # Load the CSV files into DataFrames
    batter_pitcher_df = pd.read_csv('mlb_battervpitcher_hth_data_e.csv')
    batter_team_df = pd.read_csv('mlb_battervteam_hth_data_g.csv')

    # Merge the DataFrames on the "Batter" column
    merged_df = pd.merge(batter_pitcher_df[['Batter', 'Batter Spot', 'Batter Pitcher Matchup H/PA', 'P Pitching Outs']],
                         batter_team_df[['Batter', 'Batter Team Matchup H/PA', 'T Pitching Outs']],
                         on='Batter')

    # Save the merged DataFrame to mlb_battervpitcher_hth_data.csv
    merged_df.to_csv('mlb_batter_hit_data_a.csv', index=False)

    print("mlb_battervpitcher_hth_data.csv has been created successfully.")

if __name__ == "__main__":
    main()
