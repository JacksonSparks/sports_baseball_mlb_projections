import csv
from collections import defaultdict, deque

# Function to count team and pitcher appearances
def count_appearances(filename):
    # Dictionaries to keep counts
    team_counts = defaultdict(lambda: {
        'Away': 0, 'Away RS': 0, 'Away RA': 0, 'Away NRFI': 0, 'Away YRFI': 0, 'Away NRSFI': 0, 'Away YRSFI': 0,
        'Home': 0, 'Home RS': 0, 'Home RA': 0, 'Home NRFI': 0, 'Home YRFI': 0, 'Home NRSFI': 0, 'Home YRSFI': 0,
        'Total NRFI': 0, 'Total YRFI': 0, 'Total NRSFI': 0, 'Total YRSFI': 0,
        'Intra NRFI': 0, 'Intra YRFI': 0, 'Intra NRSFI': 0, 'Intra YRSFI': 0,
        'Righties NRSFI': 0, 'Righties YRSFI': 0,
        'Lefties NRSFI': 0, 'Lefties YRSFI': 0,
        'L10 NRSFI': deque(maxlen=10),  # Initialize with a deque to keep track of last 10 NRSFI results
        'NRSFI Streak': 0, 'YRSFI Streak': 0  # Initialize streaks
    })

    pitcher_counts = defaultdict(lambda: {
        'Away': 0, 'Away RA': 0, 'Away NRFI': 0, 'Away YRFI': 0,
        'Home': 0, 'Home RA': 0, 'Home NRFI': 0, 'Home YRFI': 0,
        'Total NRFI': 0, 'Total YRFI': 0,
        'Throw': '',  # Initialize with empty string
        'Season ERA': 0,
        'L5 NRFI': deque(maxlen=5),  # Initialize with a deque to keep track of last 10 NRSFI results
        'NRFI Streak': 0, 'YRFI Streak': 0  # Initialize streaks
    })

    # Define divisions
    divisions = {
        'AL West': ['Mariners', 'Astros', 'Rangers', 'Angels', 'Athletics'],
        'AL East': ['Yankees', 'Red Sox', 'Blue Jays', 'Rays', 'Orioles'],
        'AL Central': ['White Sox', 'Guardians', 'Tigers', 'Royals', 'Twins'],
        'NL West': ['Dodgers', 'Giants', 'Padres', 'Diamondbacks', 'Rockies'],
        'NL East': ['Braves', 'Mets', 'Phillies', 'Marlins', 'Nationals'],
        'NL Central': ['Cubs', 'Cardinals', 'Brewers', 'Pirates', 'Reds']
    }

    team_to_division = {}
    for division, teams in divisions.items():
        for team in teams:
            team_to_division[team] = division


    # Read the CSV file
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            away_team = row['Away Team']
            home_team = row['Home Team']
            away_runs = int(row['Away Team Runs'])
            home_runs = int(row['Home Team Runs'])
            away_pitcher = row['Away Pitcher']
            home_pitcher = row['Home Pitcher']
            away_pitcher_runs = float(row['Away Pitcher ER'])
            home_pitcher_runs = float(row['Home Pitcher ER'])
            home_pitcher_throw = row['Home Throw']
            away_pitcher_throw = row['Away Throw']
            home_pitcher_era = row['Home ERA']
            away_pitcher_era = row['Away ERA']

            # Check if the game is intradivision
            if team_to_division[away_team] == team_to_division[home_team]:
                intradivision_game = True
            else:
                intradivision_game = False

            # Update team counts
            team_counts[away_team]['Away'] += 1
            team_counts[away_team]['Away RS'] += away_runs
            team_counts[away_team]['Away RA'] += home_runs
            team_counts[away_team]['Away NRFI'] += 1 if (home_runs + away_runs) == 0 else 0
            team_counts[away_team]['Away YRFI'] += 1 if (home_runs + away_runs) > 0 else 0
            team_counts[away_team]['Away NRSFI'] += 1 if away_runs == 0 else 0
            team_counts[away_team]['Away YRSFI'] += 1 if away_runs > 0 else 0

            team_counts[home_team]['Home'] += 1
            team_counts[home_team]['Home RS'] += home_runs
            team_counts[home_team]['Home RA'] += away_runs
            team_counts[home_team]['Home NRFI'] += 1 if (home_runs + away_runs) == 0 else 0
            team_counts[home_team]['Home YRFI'] += 1 if (home_runs + away_runs) > 0 else 0
            team_counts[home_team]['Home NRSFI'] += 1 if home_runs == 0 else 0
            team_counts[home_team]['Home YRSFI'] += 1 if home_runs > 0 else 0

            # Update total NRFI and YRFI for teams
            team_counts[away_team]['Total NRFI'] = team_counts[away_team]['Away NRFI'] + team_counts[away_team]['Home NRFI']
            team_counts[away_team]['Total YRFI'] = team_counts[away_team]['Away YRFI'] + team_counts[away_team]['Home YRFI']
            team_counts[away_team]['Total NRSFI'] = team_counts[away_team]['Away NRSFI'] + team_counts[away_team]['Home NRSFI']
            team_counts[away_team]['Total YRSFI'] = team_counts[away_team]['Away YRSFI'] + team_counts[away_team]['Home YRSFI']

            team_counts[home_team]['Total NRFI'] = team_counts[home_team]['Away NRFI'] + team_counts[home_team]['Home NRFI']
            team_counts[home_team]['Total YRFI'] = team_counts[home_team]['Away YRFI'] + team_counts[home_team]['Home YRFI']
            team_counts[home_team]['Total NRSFI'] = team_counts[home_team]['Away NRSFI'] + team_counts[home_team]['Home NRSFI']
            team_counts[home_team]['Total YRSFI'] = team_counts[home_team]['Away YRSFI'] + team_counts[home_team]['Home YRSFI']

            # Update Righties and Lefties NRSFI and YRSFI for teams
            team_counts[away_team]['Righties NRSFI'] += 1 if (away_runs == 0) and (home_pitcher_throw == 'Right') else 0
            team_counts[away_team]['Righties YRSFI'] += 1 if (away_runs > 0) and (home_pitcher_throw == 'Right') else 0
            team_counts[away_team]['Lefties NRSFI'] += 1 if (away_runs == 0) and (home_pitcher_throw == 'Left') else 0
            team_counts[away_team]['Lefties YRSFI'] += 1 if (away_runs > 0) and (home_pitcher_throw == 'Left') else 0

            team_counts[home_team]['Righties NRSFI'] += 1 if (home_runs == 0) and (away_pitcher_throw == 'Right') else 0
            team_counts[home_team]['Righties YRSFI'] += 1 if (home_runs > 0) and (away_pitcher_throw == 'Right') else 0
            team_counts[home_team]['Lefties NRSFI'] += 1 if (home_runs == 0) and (away_pitcher_throw == 'Left') else 0
            team_counts[home_team]['Lefties YRSFI'] += 1 if (home_runs > 0) and (away_pitcher_throw == 'Left') else 0


            # Update intradivision counts
            if intradivision_game:
                team_counts[away_team]['Intra NRFI'] += 1 if (home_runs + away_runs) == 0 else 0
                team_counts[away_team]['Intra YRFI'] += 1 if (home_runs + away_runs) > 0 else 0
                team_counts[away_team]['Intra NRSFI'] += 1 if away_runs == 0 else 0
                team_counts[away_team]['Intra YRSFI'] += 1 if away_runs > 0 else 0

                team_counts[home_team]['Intra NRFI'] += 1 if (home_runs + away_runs) == 0 else 0
                team_counts[home_team]['Intra YRFI'] += 1 if (home_runs + away_runs) > 0 else 0
                team_counts[home_team]['Intra NRSFI'] += 1 if home_runs == 0 else 0
                team_counts[home_team]['Intra YRSFI'] += 1 if home_runs > 0 else 0

            # Update pitcher counts
            pitcher_counts[away_pitcher]['Away'] += 1
            pitcher_counts[away_pitcher]['Away RA'] += away_pitcher_runs
            pitcher_counts[away_pitcher]['Away NRFI'] += 1 if away_pitcher_runs == 0 else 0
            pitcher_counts[away_pitcher]['Away YRFI'] += 1 if away_pitcher_runs > 0 else 0
            pitcher_counts[away_pitcher]['Throw'] = away_pitcher_throw
            pitcher_counts[away_pitcher]['Season ERA'] = away_pitcher_era

            pitcher_counts[home_pitcher]['Home'] += 1
            pitcher_counts[home_pitcher]['Home RA'] += home_pitcher_runs
            pitcher_counts[home_pitcher]['Home NRFI'] += 1 if home_pitcher_runs == 0 else 0
            pitcher_counts[home_pitcher]['Home YRFI'] += 1 if home_pitcher_runs > 0 else 0
            pitcher_counts[home_pitcher]['Throw'] = home_pitcher_throw
            pitcher_counts[home_pitcher]['Season ERA'] = home_pitcher_era

            # Update total NRFI and YRFI for pitchers
            pitcher_counts[away_pitcher]['Total NRFI'] = pitcher_counts[away_pitcher]['Away NRFI'] + pitcher_counts[away_pitcher]['Home NRFI']
            pitcher_counts[away_pitcher]['Total YRFI'] = pitcher_counts[away_pitcher]['Away YRFI'] + pitcher_counts[away_pitcher]['Home YRFI']

            pitcher_counts[home_pitcher]['Total NRFI'] = pitcher_counts[home_pitcher]['Away NRFI'] + pitcher_counts[home_pitcher]['Home NRFI']
            pitcher_counts[home_pitcher]['Total YRFI'] = pitcher_counts[home_pitcher]['Away YRFI'] + pitcher_counts[home_pitcher]['Home YRFI']

            # Update the last 10 NRSFI results for both teams
            team_counts[away_team]['L10 NRSFI'].append(1 if away_runs == 0 else 0)
            team_counts[home_team]['L10 NRSFI'].append(1 if home_runs == 0 else 0)
            pitcher_counts[away_pitcher]['L5 NRFI'].append(1 if home_runs == 0 else 0)
            pitcher_counts[home_pitcher]['L5 NRFI'].append(1 if away_runs == 0 else 0)


            # Update NRSFI and YRSFI streaks for both teams
            if away_runs == 0:
                team_counts[away_team]['NRSFI Streak'] += 1
                team_counts[away_team]['YRSFI Streak'] = 0
                pitcher_counts[home_pitcher]['NRFI Streak'] += 1
                pitcher_counts[home_pitcher]['YRFI Streak'] = 0
            else:
                team_counts[away_team]['NRSFI Streak'] = 0
                team_counts[away_team]['YRSFI Streak'] += 1
                pitcher_counts[home_pitcher]['NRFI Streak'] = 0
                pitcher_counts[home_pitcher]['YRFI Streak'] += 1

            if home_runs == 0:
                team_counts[home_team]['NRSFI Streak'] += 1
                team_counts[home_team]['YRSFI Streak'] = 0
                pitcher_counts[away_pitcher]['NRFI Streak'] += 1
                pitcher_counts[away_pitcher]['YRFI Streak'] = 0
            else:
                team_counts[home_team]['NRSFI Streak'] = 0
                team_counts[home_team]['YRSFI Streak'] += 1
                pitcher_counts[away_pitcher]['NRFI Streak'] = 0
                pitcher_counts[away_pitcher]['YRFI Streak'] += 1

    # Calculate L10 streak for each team
    for team, counts in team_counts.items():
        counts['L10 Streak'] = calculate_l10_streak(counts['L10 NRSFI'])

    for pitcher, counts in pitcher_counts.items():
        counts['L5 Streak'] = calculate_l5_streak(counts['L5 NRFI'])

    return team_counts, pitcher_counts


