import csv
import pandas as pd
import unicodedata
import requests
from bs4 import BeautifulSoup
import random

# Read the lineups_backup.csv file
lineups_data = pd.read_csv('mlb_lineups.csv')

# Read the mlb_links_players.csv file
player_links_data = pd.read_csv('mlb_links_players.csv')

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
    elif len(parts) == 4:
        return f"{parts[0][0]}. {parts[1]} {parts[2]} {parts[3]}"
    return name

# Function to find player link and return both the full name and link
def find_player_link(abbreviated_team_name, player_name, opposing_team_name):
    formatted_name = format_name(player_name)
    for _, player_row in player_links_data.iterrows():
        full_team_name = player_row['Team']
        if abbreviated_team_name in full_team_name and format_name(player_row['Player Name']) == formatted_name:
            base_link = player_row['Player Link']
            team_id = team_id_numbers.get(opposing_team_name, "")
            if team_id:
                return player_row['Player Name'], f"{base_link.replace('/_/id', '/batvspitch/_/id')}/teamId/{team_id}"
            return player_row['Player Name'], base_link
    return player_name, None

# Function to find the full name of a pitcher given their abbreviated name
def find_pitcher_name(pitcher_name):
    for _, player_row in player_links_data.iterrows():
        if format_name(player_row['Player Name']) == pitcher_name:
            return player_row['Player Name']
    return pitcher_name

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
                        return batter_stats

            return []  # Return empty list if no match is found
    except requests.RequestException as e:
        print(f"Failed to fetch URL: {url}, Error: {e}")
        return []

def main():
    # Collecting data into a list
    data_rows = []

    # Process each row in lineups_backup.csv
    for index, row in lineups_data.iterrows():
        # Extracting Away team data
        away_team_name = row['Away Team']
        away_pitcher_name = row['Away Pitcher']
        away_pitcher_full_name = find_pitcher_name(away_pitcher_name)
        away_batters = [row[f'Away ({i})'] for i in range(1, 10)]

        # Extracting Home team data
        home_team_name = row['Home Team']
        home_pitcher_name = row['Home Pitcher']
        home_pitcher_full_name = find_pitcher_name(home_pitcher_name)
        home_batters = [row[f'Home ({i})'] for i in range(1, 10)]

        # Find links for away batters and fetch their batter vs. pitcher table
        for i, batter in enumerate(away_batters, 1):
            batter_spot = i
            full_name, link = find_player_link(away_team_name, batter, home_team_name)
            print(f"Away Batter: {full_name}, Batter Spot: {batter_spot}, Link: {link}")
            if link:
                batter_stats = fetch_batter_vs_pitcher_table(link, home_pitcher_full_name)
                if not batter_stats:
                    # If no stats found, append row with zeros
                    batter_stats = [['0'] * 12]
                for stats in batter_stats:
                    batter_location = 'Away'
                    data_rows.append([full_name, home_pitcher_full_name, home_team_name, batter_location, batter_spot] + stats)

        # Find links for home batters and fetch their batter vs. pitcher table
        for i, batter in enumerate(home_batters, 1):
            batter_spot = i
            full_name, link = find_player_link(home_team_name, batter, away_team_name)
            print(f"Home Batter: {full_name}, Batter Spot: {batter_spot}, Link: {link}")
            if link:
                batter_stats = fetch_batter_vs_pitcher_table(link, away_pitcher_full_name)
                if not batter_stats:
                    # If no stats found, append row with zeros
                    batter_stats = [['0'] * 12]
                for stats in batter_stats:
                    batter_location = 'Home'
                    data_rows.append([full_name, away_pitcher_full_name, away_team_name, batter_location, batter_spot] + stats)

    # Writing collected data to a CSV file
    with open('mlb_battervpitcher_hth_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Batter', 'Opposing Pitcher', 'Opposing Team', 'Batter Location', 'Batter Spot', 'AB', 'H', '2B', '3B', 'HR', 'RBI', 'BB', 'K', 'AVG', 'OBP', 'SLG', 'OPS'])
        csv_writer.writerows(data_rows)

if __name__ == '__main__':
    main()
