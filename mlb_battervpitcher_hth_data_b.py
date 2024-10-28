import csv
import pandas as pd
import unicodedata
import requests
from bs4 import BeautifulSoup
import random

# Read the hitters_hot_update_first.csv file
hits_data = pd.read_csv('mlb_battervpitcher_hth_data_a.csv')

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
                                season_tr = tr_elements[0]

                                left_tr = tr_elements[1]
                                right_tr = tr_elements[2]

                                season_ab = season_tr.find_all('td')[0].text.strip()
                                season_bb = season_tr.find_all('td')[7].text.strip()
                                season_hbp = season_tr.find_all('td')[8].text.strip()
                                season_h = season_tr.find_all('td')[2].text.strip()
                                season_ab = float(season_ab)
                                season_bb = float(season_bb)
                                season_hbp = float(season_hbp)
                                season_ab += season_bb + season_hbp

                                left_ab = left_tr.find_all('td')[0].text.strip()
                                left_bb = left_tr.find_all('td')[7].text.strip()
                                left_hbp = left_tr.find_all('td')[8].text.strip()
                                left_h = left_tr.find_all('td')[2].text.strip()
                                left_ab = float(left_ab)
                                left_bb = float(left_bb)
                                left_hbp = float(left_hbp)
                                left_ab += left_bb + left_hbp

                                right_ab = right_tr.find_all('td')[0].text.strip()
                                right_bb = right_tr.find_all('td')[7].text.strip()
                                right_hbp = right_tr.find_all('td')[8].text.strip()
                                right_h = right_tr.find_all('td')[2].text.strip()
                                right_ab = float(right_ab)
                                right_bb = float(right_bb)
                                right_hbp = float(right_hbp)
                                right_ab += right_bb + right_hbp

                                home_tr = tr_elements[3]
                                away_tr = tr_elements[4]

                                home_ab = home_tr.find_all('td')[0].text.strip()
                                home_bb = home_tr.find_all('td')[7].text.strip()
                                home_hbp = home_tr.find_all('td')[8].text.strip()
                                home_h = home_tr.find_all('td')[2].text.strip()
                                home_ab = float(home_ab)
                                home_bb = float(home_bb)
                                home_hbp = float(home_hbp)
                                home_ab += home_bb + home_hbp

                                away_ab = away_tr.find_all('td')[0].text.strip()
                                away_bb = away_tr.find_all('td')[7].text.strip()
                                away_hbp = away_tr.find_all('td')[8].text.strip()
                                away_h = away_tr.find_all('td')[2].text.strip()
                                away_ab = float(away_ab)
                                away_bb = float(away_bb)
                                away_hbp = float(away_hbp)
                                away_ab += away_bb + away_hbp


                                # return [left_ab, left_so, right_ab, right_so, home_ab, home_so, away_ab, away_so, season_ab, season_so]


                                header_div = soup.find('div', class_='ResponsiveWrapper')
                                if header_div:
                                    header_div_left = header_div.find('div', class_='PlayerHeader__Left flex items-center justify-start overflow-hidden brdr-clr-gray-09')
                                    if header_div_left:
                                        bio_div = header_div_left.find('div', class_='PlayerHeader__Bio pv5')
                                        if bio_div:
                                            bio_div_list = bio_div.find('ul', class_='PlayerHeader__Bio_List flex flex-column list clr-gray-04')
                                            if bio_div_list:
                                                arm = bio_div_list.find_all('li')[2]
                                                if arm:
                                                    arm_inner = arm.find('div', class_='fw-medium clr-black')
                                                    if arm_inner:
                                                        arm_inner_div = arm_inner.find('div').text.strip()
                                                        if arm_inner_div:
                                                            batting_orientation = arm_inner_div.split('/')[0].strip()
                                #                             print('got batting_orientation')
                                #                         else:
                                #                             print('no arm_inner_div')
                                #                     else:
                                #                         print('no arm_inner')
                                #                 else:
                                #                     print('no arm')
                                #             else:
                                #                 print('no bio_div_list')
                                #         else:
                                #             print('no bio_div')
                                #     else:
                                #         print('no header_div_left')
                                # else:
                                #     print('no header_div')
                                #                             return [left_ab, left_so, right_ab, right_so, home_ab, home_so, away_ab, away_so, season_ab, season_so, batting_orientation]

                                return [left_ab, left_h, right_ab, right_h, home_ab, home_h, away_ab, away_h, season_ab, season_h, batting_orientation]

        return ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']  # Return default values if no match is found
    except requests.RequestException as e:
        print(f"Failed to fetch URL: {url}, Error: {e}")
        return ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']

