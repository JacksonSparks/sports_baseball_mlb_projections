import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

# URL of the website to scrape
url = "https://www.espn.com/mlb/teams"

# User-Agent header to avoid getting blocked
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)
response.raise_for_status()  # Raise an exception for HTTP errors
soup = BeautifulSoup(response.text, 'html.parser')

# Find all the matchup div elements
teams = soup.find_all('div', class_='ContentList__Item', role='listitem')

# Prepare data for CSV and Excel
data = []
header = ['Team', 'Roster Link']


def replace_team_name(name):
    return name.replace("D-backs", "Diamondbacks")


# Iterate over each matchup and extract the required information
for team in teams:
    team_container = team.find('div', class_='pl3')
    if not team_container:
        print("No team container found")
        continue

    team_name_element = team_container.find('h2', class_='di clr-gray-01 h5')
    if not team_name_element:
        print("No team name element found")
        continue
    team_name = team_name_element.text.strip()
    team_name = replace_team_name(team_name)
    print(f"Team: {team_name}")

    team_links_container = team_container.find('div', class_='TeamLinks__Links')
    if not team_links_container:
        print("No team links container found")
        continue

    team_links = team_links_container.find_all('span', class_='TeamLinks__Link n9 nowrap')
    if len(team_links) < 3:
        print("Not enough team links found")
        continue

    team_roster_link_element = team_links[2].find('a', class_='AnchorLink')
    if not team_roster_link_element:
        print("No team roster link element found")
        continue
    team_roster_link = team_roster_link_element.get('href')
    print(f"Roster Link: {team_roster_link}")

    # Append data
    data.append({
        'Team': team_name,
        'Roster Link': team_roster_link,
    })
    print(f"Data appended: Team - {team_name}, Roster Link - {team_roster_link}")

# Function to save data to CSV
def save_to_csv(filename, data):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

# Function to save data to Excel
# def save_to_excel(filename, data):
#     df = pd.DataFrame(data)
#     df.to_excel(filename, index=False, columns=header)  # Set column order explicitly

def main():
    # Save data to CSV and Excel files
    save_to_csv('mlb_links_teams.csv', data)
    print("Data written to mlb_links_teams.csv")

if __name__ == '__main__':
    main()
