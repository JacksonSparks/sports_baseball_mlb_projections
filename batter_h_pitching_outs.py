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
header = ['Player Name', 'Pitching Outs']

url = "https://sportsbook.draftkings.com/leagues/baseball/mlb?category=pitcher-props&subcategory=outs-recorded"

# Set up Selenium
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Initialize the Chrome driver
driver = webdriver.Chrome(options=options)

# Open the URL
driver.get(url)

def remove_hits_suffix(player_name):
    """
    Removes the ' Hits' suffix from the given player name.
    """
    return player_name.replace(" Hits", "")

# Wait for the player items to be present
try:
    player_items = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".sportsbook-table__body > tr"))
    )

    for item in player_items:
        try:
            # Extract the player name
            player_name_tag = item.find_element(By.CSS_SELECTOR, ".sportsbook-row-name")
            player_name = remove_hits_suffix(player_name_tag.text.strip())

            # Extract the Pitching Outs value
            pitching_outs = ""
            outcome_cells = item.find_elements(By.CSS_SELECTOR, ".sportsbook-outcome-cell__line")

            if len(outcome_cells) > 0:
                # Assuming "O 17.5" and "U 17.5" appear in two cells, get the value from the first cell
                pitching_outs = outcome_cells[0].text.strip()

            # Append the extracted data to the list
            data.append({'Player Name': player_name, 'Pitching Outs': pitching_outs})
            print(f"Data appended: Player Name - {player_name}, Pitching Outs - {pitching_outs}")

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
    save_to_csv('batter_h_pitching_outs.csv', data)
    print("Data written to batter_h_pitching_outs.csv")

if __name__ == '__main__':
    main()
