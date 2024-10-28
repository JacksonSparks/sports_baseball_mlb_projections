import pandas as pd

def main():
    # Step 1: Read the CSV files
    df1 = pd.read_csv('mlb_battervteam_hth_data_b.csv')
    df2 = pd.read_csv('mlb_battervpitcher_hth_data_c.csv')

    # Step 2: Drop the duplicate columns from df2 except 'Batter'
    df2 = df2.drop(columns=[col for col in df2.columns if col != 'Batter' and col in df1.columns])

    # Step 3: Merge the DataFrames on the 'Batter' column
    merged_df = pd.merge(df1, df2, on='Batter', how='inner')

    # Step 4: Save the merged DataFrame to a new CSV file
    merged_df.to_csv('mlb_battervteam_hth_data_c.csv', index=False)

    # Print a message to indicate the process is complete
    print("Merged CSV file 'mlb_battervteam_hth_data_c.csv' has been created successfully.")

if __name__ == "__main__":
    main()