# Function to calculate the L10 streak for a team
def calculate_l10_streak(l10_nrsfi):
    return sum(l10_nrsfi)


def calculate_l5_streak(l5_nrfi):
    return sum(l5_nrfi)


# Function to save team counts to CSV
def save_team_counts_to_csv(filename, team_counts):
    # Write to the CSV file
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write header
        writer.writerow([
            'Name', 'Away', 'Away RS', 'Away RA', 'Away NRFI', 'Away YRFI', 'Away NRSFI', 'Away YRSFI',
            'Home', 'Home RS', 'Home RA', 'Home NRFI', 'Home YRFI', 'Home NRSFI', 'Home YRSFI',
            'Total NRFI', 'Total YRFI', 'Total NRSFI', 'Total YRSFI',
            'Intra NRFI', 'Intra YRFI', 'Intra NRSFI', 'Intra YRSFI',
            'Righties NRSFI', 'Righties YRSFI',
            'Lefties NRSFI', 'Lefties YRSFI',
            'L10 Streak',  # Add L10 Streak column
            'NRSFI Streak', 'YRSFI Streak'
        ])



        # Write team counts
        for team, counts in team_counts.items():
            writer.writerow([
                team,
                counts['Away'],
                counts['Away RS'],
                counts['Away RA'],
                counts['Away NRFI'],
                counts['Away YRFI'],
                counts['Away NRSFI'],
                counts['Away YRSFI'],
                counts['Home'],
                counts['Home RS'],
                counts['Home RA'],
                counts['Home NRFI'],
                counts['Home YRFI'],
                counts['Home NRSFI'],
                counts['Home YRSFI'],
                counts['Total NRFI'],
                counts['Total YRFI'],
                counts['Total NRSFI'],
                counts['Total YRSFI'],
                counts['Intra NRFI'],
                counts['Intra YRFI'],
                counts['Intra NRSFI'],
                counts['Intra YRSFI'],
                counts['Righties NRSFI'],
                counts['Righties YRSFI'],
                counts['Lefties NRSFI'],
                counts['Lefties YRSFI'],
                counts['L10 Streak'],
                counts['NRSFI Streak'],
                counts['YRSFI Streak']
            ])