def main():
    # Collecting data into a list
    data_rows = []

    # Process each row in hitters_hot_update_first.csv
    for index, row in hits_data.iterrows():
        batter_name = row['Batter']
        opposing_pitcher = row['Opposing Pitcher']
        pitcher_throw = row['Throw']
        batter_location = row['Batter Location']
        batter_spot = row['Batter Spot']
        against_pa = row['B Against PA']
        against_h = row['B Against H']
        pitcher_season_pa = row['Season PA']
        pitcher_season_h = row['Season H']
        pitcher_location_ip = row['Location IP']
        pitcher_location_h = row['Location H']
        pitcher_location_bb = row['Location BB']
        pitcher_right_pa = row['Right PA']
        pitcher_right_h = row['Right H']
        pitcher_left_pa = row['Left PA']
        pitcher_left_h = row['Left H']
        pitcher_recent_ip = row['Recent IP']
        pitcher_recent_h = row['Recent H']
        pitcher_recent_bb = row['Recent BB']
        if not pd.isna(batter_spot):
            batter_spot = int(batter_spot)

        # Find player link and fetch their splits table
        link = find_player_link(batter_name)
        print(f"Player: {batter_name}, Link: {link}")
        if link:
            stats = fetch_batter_vs_pitcher_table(link)
        else:
            stats = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']  # Default values if link not found

        batter_left_pa, batter_left_h, batter_right_pa, batter_right_h, batter_home_pa, batter_home_h, batter_away_pa, batter_away_h, batter_season_pa, batter_season_h, batting_orientation = stats

        # Determine Throw AB and Throw AVG based on pitcher_throw
        batter_throw_pa = batter_left_pa if pitcher_throw == 'Left' else batter_right_pa
        batter_throw_h = batter_left_h if pitcher_throw == 'Left' else batter_right_h


        # Determine Location AB and Location AVG based on batter_location
        batter_location_pa = batter_home_pa if batter_location == 'Home' else batter_away_pa
        batter_location_h = batter_home_h if batter_location == 'Home' else batter_away_h

        if batting_orientation == 'Left':
            pitcher_throw_pa = pitcher_left_pa
            pitcher_throw_h = pitcher_left_h
        elif batting_orientation == 'Right':
            pitcher_throw_pa = pitcher_right_pa
            pitcher_throw_h = pitcher_right_h
        else:
            pitcher_throw_pa = pitcher_season_pa
            pitcher_throw_h = pitcher_season_h



        pitcher_location_pa = (int(pitcher_location_ip * 3)) + pitcher_location_h + pitcher_location_bb
        pitcher_recent_pa = (int(pitcher_recent_ip * 3)) + pitcher_recent_h + pitcher_recent_bb


        data_rows.append([
            batter_name,
            opposing_pitcher,
            pitcher_throw,
            batter_location,
            batter_spot,
            batting_orientation,
            against_pa,
            against_h,
            batter_throw_pa,
            batter_throw_h,
            batter_location_pa,
            batter_location_h,
            batter_season_pa,
            batter_season_h,
            pitcher_season_pa,
            pitcher_season_h,
            pitcher_location_pa,
            pitcher_location_h,
            pitcher_throw_pa,
            pitcher_throw_h,
            pitcher_recent_pa,
            pitcher_recent_h
        ])

    # Writing collected data to a CSV file
    with open('mlb_battervpitcher_hth_data_b.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([
            'Batter', 'Opposing Pitcher', 'Throw', 'Batter Location', 'Batter Spot', 'Batting Orientation',
            'B Against PA', 'B Against H',
            'B Throw PA', 'B Throw H',
            'B Location PA', 'B Location H',
            'B Season PA', 'B Season H',
            'P Season PA', 'P Season H',
            'P Location PA', 'P Location H',
            'P Throw PA', 'P Throw H',
            'P Recent PA', 'P Recent H'
        ])
        csv_writer.writerows(data_rows)

if __name__ == '__main__':
    main()
