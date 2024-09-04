import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL and headers for the backup website
backup_url = "https://rotogrinders.com/lineups/mlb"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def replace_player_name(name):
    name = name.replace("LaMonte Wade", "LaMonte Wade Jr")
    name = name.replace("Mike King", "Michael King")
    name = name.replace("Lourdes Gurriel", "Lourdes Gurriel Jr")
    name = name.replace("Fernando Tatis", "Fernando Tatis Jr")
    name = name.replace("Luis Robert", "Luis Robert Jr")
    name = name.replace("Luis Garcia", "Luis Garcia Jr")
    name = name.replace("Vladimir Guerrero Jr.", "Vladimir Guerrero Jr")
    name = name.replace("Bobby Witt", "Bobby Witt Jr")
    name = name.replace("Michael Harris", "Michael Harris II")
    name = name.replace("Michael A. Taylor", "Michael A Taylor")
    name = name.replace("Jazz Chisholm", "Jazz Chisholm Jr")
    name = name.replace("Yulieski Gurriel", "Yuli Gurriel")
    name = name.replace("Zachary DeLoach", "Zach DeLoach")
    return name


# Function to fetch and parse the backup lineups
def fetch_backup_lineups():
    response = requests.get(backup_url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the lineup divs
    lineups_div = soup.find('div', class_='container-body columns')
    if not lineups_div:
        print("Lineups container not found.")
        return []

    lineups = lineups_div.find_all('div', class_='module game-card')
    if not lineups:
        print("No lineup divs found.")
        return []

    backup_lineups = []

    for lineup in lineups:
        lineup_header = lineup.find('div', class_='module-header game-card-header')
        if not lineup_header:
            print("Lineup header not found for a game.")
            continue  # Skip if lineup_box is not found

        teams_container = lineup_header.find('div', class_='game-card-teams')
        if not teams_container:
            print("Teams container not found for a game.")
            continue  # Skip if teams_container is not found

        teams_containers = teams_container.find_all('div', class_='team-nameplate')
        if len(teams_containers) < 2:
            print("Teams containers not found properly.")
            continue  # Ensure both teams are present

        away_team_city = teams_containers[0].find('span', class_='team-nameplate-title').find('span', class_='team-nameplate-city').text.strip()
        home_team_city = teams_containers[1].find('span', class_='team-nameplate-title').find('span', class_='team-nameplate-city').text.strip()
        away_team_mascot = teams_containers[0].find('span', class_='team-nameplate-title').find('span', class_='team-nameplate-mascot').text.strip()
        home_team_mascot = teams_containers[1].find('span', class_='team-nameplate-title').find('span', class_='team-nameplate-mascot').text.strip()

        # Extract the team names, ignoring the win-loss records
        if away_team_city and away_team_mascot and home_team_city and home_team_mascot:
            away_team = away_team_mascot
            home_team = home_team_mascot
        else:
            print("Team city or mascot missing.")
            continue  # Skip if either team div is not found

        lineup_body = lineup.find('div', class_='module-body game-card-body')
        if not lineup_body:
            print("Lineup body not found for a game.")
            continue  # Skip if lineup_main is not found

        lineup_body_inner = lineup_body.find('div', class_='game-card-lineups')
        if not lineup_body_inner:
            print("Lineup inner body not found for a game.")
            continue  # Skip if lineup_main is not found

        lineups_divs = lineup_body_inner.find_all('div', class_='lineup-card')
        if len(lineups_divs) < 2:
            print("Lineups divs not found properly.")
            continue  # Ensure both lineups are present

        away_div = lineups_divs[0]
        home_div = lineups_divs[1]

        if away_div and home_div:
            away_div_header = away_div.find('div', class_='lineup-card-header')
            home_div_header = home_div.find('div', class_='lineup-card-header')

            if away_div_header and home_div_header:
                away_pitcher_div = away_div_header.find('div', class_='lineup-card-pitcher break')
                if away_pitcher_div:
                    away_pitcher_div = away_pitcher_div.find('span')
                    if away_pitcher_div:
                        away_pitcher_div = away_pitcher_div.find('div', class_='player-nameplate-info')
                    else:
                        print("Away pitcher span not found.")
                        continue
                else:
                    print("Away pitcher div not found.")
                    continue

                home_pitcher_div = home_div_header.find('div', class_='lineup-card-pitcher break')
                if home_pitcher_div:
                    home_pitcher_div = home_pitcher_div.find('span')
                    if home_pitcher_div:
                        home_pitcher_div = home_pitcher_div.find('div', class_='player-nameplate-info')
                    else:
                        print("Home pitcher span not found.")
                        continue
                else:
                    print("Home pitcher div not found.")
                    continue

            else:
                print("Header divs not found.")
                continue

            if away_pitcher_div and home_pitcher_div:
                away_pitcher = replace_player_name(away_pitcher_div.find('a', class_='player-nameplate-name').text.strip())
                home_pitcher = replace_player_name(home_pitcher_div.find('a', class_='player-nameplate-name').text.strip())
            else:
                print("Pitcher information not found.")
                continue  # Skip if pitcher information is not found


            away_batters_ul = away_div.find('div', class_='lineup-card-body').find('ul', class_='lineup-card-players')
            home_batters_ul = home_div.find('div', class_='lineup-card-body').find('ul', class_='lineup-card-players')

            if not away_batters_ul or not home_batters_ul:
                print("Batter lists not found.")
                continue  # Skip if batter lists are not found

            away_batters = away_batters_ul.find_all('li', class_='lineup-card-player')
            home_batters = home_batters_ul.find_all('li', class_='lineup-card-player')

            away_batter_names = []
            for away_batter in away_batters:
                away_batter_name = away_batter.find('div', class_='player-nameplate-info').find('a', class_='player-nameplate-name').text.strip()
                away_batter_names.append(replace_player_name(away_batter_name))

            home_batter_names = []
            for home_batter in home_batters:
                home_batter_name = home_batter.find('div', class_='player-nameplate-info').find('a', class_='player-nameplate-name').text.strip()
                home_batter_names.append(replace_player_name(home_batter_name))

            backup_lineups.append({
                'Away Team': away_team,
                'Away Pitcher': away_pitcher,
                'Away (1)': away_batter_names[0] if len(away_batter_names) > 0 else '',
                'Away (2)': away_batter_names[1] if len(away_batter_names) > 1 else '',
                'Away (3)': away_batter_names[2] if len(away_batter_names) > 2 else '',
                'Away (4)': away_batter_names[3] if len(away_batter_names) > 3 else '',
                'Away (5)': away_batter_names[4] if len(away_batter_names) > 4 else '',
                'Away (6)': away_batter_names[5] if len(away_batter_names) > 5 else '',
                'Away (7)': away_batter_names[6] if len(away_batter_names) > 6 else '',
                'Away (8)': away_batter_names[7] if len(away_batter_names) > 7 else '',
                'Away (9)': away_batter_names[8] if len(away_batter_names) > 8 else '',
                'Home Team': home_team,
                'Home Pitcher': home_pitcher,
                'Home (1)': home_batter_names[0] if len(home_batter_names) > 0 else '',
                'Home (2)': home_batter_names[1] if len(home_batter_names) > 1 else '',
                'Home (3)': home_batter_names[2] if len(home_batter_names) > 2 else '',
                'Home (4)': home_batter_names[3] if len(home_batter_names) > 3 else '',
                'Home (5)': home_batter_names[4] if len(home_batter_names) > 4 else '',
                'Home (6)': home_batter_names[5] if len(home_batter_names) > 5 else '',
                'Home (7)': home_batter_names[6] if len(home_batter_names) > 6 else '',
                'Home (8)': home_batter_names[7] if len(home_batter_names) > 7 else '',
                'Home (9)': home_batter_names[8] if len(home_batter_names) > 8 else ''
            })
        else:
            print("Away or home div not found.")
            continue  # Skip if away or home div is not found

    return backup_lineups

# Function to save backup lineups to CSV
def save_backup_lineups():
    # Fetch the backup lineups
    backup_lineups = fetch_backup_lineups()

    if not backup_lineups:
        print("No lineups found.")
        return

    # Convert the backup lineups to a DataFrame
    lineups_df = pd.DataFrame(backup_lineups)

    # Save the data to a CSV file
    lineups_df.to_csv('lineups.csv', index=False)
    print("Lineups saved to lineups.csv")

if __name__ == "__main__":
    save_backup_lineups()