# Function to save pitcher counts to CSV
def save_pitcher_counts_to_csv(filename, pitcher_counts):
    # Write to the CSV file
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write header
        writer.writerow([
            'Name', 'Away', 'Away RA', 'Away NRFI', 'Away YRFI', 'Away ERA',
            'Home', 'Home RA', 'Home NRFI', 'Home YRFI', 'Home ERA',
            'Total NRFI', 'Total YRFI', 'Throw', 'Season ERA',
            'L5 Streak',
            'NRFI Streak', 'YRFI Streak'
        ])

        # Write pitcher counts
        for pitcher, counts in pitcher_counts.items():
            away_era = round(counts['Away RA'] * 9 / counts['Away'], 2) if counts['Away'] > 0 else 0
            home_era = round(counts['Home RA'] * 9 / counts['Home'], 2) if counts['Home'] > 0 else 0
            writer.writerow([
                pitcher,
                counts['Away'],
                counts['Away RA'],
                counts['Away NRFI'],
                counts['Away YRFI'],
                away_era,
                counts['Home'],
                counts['Home RA'],
                counts['Home NRFI'],
                counts['Home YRFI'],
                home_era,
                counts['Total NRFI'],
                counts['Total YRFI'],
                counts['Throw'],
                counts['Season ERA'],
                counts['L5 Streak'],
                counts['NRFI Streak'],
                counts['YRFI Streak']
            ])

def main():
    input_filename = 'mlb_fi_gamelog.csv'
    team_output_filename = 'mlb_fi_team_data.csv'
    pitcher_output_filename = 'mlb_fi_pitcher_data.csv'

    team_counts, pitcher_counts = count_appearances(input_filename)
    save_team_counts_to_csv(team_output_filename, team_counts)
    save_pitcher_counts_to_csv(pitcher_output_filename, pitcher_counts)

if __name__ == '__main__':
    main()
