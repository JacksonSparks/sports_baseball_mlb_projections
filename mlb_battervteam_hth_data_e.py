import csv
import pandas as pd
import unicodedata
import requests
from bs4 import BeautifulSoup
import random

# Read the hitters_hot_update_first.csv file
hits_data = pd.read_csv('batter_team_matchups_d.csv')

# Read the links_players.csv file
team_links_data = pd.read_csv('links_team_pitching_splits.csv')

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

    return normalized_name

def find_player_link(team_name, batter_location):
    for _, player_row in team_links_data.iterrows():
        team_row_name = player_row['Team']
        print(f"Checking against: {team_row_name}")

        if team_row_name == team_name:
            base_link = player_row['Team Link']
            print(f"Match found. Base link: {base_link}")

            # Replace '/splits' with '/stats' in the base_link if it exists
            if '/splits' in base_link:
                base_link = base_link.replace('/splits', '/stats')

            base_part = "https://www.espn.com"


            if batter_location == 'Home':
                # Construct the new URL
                new_url = f"{base_part}{base_link}/split/34"

            if batter_location == 'Away':
                # Construct the new URL
                new_url = f"{base_part}{base_link}/split/33"

            if new_url:
                # Print the constructed URL for debugging
                print(f"Constructed URL: {new_url}")
                return new_url

    print(f"No link found for team: {team_name}")
    return None


def fetch_batter_vs_pitcher_table(url):
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
            table_div = soup.find_all('div', class_='ResponsiveTable ResponsiveTable--fixed-left mt5 remove_capitalize')[1]
            if table_div:
                flex_div = table_div.find('div', class_='flex')
                if flex_div:
                    scroller_div = flex_div.find('div', class_='Table__ScrollerWrapper relative overflow-hidden')
                    if scroller_div:
                        scroller_div_inner = scroller_div.find('div', class_='Table__Scroller')
                        if scroller_div_inner:
                            table = scroller_div_inner.find('table', class_='Table Table--align-right')
                            if table:
                                tbody = table.find('tbody', class_='Table__TBODY')
                                if tbody:
                                    tr_elements = tbody.find_all('tr', class_='Table__TR Table__TR--sm Table__even')
                                    if len(tr_elements) > 1:
                                        # Assume the last tr element is the total row you want
                                        total_tr_element = tr_elements[-1]

                                        # Extract the text from each span element within the td elements
                                        batter_stats = [td.find('span').text.strip() for td in total_tr_element.find_all('td')]

                                        return batter_stats

            return []  # Return empty list if no match is found
    except requests.RequestException as e:
        print(f"Failed to fetch URL: {url}, Error: {e}")
        return []


def main():
    # Collecting data into a list
    data_rows = []

    # Process each row in hitters_hot_update_first.csv
    for index, row in hits_data.iterrows():
        batter_name = row['Batter']
        opposing_team = row['Opposing Team']
        batter_location = row['Batter Location']
        batter_spot = row['Batter Spot']
        against_pa = row['Against PA']
        against_h = row['Against H']
        location_pa = row['Location PA']
        location_h = row['Location H']
        season_pa = row['Season PA']
        season_h = row['Season H']
        recent_pa = row['Recent PA']
        recent_h = row['Recent H']
        team_recent_pa = row['T Recent PA']
        team_recent_h = row['T Recent H']
        team_throw_pa = row['T Throw PA']
        team_throw_h = row['T Throw H']
        batting_orientation = row['Batting Orientation']
        if not pd.isna(batter_spot):
            batter_spot = int(batter_spot)





        # Find player link and fetch their splits table
        link = find_player_link(opposing_team, batter_location)
        print(f"Team: {opposing_team}, Link: {link}")
        if link:
            stats = fetch_batter_vs_pitcher_table(link)
        else:
            stats = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']  # Default values if link not found

        team_local_gp, team_local_ab, team_local_r, team_local_h, team_local_2b, team_local_3b, team_local_hr, team_local_bb, team_local_k, team_local_sb, team_local_cs, team_local_oba = stats

        team_local_ab = int(team_local_ab)
        team_local_bb = int(team_local_bb)
        team_local_pa = team_local_ab + team_local_bb

        data_rows.append([
            batter_name,
            opposing_team,
            batter_location,
            batter_spot,
            batting_orientation,
            against_pa,
            against_h,
            location_pa,
            location_h,
            season_pa,
            season_h,
            recent_pa,
            recent_h,
            team_recent_pa,
            team_recent_h,
            team_throw_pa,
            team_throw_h,
            team_local_pa,
            team_local_h
        ])

    # Writing collected data to a CSV file
    with open('batter_team_matchups_e.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([
            'Batter', 'Opposing Team', 'Batter Location', 'Batter Spot', 'Batting Orientation',
            'Against PA', 'Against H',
            'Location PA', 'Location H',
            'Season PA', 'Season H',
            'Recent PA', 'Recent H',
            'T Recent PA', 'T Recent H',
            'T Throw PA', 'T Throw H',
            'T Local PA', 'T Local H'
        ])
        csv_writer.writerows(data_rows)

if __name__ == '__main__':
    main()
