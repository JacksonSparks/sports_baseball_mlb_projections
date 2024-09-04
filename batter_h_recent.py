# import csv
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
# # Prepare data for CSV
# data = []
# header = ['Player Name', 'Player AVG', 'Player AB']
#
# url = "https://www.fantasypros.com/mlb/stats/hitters.php?range=15"
#
# # Set up Selenium
# options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Run in headless mode
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
#
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#
# # Open the URL
# driver.get(url)

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
header = ['Player Name', 'B Recent H', 'B Recent PA']

url = "https://www.fantasypros.com/mlb/stats/hitters.php?range=15"

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
    name = name.replace("Cedric Mullins II", "Cedric Mullins")
    name = name.replace("Luis Garcia", "Luis Garcia Jr")
    name = name.replace("Kike Hernandez", "Enrique Hernandez")
    name = name.replace("Michael A. Taylor", "Michael A Taylor")
    return name


def remove_periods(last_name):
    """
    Removes all periods from the given last name.

    Parameters:
    last_name (str): The last name to be checked and modified.

    Returns:
    str: The modified last name with all periods removed.
    """
    return last_name.replace(".", "")


# Wait for the table to be present
try:
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "data"))
    )

    # Extract rows from the table
    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows[1:]:  # Skip the header row
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) > 7:  # Ensure there are enough columns
            player_a_tag = cols[1].find_element(By.TAG_NAME, "a")
            player_name = player_a_tag.text.strip()
            player_name = remove_periods(player_name)
            player_name = replace_player_name(player_name)
            player_abs = cols[2].text.strip()
            player_h = cols[9].text.strip()
            player_bb = cols[12].text.strip()
            player_abs = float(player_abs)
            player_bb = float(player_bb)
            player_h = float(player_h)
            player_abs += player_bb

            try:
                player_abs = float(player_abs)
                player_bb = float(player_bb)
                player_h = float(player_h)
                player_abs += player_bb
            except ValueError:
                continue  # Skip rows with invalid data

            data.append({'Player Name': player_name, 'B Recent H': player_h, 'B Recent PA': player_abs})
            print(f"Data appended: Player Name - {player_name}, Player H - {player_h}, Player PA - {player_abs}")

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
    save_to_csv('batter_h_recent.csv', data)
    print("Data written to batter_h_recent.csv")

if __name__ == '__main__':
    main()
