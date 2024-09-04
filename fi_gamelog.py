import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta
from urllib.parse import urljoin


# User-Agent header to avoid getting blocked
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def remove_periods(last_name):
    """
    Removes all periods from the given last name.

    Parameters:
    last_name (str): The last name to be checked and modified.

    Returns:
    str: The modified last name with all periods removed.
    """
    return last_name.replace(".", "")

def scrape_pitcher_throw(pitcher_url):
    try:
        response = requests.get(pitcher_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')

        # Debugging prints
        print("Pitcher page fetched successfully")

        # Find the ul element with class "PlayerHeader__Bio_List flex flex-column list clr-gray-04"
        bio_list = soup.find('ul', class_='PlayerHeader__Bio_List flex flex-column list clr-gray-04')
        if not bio_list:
            print(f"Error: Bio list not found on pitcher page {pitcher_url}")
            return None

        # Find the third li element
        li_elements = bio_list.find_all('li')
        if len(li_elements) < 5:
            if len(li_elements) < 3:
                print(f"Error: Not enough li elements found on pitcher page {pitcher_url}")
                return None
            else:
                throwing_info = li_elements[1].find('div', class_='fw-medium clr-black')
                if not throwing_info:
                    print(f"Error: Throwing info div not found on pitcher page {pitcher_url}")
                    return None
                throwing_orientation = throwing_info.find('div').text.strip()
                return throwing_orientation.split('/')[1].strip()

        # Find the div with the class "fw-medium clr-black" and extract throwing orientation
        throwing_info = li_elements[2].find('div', class_='fw-medium clr-black')
        if not throwing_info:
            print(f"Error: Throwing info div not found on pitcher page {pitcher_url}")
            return None

        throwing_orientation = throwing_info.find('div').text.strip()
        return throwing_orientation.split('/')[1].strip()

    except requests.RequestException as e:
        print(f"Request error for pitcher URL {pitcher_url}: {e}")
        return None


def scrape_pitcher_era(pitcher_url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(pitcher_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')

        # Debugging prints
        print("Pitcher page fetched successfully")

        # Find the specific stat block container
        stat_container = soup.find('aside', class_='StatBlock br-5 ba overflow-hidden flex-expand StatBlock--multiple bg-clr-white brdr-clr-gray-06 PlayerHeader__StatBlock')

        # If stat_container is None, print an error message and return
        if not stat_container:
            print(f"Error: Stat container not found on pitcher page {pitcher_url}")
            return None

        # Find the ul element within the stat block container
        stat_list = stat_container.find('ul', class_='StatBlock__Content flex list ph4 pv3 justify-between')
        if not stat_list:
            print(f"Error: Stat list not found on pitcher page {pitcher_url}")
            return None

        # Find all li elements within the ul element
        li_elements = stat_list.find_all('li', class_='flex-expand')
        if len(li_elements) < 2:
            print(f"Error: Not enough li elements found on pitcher page {pitcher_url}")
            return None

        # Find the div with the class "StatBlockInner" in the second li element
        era_info = li_elements[1].find('div', class_='StatBlockInner')
        if not era_info:
            print(f"Error: ERA info div not found on pitcher page {pitcher_url}")
            return None

        # Try to find the ERA value div using more generalized classes
        era_value_div = era_info.find('div', class_='StatBlockInner__Value')
        if not era_value_div:
            # Print the content of era_info for debugging
            print(f"Debug: ERA info div content: {era_info}")
            print(f"Error: ERA value div not found on pitcher page {pitcher_url}")
            return None

        # Extract the text and strip any surrounding whitespace
        era_number = era_value_div.text.strip()
        return era_number

    except requests.RequestException as e:
        print(f"Request error for pitcher URL {pitcher_url}: {e}")
        return None


def scrape_pitcher_name(pitcher_url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(pitcher_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')

        # Debugging prints
        print("Pitcher page fetched successfully")

        # Find the specific stat block container
        name_container = soup.find('div', class_='PlayerHeader__Main_Aside min-w-0 flex-grow flex-basis-0')

        if not name_container:
            print("name_container not found")

        name_container_inner = name_container.find('h1')

        if not name_container_inner:
            print("name_container_inner not found")

        name_parts = name_container_inner.find_all('span')

        if not name_parts:
            print("name_parts not found")

        first_name = name_parts[0].text.strip()
        last_name = name_parts[1].text.strip()

        last_name = remove_periods(last_name)
        first_name = remove_periods(first_name)

        full_name = f"{first_name} {last_name}"

        return full_name

    except requests.RequestException as e:
        print(f"Request error for pitcher URL {pitcher_url}: {e}")
        return None


# Function to scrape box score page
def scrape_box_score(box_score_url):
    try:
        response = requests.get(box_score_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')

        # Debugging prints
        print("Box score page fetched successfully")

        # Extract the first inning runs from each team
        table = soup.find('table', class_='Table Table--align-center')
        if not table:
            print("Error: Table not found")
            return None, None, None, None, None, None, None, None, None, None, None, None

        rows = table.find('tbody').find_all('tr', class_='Table__TR Table__TR--sm Table__even')
        if len(rows) < 2:
            print("Error: Not enough rows found in table")
            return None, None, None, None, None, None, None, None, None, None, None, None

        # Extract first inning runs from each team
        first_inning_runs = [row.find_all('td')[0].text.strip() for row in rows]

        if len(first_inning_runs) == 2:
            away_team_runs = first_inning_runs[0]
            home_team_runs = first_inning_runs[1]
        else:
            print("Error: Could not retrieve first inning runs")
            return None, None, None, None, None, None, None, None, None, None, None, None

        # Extract starting pitchers
        player_sections = soup.find_all('div', class_='Boxscore__Category')
        if len(player_sections) < 2:
            print("Error: Not enough pitcher sections found")
            return away_team_runs, home_team_runs, None, None, None, None, None, None, None, None, None, None

        # The second div with class 'Boxscore__Category' is for the pitchers
        pitcher_table = player_sections[1]

        pitcher_sections = pitcher_table.find_all('div', class_='Boxscore__Team')
        if len(pitcher_sections) < 2:
            print("Error: Not enough pitcher sections found")
            return away_team_runs, home_team_runs, None, None, None, None, None, None, None, None, None, None

        away_pitchers = pitcher_sections[0].find_all('a', class_='AnchorLink Boxscore__Athlete_Name truncate db')
        home_pitchers = pitcher_sections[1].find_all('a', class_='AnchorLink Boxscore__Athlete_Name truncate db')

        base_url = 'https://www.espn.com'

        if away_pitchers and home_pitchers:
            away_pitcher = away_pitchers[0].text.strip()
            home_pitcher = home_pitchers[0].text.strip()
            away_pitcher_url = urljoin(base_url, away_pitchers[0]['href'])
            home_pitcher_url = urljoin(base_url, home_pitchers[0]['href'])
        else:
            print("Error: Could not retrieve pitcher names")
            return away_team_runs, home_team_runs, None, None, None, None, None, None, None, None, None, None

        # Extract starting pitchers' innings and earned runs
        pitcher_boxscore = pitcher_table.find_all('div', class_='Table__ScrollerWrapper relative overflow-hidden')
        if len(pitcher_boxscore) < 2:
            print("Error: Not enough pitcher boxscores found")
            return away_team_runs, home_team_runs, away_pitcher, home_pitcher, None, None, None, None, None, None, None, None

        away_pitcher_boxscore = pitcher_boxscore[0].find('tbody').find_all('tr', class_='Table__TR Table__TR--sm Table__even')
        home_pitcher_boxscore = pitcher_boxscore[1].find('tbody').find_all('tr', class_='Table__TR Table__TR--sm Table__even')

        away_pitcher_stats = away_pitcher_boxscore[0].find_all('td', class_="Table__TD")
        home_pitcher_stats = home_pitcher_boxscore[0].find_all('td', class_="Table__TD")

        if away_pitcher_stats and home_pitcher_stats:
            away_pitcher_innings = away_pitcher_stats[0].text.strip()
            away_pitcher_runs = away_pitcher_stats[3].text.strip()
            home_pitcher_innings = home_pitcher_stats[0].text.strip()
            home_pitcher_runs = home_pitcher_stats[3].text.strip()
        else:
            print("Error: Could not retrieve pitcher stats")
            return away_team_runs, home_team_runs, away_pitcher, home_pitcher, None, None, None, None, None, None

        # Normalize innings pitched to 1 if >= 1
        if float(away_pitcher_innings) >= 1:
            away_pitcher_innings = 1
            away_pitcher_runs = home_team_runs
        else:
            away_pitcher_innings = away_pitcher_innings
            away_pitcher_runs = away_pitcher_runs

        if float(home_pitcher_innings) >= 1:
            home_pitcher_innings = 1
            home_pitcher_runs = away_team_runs
        else:
            home_pitcher_innings = home_pitcher_innings
            home_pitcher_runs = home_pitcher_runs

        if away_pitcher_url and home_pitcher_url:
            # Scrape pitcher orientations
            away_throw = scrape_pitcher_throw(away_pitcher_url)
            home_throw = scrape_pitcher_throw(home_pitcher_url)
            away_era = scrape_pitcher_era(away_pitcher_url)
            home_era = scrape_pitcher_era(home_pitcher_url)
            away_pitcher_full_name = scrape_pitcher_name(away_pitcher_url)
            home_pitcher_full_name = scrape_pitcher_name(home_pitcher_url)
        else:
            return away_team_runs, home_team_runs, away_pitcher, home_pitcher, away_pitcher_innings, home_pitcher_innings, away_pitcher_runs, home_pitcher_runs, None, None, None, None

        if away_throw and home_throw:
            if away_era and home_era:
                if away_pitcher_full_name and home_pitcher_full_name:
                    away_pitcher = away_pitcher_full_name
                    home_pitcher = home_pitcher_full_name
                    return away_team_runs, home_team_runs, away_pitcher, home_pitcher, away_pitcher_innings, home_pitcher_innings, away_pitcher_runs, home_pitcher_runs, away_throw, home_throw, away_era, home_era
            else:
                return away_team_runs, home_team_runs, away_pitcher, home_pitcher, away_pitcher_innings, home_pitcher_innings, away_pitcher_runs, home_pitcher_runs, away_throw, home_throw, None, None
        else:
            return away_team_runs, home_team_runs, away_pitcher, home_pitcher, away_pitcher_innings, home_pitcher_innings, away_pitcher_runs, home_pitcher_runs, None, None, None, None

    except requests.RequestException as e:
        print(f"Request error for box score URL {box_score_url}: {e}")
        return None, None, None, None, None, None, None, None, None, None, None, None


# Function to scrape a single day's games
def scrape_games(date):
    url = f'http://espn.com/mlb/scoreboard/_/date/{date}'

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all sections that contain game information
        games = soup.find_all('section', class_='Scoreboard bg-clr-white flex flex-auto justify-between')

        if not games:
            print(f"No games found for date: {date}")

        game_data = []

        # Iterate over each game section and extract information
        for game in games:
            # Extract team names
            teams = game.find_all('div', class_='ScoreCell__TeamName')
            if len(teams) >= 2:
                away_team = teams[0].text.strip()
                home_team = teams[1].text.strip()

                # Extract the box score URL
                box_score_link = game.find('a', text='Box Score')
                if box_score_link:
                    box_score_url = 'http://espn.com' + box_score_link['href']
                    print(f"Fetching box score for URL: {box_score_url}")
                    away_runs, home_runs, away_pitcher, home_pitcher, away_pitcher_innings, home_pitcher_innings, away_pitcher_runs, home_pitcher_runs, away_throw, home_throw, away_era, home_era = scrape_box_score(box_score_url)
                    if away_runs is not None and home_runs is not None:
                        # Create a dictionary with the scraped data
                        game_data.append({
                            'Date': date,
                            'Away Team': away_team,
                            'Home Team': home_team,
                            'Away Team Runs': away_runs,
                            'Home Team Runs': home_runs,
                            'Away Pitcher': away_pitcher,
                            'Home Pitcher': home_pitcher,
                            'Away Pitcher I': away_pitcher_innings,
                            'Home Pitcher I': home_pitcher_innings,
                            'Away Pitcher ER': away_pitcher_runs,
                            'Home Pitcher ER': home_pitcher_runs,
                            'Away Throw': away_throw,
                            'Home Throw': home_throw,
                            'Away ERA': away_era,
                            'Home ERA': home_era
                        })
                    else:
                        print(f"Error retrieving data for game on {date}")
                else:
                    print(f"No box score link found for game on {date}")

        return game_data

    except requests.RequestException as e:
        print(f"Request error for date {date}: {e}")
        return []

# Function to save data to CSV
def save_to_csv(filename, data):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=[
            'Date', 'Away Team', 'Home Team', 'Away Team Runs', 'Home Team Runs',
            'Away Pitcher', 'Home Pitcher', 'Away Pitcher I', 'Home Pitcher I',
            'Away Pitcher ER', 'Home Pitcher ER',
            'Away Throw', 'Home Throw', 'Away ERA', 'Home ERA'
        ])
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def main():
    start_date = datetime.strptime('2024-03-28', '%Y-%m-%d')
    end_date = datetime.strptime('2024-07-14', '%Y-%m-%d')

    all_game_data = []

    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y%m%d')
        print(f"Scraping data for {date_str}")
        daily_game_data = scrape_games(date_str)
        all_game_data.extend(daily_game_data)
        current_date += timedelta(days=1)

    if all_game_data:
        save_to_csv('fi_gamelog.csv', all_game_data)
        print("Scraped data saved to fi_gamelog.csv")
    else:
        print("No data to save.")

if __name__ == '__main__':
    main()
