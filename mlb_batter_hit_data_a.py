import pandas as pd

def main():
    # Load the CSV files into DataFrames
    batter_pitcher_df = pd.read_csv('batter_pitcher_matchups_e.csv')
    batter_team_df = pd.read_csv('batter_team_matchups_g.csv')

    # Merge the DataFrames on the "Batter" column
    merged_df = pd.merge(batter_pitcher_df[['Batter', 'Batter Spot', 'Batter Pitcher Matchup H/PA', 'P Pitching Outs']],
                         batter_team_df[['Batter', 'Batter Team Matchup H/PA', 'T Pitching Outs']],
                         on='Batter')

    # Save the merged DataFrame to batter_h_matchups.csv
    merged_df.to_csv('batter_h_matchups_a.csv', index=False)

    print("batter_h_matchups.csv has been created successfully.")

if __name__ == "__main__":
    main()
