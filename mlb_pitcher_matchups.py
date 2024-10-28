import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

# URL of the website to scrape
url = "https://www.mlb.com/probable-pitchers/2024-10-09"

# Make a request to the website
response = requests.get(url)
response.raise_for_status()  # Check if the request was successful

# Parse the HTML content of the page
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the matchup div elements
matchups = soup.find_all('div', class_='probable-pitchers__matchup')

# Prepare data for CSV and Excel
data = []
header = ['Away Team', 'Away Pitcher', 'Home Team', 'Home Pitcher']


def replace_team_name(name):
    return name.replace("D-backs", "Diamondbacks")


# Iterate over each matchup and extract the required information
for matchup in matchups:
    away_team = matchup.find('span', class_='probable-pitchers__team-name probable-pitchers__team-name--away').text.strip()
    home_team = matchup.find('span', class_='probable-pitchers__team-name probable-pitchers__team-name--home').text.strip()

    home_team = replace_team_name(home_team)
    away_team = replace_team_name(away_team)

    pitcher_summaries = matchup.find_all('div', class_='probable-pitchers__pitcher-summary')

    # Check if the away pitcher element exists
    away_pitcher_element = pitcher_summaries[0].find('a', class_='probable-pitchers__pitcher-name-link')
    away_pitcher = away_pitcher_element.text.strip() if away_pitcher_element else "TBD"

    # Check if the home pitcher element exists
    home_pitcher_element = pitcher_summaries[1].find('a', class_='probable-pitchers__pitcher-name-link')
    home_pitcher = home_pitcher_element.text.strip() if home_pitcher_element else "TBD"

    # Append data
    data.append({
        'Away Team': away_team,
        'Away Pitcher': away_pitcher,
        'Home Team': home_team,
        'Home Pitcher': home_pitcher
    })

# Function to save data to CSV
def save_to_csv(filename, data):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

# # Function to save data to Excel
# def save_to_excel(filename, data):
#     df = pd.DataFrame(data)
#     df.to_excel(filename, index=False, columns=header)  # Set column order explicitly

def main():
    # Save data to CSV and Excel files
    save_to_csv('mlb_pitcher_matchups.csv', data)
    print("Data written to mlb_pitcher_matchups.csv")

if __name__ == '__main__':
    main()
