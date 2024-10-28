import csv
import pandas as pd
import unicodedata
import requests
from bs4 import BeautifulSoup
import random

# Read the cold_hitters_data_update.csv file
cold_hitters_data = pd.read_csv('mlb_battervpitcher_hth_data_update.csv')

# Read the mlb_links_players.csv file
player_links_data = pd.read_csv('mlb_links_players.csv')

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

def find_player_link(player_name):
    formatted_name = format_name(player_name).replace(' ', '-').lower()
    print(f"Formatted name to find: {formatted_name}")

    for _, player_row in player_links_data.iterrows():
        player_row_name = format_name(player_row['Player Name']).replace(' ', '-').lower()
        print(f"Checking against: {player_row_name}")

        if player_row_name == formatted_name:
            base_link = player_row['Player Link']
            print(f"Match found. Base link: {base_link}")

            # Split the link into base and ID parts
            try:
                base_part, id_part = base_link.split('_/id/')
            except ValueError as e:
                print(f"Error splitting link: {base_link}")
                print(f"Exception: {e}")
                continue

            # Construct the new URL
            new_url = f"{base_part}/splits/_/id/{id_part}/{formatted_name}"

            # Print the constructed URL for debugging
            print(f"Constructed URL: {new_url}")

            return new_url

    print(f"No link found for player: {player_name}")
    return None


# Function to fetch and parse the HTML content of a URL
def fetch_gamelog_table(url):
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
            table_div = soup.find('div', class_='ResponsiveTable ResponsiveTable--fixed-left player-splits-table')
            if table_div:
                scroller_div = table_div.find('div', class_='Table__ScrollerWrapper relative overflow-hidden')
                if scroller_div:
                    table = scroller_div.find('table', class_='Table Table--align-right')
                    if table:
                        tbody = table.find('tbody', class_='Table__TBODY')
                        if tbody:
                            tr_elements = tbody.find_all('tr', class_='Table__TR Table__TR--sm Table__even')
                            if len(tr_elements) >= 5:
                                opponent_tr = tr_elements[1]

                                season_ab = opponent_tr.find_all('td')[0].text.strip()
                                season_h = opponent_tr.find_all('td')[2].text.strip()
                                season_bb = opponent_tr.find_all('td')[7].text.strip()
                                season_hbp = opponent_tr.find_all('td')[8].text.strip()
                                season_ab = float(season_ab)
                                season_hbp = float(season_hbp)
                                season_bb = float(season_bb)
                                season_pa = season_ab + season_bb + season_hbp


                                # total_tr = tr_elements[0]
                                #
                                # total_ip = total_tr.find_all('td')[8].text.strip()
                                # total_gs = total_tr.find_all('td')[6].text.strip()
                                # total_gp = total_tr.find_all('td')[5].text.strip()

                                home_tr = tr_elements[2]
                                away_tr = tr_elements[3]

                                home_ip = home_tr.find_all('td')[8].text.strip()
                                home_h = home_tr.find_all('td')[9].text.strip()
                                home_bb = home_tr.find_all('td')[13].text.strip()


                                away_ip = away_tr.find_all('td')[8].text.strip()
                                away_h = away_tr.find_all('td')[9].text.strip()
                                away_bb = away_tr.find_all('td')[13].text.strip()

                                right_tr = tr_elements[7]
                                left_tr = tr_elements[6]

                                right_ab = right_tr.find_all('td')[0].text.strip()
                                right_h = right_tr.find_all('td')[2].text.strip()
                                right_bb = right_tr.find_all('td')[7].text.strip()
                                right_hbp = right_tr.find_all('td')[8].text.strip()
                                right_ab = float(right_ab)
                                right_bb = float(right_bb)
                                right_hbp = float(right_hbp)
                                right_pa = right_ab + right_bb + right_hbp

                                left_ab = left_tr.find_all('td')[0].text.strip()
                                left_h = left_tr.find_all('td')[2].text.strip()
                                left_bb = left_tr.find_all('td')[7].text.strip()
                                left_hbp = left_tr.find_all('td')[8].text.strip()
                                left_ab = float(left_ab)
                                left_bb = float(left_bb)
                                left_hbp = float(left_hbp)
                                left_pa = left_ab + left_hbp + left_bb

                                recent_tr = tr_elements[16]
                                recent_ip = recent_tr.find_all('td')[8].text.strip()
                                recent_h = recent_tr.find_all('td')[9].text.strip()
                                recent_bb = recent_tr.find_all('td')[13].text.strip()


                                return [season_pa, season_h, home_ip, home_h, home_bb, away_ip, away_h, away_bb, right_pa, right_h, left_pa, left_h, recent_ip, recent_h, recent_bb]

            return ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']  # Return default values if no match is found
    except requests.RequestException as e:
        print(f"Failed to fetch URL: {url}, Error: {e}")
        return ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']

def main():
    # Collecting data into a list
    data_rows = []

    # Process each row in cold_hitters_data_update.csv
    for index, row in cold_hitters_data.iterrows():
        batter = row['Batter']
        opposing_pitcher = row['Opposing Pitcher']
        opposing_team = row['Opposing Team']
        throw = row['Throw']
        batter_location = row['Batter Location']
        batter_spot = row['Batter Spot']
        against_ab = row['AB']
        against_h = row['H']
        against_bb = row['BB']
        if not pd.isna(batter_spot):
            batter_spot = int(batter_spot)

        # Find player link and fetch their splits table
        link = find_player_link(opposing_pitcher)
        print(f"Player: {opposing_pitcher}, Link: {link}")
        if link:
            stats = fetch_gamelog_table(link)
        else:
            stats = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']  # Default values if link not found

        season_pa, season_h, home_ip, home_h, home_bb, away_ip, away_h, away_bb, right_pa, right_h, left_pa, left_h, recent_ip, recent_h, recent_bb = stats

        if batter_location == 'Away':
            pitcher_location_ip = home_ip
            pitcher_location_h = home_h
            pitcher_location_bb = home_bb
        elif batter_location == 'Home':
            pitcher_location_ip = away_ip
            pitcher_location_h = away_h
            pitcher_location_bb = away_bb
        else:
            pitcher_location_ip = 'N/A'
            pitcher_location_h = 'N/A'
            pitcher_location_bb = 'N/A'

        against_pa = against_ab + against_bb

        data_rows.append([
            batter,
            opposing_pitcher,
            throw,
            batter_location,
            batter_spot,
            against_pa,
            against_h,
            season_pa,
            season_h,
            pitcher_location_ip,
            pitcher_location_h,
            pitcher_location_bb,
            right_pa,
            right_h,
            left_pa,
            left_h,
            recent_ip,
            recent_h,
            recent_bb
        ])

    # Writing collected data to a CSV file
    with open('mlb_battervpitcher_hth_data_a.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([
            'Batter', 'Opposing Pitcher', 'Throw', 'Batter Location', 'Batter Spot',
            'B Against PA', 'B Against H',
            'Season PA', 'Season H',
            'Location IP', 'Location H', 'Location BB',
            'Right PA', 'Right H',
            'Left PA', 'Left H',
            'Recent IP', 'Recent H', 'Recent BB'
        ])
        csv_writer.writerows(data_rows)

if __name__ == '__main__':
    main()
