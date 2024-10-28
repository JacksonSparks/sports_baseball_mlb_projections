import pandas as pd

def merge_batter_team_matchups():
    # Load the CSV files into DataFrames
    team_matchups_df = pd.read_csv('mlb_battervteam_hth_data_e.csv')
    pitcher_matchups_df = pd.read_csv('mlb_battervpitcher_hth_data_d.csv')

    # Merge the DataFrames on the "Batter" column
    merged_df = team_matchups_df.merge(pitcher_matchups_df[['Batter', 'Pitching Outs']],
                                       on='Batter',
                                       how='left')

    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv('mlb_battervteam_hth_data_f.csv', index=False)

def main():
    merge_batter_team_matchups()
    print("The CSV files have been successfully merged and saved as 'mlb_battervteam_hth_data_f.csv'.")

if __name__ == "__main__":
    main()
