import pandas as pd

def main():
    # Load the first CSV file
    pitcher_matchups = pd.read_csv('batter_pitcher_matchups_b.csv')

    # Load the second CSV file
    batter_matchups = pd.read_csv('batter_h_recent.csv')

    # Merge the dataframes on the "Batter" column from the first file and the "Player Name" column from the second file
    merged_data = pd.merge(pitcher_matchups, batter_matchups, left_on='Batter', right_on='Player Name', how='left')

    # Drop the "Player Name" column as it's redundant now
    merged_data = merged_data.drop(columns=['Player Name'])

    # Save the merged dataframe to a new CSV file
    merged_data.to_csv('batter_pitcher_matchups_c.csv', index=False)

if __name__ == "__main__":
    main()
