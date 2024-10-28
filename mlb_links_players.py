import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

# Read the mlb_links_teams.csv file
roster_data = pd.read_csv('mlb_links_teams.csv')

# User-Agent header to avoid getting blocked
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def remove_periods(name):
    """
    Removes all periods from the given last name.

    Parameters:
    last_name (str): The last name to be checked and modified.

    Returns:
    str: The modified last name with all periods removed.
    """
    return name.replace(".", "")

# Prepare data for CSV
data = []
header = ['Team', 'Player Name', 'Player Link']

for index, row in roster_data.iterrows():
    team_name = row['Team']
    url = f"https://www.espn.com{row['Roster Link']}"
    print(f"Scraping team: {team_name} | URL: {url}")

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    soup = BeautifulSoup(response.text, 'html.parser')

    players_container = soup.find('section', class_='Roster')

    # Find all the matchup div elements
    pitchers_container = players_container.find('div', class_='ResponsiveTable Pitchers Roster__MixedTable')
    catchers_container = players_container.find('div', class_='ResponsiveTable Catchers Roster__MixedTable')
    infielders_container = players_container.find('div', class_='ResponsiveTable Infielders Roster__MixedTable')
    outfielders_container = players_container.find('div', class_='ResponsiveTable Outfielders Roster__MixedTable')
    dhs_container = players_container.find('div', class_='ResponsiveTable Designated Hitter Roster__MixedTable')

    if pitchers_container:
        pitchers_table = pitchers_container.find('table', class_='Table')
        pitchers_items = pitchers_table.find_all('tr', class_='Table__TR Table__TR--lg Table__even')
        for pitcher_item in pitchers_items:
            pitcher_item_info = pitcher_item.find_all('td')
            pitcher_name_tab = pitcher_item_info[1].find('a', class_='AnchorLink')
            pitcher_name = pitcher_name_tab.text.strip()
            pitcher_name = remove_periods(pitcher_name)
            pitcher_link = pitcher_name_tab.get('href')
            data.append({'Team': team_name, 'Player Name': pitcher_name, 'Player Link': pitcher_link})
            print(f"Data appended: Player Name - {pitcher_name}, Player Link - {pitcher_link}")

    if catchers_container:
        catchers_table = catchers_container.find('table', class_='Table')
        catchers_items = catchers_table.find_all('tr', class_='Table__TR Table__TR--lg Table__even')
        for catcher_item in catchers_items:
            catcher_item_info = catcher_item.find_all('td')
            catcher_name_tab = catcher_item_info[1].find('a', class_='AnchorLink')
            catcher_name = catcher_name_tab.text.strip()
            catcher_name = remove_periods(catcher_name)
            catcher_link = catcher_name_tab.get('href')
            data.append({'Team': team_name, 'Player Name': catcher_name, 'Player Link': catcher_link})
            print(f"Data appended: Player Name - {catcher_name}, Player Link - {catcher_link}")

    if infielders_container:
        infielders_table = infielders_container.find('table', class_='Table')
        infielders_items = infielders_table.find_all('tr', class_='Table__TR Table__TR--lg Table__even')
        for infielder_item in infielders_items:
            infielder_item_info = infielder_item.find_all('td')
            infielder_name_tab = infielder_item_info[1].find('a', class_='AnchorLink')
            infielder_name = infielder_name_tab.text.strip()
            infielder_name = remove_periods(infielder_name)
            infielder_link = infielder_name_tab.get('href')
            data.append({'Team': team_name, 'Player Name': infielder_name, 'Player Link': infielder_link})
            print(f"Data appended: Player Name - {infielder_name}, Player Link - {infielder_link}")

    if outfielders_container:
        outfielders_table = outfielders_container.find('table', class_='Table')
        outfielders_items = outfielders_table.find_all('tr', class_='Table__TR Table__TR--lg Table__even')
        for outfielder_item in outfielders_items:
            outfielder_item_info = outfielder_item.find_all('td')
            outfielder_name_tab = outfielder_item_info[1].find('a', class_='AnchorLink')
            outfielder_name = outfielder_name_tab.text.strip()
            outfielder_name = remove_periods(outfielder_name)
            outfielder_link = outfielder_name_tab.get('href')
            data.append({'Team': team_name, 'Player Name': outfielder_name, 'Player Link': outfielder_link})
            print(f"Data appended: Player Name - {outfielder_name}, Player Link - {outfielder_link}")

    if dhs_container:
        dhs_table = dhs_container.find('table', class_='Table')
        dhs_items = dhs_table.find_all('tr', class_='Table__TR Table__TR--lg Table__even')
        for dh_item in dhs_items:
            dh_item_info = dh_item.find_all('td')
            dh_name_tab = dh_item_info[1].find('a', class_='AnchorLink')
            dh_name = dh_name_tab.text.strip()
            dh_name = remove_periods(dh_name)
            dh_link = dh_name_tab.get('href')
            data.append({'Team': team_name, 'Player Name': dh_name, 'Player Link': dh_link})
            print(f"Data appended: Player Name - {dh_name}, Player Link - {dh_link}")

# Function to save data to CSV
def save_to_csv(filename, data):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def main():
    # Save data to CSV and Excel files
    save_to_csv('mlb_links_players.csv', data)
    print("Data written to mlb_links_players.csv")

if __name__ == '__main__':
    main()
