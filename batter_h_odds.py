import csv
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Install the correct version of ChromeDriver
chromedriver_autoinstaller.install()

# Prepare data for CSV
data = []
header = ['Batter Name', '1 H', '2 H', '3 H']

url = "https://sportsbook.draftkings.com/leagues/baseball/mlb?category=batter-props&subcategory=hits"

# Set up Selenium
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Initialize the Chrome driver
driver = webdriver.Chrome(options=options)

# Open the URL
driver.get(url)

def replace_player_name(name):
    name = name.replace("Bobby Witt Jr.", "Bobby Witt Jr")
    name = name.replace("Vladimir Guerrero Jr.", "Vladimir Guerrero Jr")
    name = name.replace("Jazz Chisholm", "Jazz Chisholm Jr")
    name = name.replace("Luis Garcia (WAS)", "Luis Garcia Jr")
    name = name.replace("Luis Robert", "Luis Robert Jr")
    name = name.replace("LaMonte Wade Jr.", "LaMonte Wade Jr")
    name = name.replace("Lourdes Gurriel Jr.", "Lourdes Gurriel Jr")
    name = name.replace("Michael Harris", "Michael Harris II")
    name = name.replace("Will Smith (LAD)", "Will Smith")
    return name

def remove_hits_suffix(player_name):
    """
    Removes the ' Hits' suffix from the given player name.

    Parameters:
    player_name (str): The player name to be checked and modified.

    Returns:
    str: The modified player name without the ' Hits' suffix.
    """
    return player_name.replace(" Hits", "")


# Wait for the player items to be present
try:
    player_items = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "component-29"))
    )

    for item in player_items:
        try:
            # Extract the player name
            player_name_tag = item.find_element(By.CSS_SELECTOR, "p.participants")
            player_name = remove_hits_suffix(player_name_tag.text.strip())
            player_name = replace_player_name(player_name)

            # Extract hit odds
            hit_odds = item.find_elements(By.CSS_SELECTOR, "ul > li.component-29__cell")

            # Initialize odds values
            odds_1h, odds_2h, odds_3h = '', '', ''

            # Iterate through the hit odds elements and extract text
            if len(hit_odds) > 0:
                odds_1h = hit_odds[0].find_element(By.CSS_SELECTOR, "div.sportsbook-outcome-cell__element span").text.strip()
            if len(hit_odds) > 1:
                odds_2h = hit_odds[1].find_element(By.CSS_SELECTOR, "div.sportsbook-outcome-cell__element span").text.strip()
            if len(hit_odds) > 2:
                odds_3h = hit_odds[2].find_element(By.CSS_SELECTOR, "div.sportsbook-outcome-cell__element span").text.strip()

            # Append the extracted data to the list
            data.append({'Batter Name': player_name, '1 H': odds_1h, '2 H': odds_2h, '3 H': odds_3h})
            print(f"Data appended: Batter Name - {player_name}, 1 H - {odds_1h}, 2 H - {odds_2h}, 3 H - {odds_3h}")

        except Exception as e:
            print(f"Error processing player item: {e}")

finally:
    driver.quit()

# Function to save data to CSV
def save_to_csv(filename, data):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def main():
    # Save data to CSV
    save_to_csv('batter_h_odds.csv', data)
    print("Data written to batter_h_odds.csv")

if __name__ == '__main__':
    main()
