import pandas as pd

def merge_csv_files():
    # Load the CSV files into DataFrames
    matchups_df = pd.read_csv('batter_pitcher_matchups_c.csv')
    outs_df = pd.read_csv('batter_h_pitching_outs.csv')

    # Merge the DataFrames on the condition where "Opposing Pitcher" matches "Player Name"
    merged_df = matchups_df.merge(outs_df[['Player Name', 'Pitching Outs']],
                                  left_on='Opposing Pitcher',
                                  right_on='Player Name',
                                  how='left')

    # Drop the "Player Name" column since it's redundant after merging
    merged_df.drop(columns=['Player Name'], inplace=True)

    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv('batter_pitcher_matchups_d.csv', index=False)

def main():
    merge_csv_files()
    print("The CSV files have been successfully merged and saved as 'batter_pitcher_matchups_d.csv'.")

if __name__ == "__main__":
    main()
