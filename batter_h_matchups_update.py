import csv
import pandas as pd
import unicodedata
import requests
from bs4 import BeautifulSoup
import random

# Read the lineups_backup.csv file
lineups_data = pd.read_csv('lineups.csv')

# Read the links_players.csv file
player_links_data = pd.read_csv('links_players.csv')

# Read the fi_pitcher_data.csv file
pitcher_data = pd.read_csv('fi_pitcher_data.csv')

# Define Teams Id Numbers
team_id_numbers = {
    'Mariners': 12,
    'Angels': 3,
    'Rangers': 13,
    'Athletics': 11,
    'Astros': 18,
    'Yankees': 10,
    'Red Sox': 2,
    'Blue Jays': 14,
    'Orioles': 1,
    'Rays': 30,
    'White Sox': 4,
    'Guardians': 5,
    'Tigers': 6,
    'Royals': 7,
    'Twins': 9,
    'Dodgers': 19,
    'Giants': 26,
    'Padres': 25,
    'Diamondbacks': 29,
    'Rockies': 27,
    'Braves': 15,
    'Mets': 21,
    'Phillies': 22,
    'Marlins': 28,
    'Nationals': 20,
    'Cubs': 16,
    'Cardinals': 24,
    'Brewers': 8,
    'Pirates': 23,
    'Reds': 17,
}

# List of User-Agent strings
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
]

def format_name(name):
    """
    Convert name from 'First Last' to 'F. Last' and handle three-word names.
    Handles special characters by normalizing to ASCII.
    """
    # Normalize the name to remove accents and other diacritics
    normalized_name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')

    # Split the normalized name into parts
    parts = normalized_name.split()

    if len(parts) == 2:
        return f"{parts[0][0]}. {parts[1]}"
    elif len(parts) == 3:
        return f"{parts[0][0]}. {parts[1]} {parts[2]}"
    return name

# Function to find player link and append the required segments
def find_player_link(abbreviated_team_name, player_name, opposing_team_name):
    formatted_name = format_name(player_name)
    for _, player_row in player_links_data.iterrows():
        full_team_name = player_row['Team']
        if abbreviated_team_name in full_team_name and format_name(player_row['Player Name']) == formatted_name:
            base_link = player_row['Player Link']
            team_id = team_id_numbers.get(opposing_team_name, "")
            if team_id:
                return f"{base_link.replace('/_/id', '/batvspitch/_/id')}/teamId/{team_id}"
            return base_link
    return None

# Function to fetch and parse the HTML content of a URL
def fetch_batter_vs_pitcher_table(url, opposing_pitcher_name):
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/',
        'Connection': 'keep-alive',
    }

    try:
        with requests.Session() as session:
            session.headers.update(headers)
            response = session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            table_div = soup.find('div', class_='ResponsiveTable pt4 bat-pitch')
            if table_div:
                table = table_div.find('table', class_='Table Table--align-right')
                if table:
                    tbody = table.find('tbody', class_='Table__TBODY')
                    if tbody:
                        tr_elements = tbody.find_all('tr', class_='Table__TR Table__TR--sm Table__even')
                        batter_stats = []
                        for tr in tr_elements:
                            td_elements = tr.find_all('td')
                            if len(td_elements) >= 13:
                                a = td_elements[0].find('a', class_='AnchorLink')
                                if a:
                                    formatted_pitcher_name = format_name(a.text.strip())
                                    if formatted_pitcher_name == format_name(opposing_pitcher_name):
                                        batter_stats.append([td.text.strip() for td in td_elements[1:14]])
                                else:
                                    print("AnchorLink not found in td element.")
                            else:
                                print(f"Expected 13 td elements, but found {len(td_elements)} in tr element.")
                        return batter_stats
                    else:
                        print(f"Could not find tbody inside {url}")
                else:
                    print(f"Could not find table inside {url}")
            else:
                print(f"Could not find table div inside {url}")

            return []  # Return empty list if no match is found
    except requests.RequestException as e:
        print(f"Failed to fetch URL: {url}, Error: {e}")
        return []

def main():
    # Read the batter_h_matchups.csv file
    data = pd.read_csv('batter_h_matchups.csv')

    # Add the 'Throw' column based on the 'Opposing Pitcher' column
    data['Throw'] = data['Opposing Pitcher'].apply(lambda x: pitcher_data[pitcher_data['Name'].apply(
        lambda name: unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
    ) == unicodedata.normalize('NFKD', x).encode('ASCII', 'ignore').decode('ASCII')]['Throw'].values[0] if not pitcher_data[pitcher_data['Name'].apply(
        lambda name: unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
    ) == unicodedata.normalize('NFKD', x).encode('ASCII', 'ignore').decode('ASCII')].empty else 'N/A')

    # Calculate XBH and replace "2B", "3B", and "HR" columns
    data['XBH'] = data['2B'] + data['3B'] + data['HR']
    data = data.drop(columns=['2B', '3B', 'HR'])

    # Reorder columns so that XBH appears after H
    data = data[['Batter', 'Opposing Pitcher', 'Opposing Team', 'Throw', 'Batter Location', 'Batter Spot', 'AB', 'H', 'XBH', 'RBI', 'BB', 'K', 'AVG', 'OBP', 'SLG', 'OPS']]

    # Write the modified data to a new CSV file
    data.to_csv('batter_h_matchups_update.csv', index=False)

if __name__ == '__main__':
    main()
