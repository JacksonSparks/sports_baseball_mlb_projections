from flask import Flask, render_template
import pandas as pd
import datetime
import unicodedata
import math

app = Flask(__name__)


# Define divisions
divisions = {
    'AL West': ['Mariners', 'Astros', 'Rangers', 'Angels', 'Athletics'],
    'AL East': ['Yankees', 'Red Sox', 'Blue Jays', 'Rays', 'Orioles'],
    'AL Central': ['White Sox', 'Guardians', 'Tigers', 'Royals', 'Twins'],
    'NL West': ['Dodgers', 'Giants', 'Padres', 'Diamondbacks', 'Rockies'],
    'NL East': ['Braves', 'Mets', 'Phillies', 'Marlins', 'Nationals'],
    'NL Central': ['Cubs', 'Cardinals', 'Brewers', 'Pirates', 'Reds']
}

def format_pitcher_name(name):
    """
    Convert pitcher name from 'First Last' to 'F. Last' and handle three-word names.
    Handles special characters by normalizing to ASCII.
    """
    # Normalize the name to remove accents and other diacritics
    normalized_name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')

    # # Split the normalized name into parts
    # parts = normalized_name.split()
    #
    # if len(parts) == 2:
    #     return f"{parts[0][0]}. {parts[1]}"
    # elif len(parts) == 3:
    #     return f"{parts[0][0]}. {parts[1]} {parts[2]}"
    return normalized_name

def calculate_min_max(df, column):
    """Calculate the min and max values of a column in a DataFrame."""
    if column in df:
        return df[column].min(), df[column].max()
    return None, None

def calculate_color(value, min_val, max_val, inverse=False):
    """Calculate color based on value, min, and max."""
    if value == 'N/A' or pd.isna(value):
        return '#ffffff'
    ratio = (value - min_val) / (max_val - min_val)
    if inverse:
        green = int(255 * ratio)
        red = int(255 * (1 - ratio))
    else:
        green = int(255 * (1 - ratio))
        red = int(255 * ratio)
    return f'rgb({red},{green},0)'

def calculate_nrfi_color(value, min_val=0, max_val=100):
    """Calculate color for NRFI percentages based on a fixed scale (0 to 100)."""
    if value == 'N/A' or pd.isna(value):
        return '#ffffff'  # White for 'N/A' values

    # Ensure value is within the min-max range
    try:
        value = float(value)
    except ValueError:
        return '#ffffff'  # Return white for invalid numbers

    if value < min_val:
        value = min_val
    elif value > max_val:
        value = max_val

    # Scale value from 0 to 255 for color gradient
    ratio = (value - min_val) / (max_val - min_val)
    green = int(255 * ratio)   # Higher percentage (closer to 100) is more green
    red = int(255 * (1 - ratio))  # Lower percentage (closer to 0) is more red

    return f'rgb({red},{green},0)'

def calculate_nrsfi_color(value, min_val=50, max_val=100):
    """Calculate color for NRFI percentages based on a fixed scale (0 to 100)."""
    if value == 'N/A' or pd.isna(value):
        return '#ffffff'  # White for 'N/A' values

    # Ensure value is within the min-max range
    try:
        value = float(value)
    except ValueError:
        return '#ffffff'  # Return white for invalid numbers

    if value < min_val:
        value = min_val
    elif value > max_val:
        value = max_val

    # Scale value from 0 to 255 for color gradient
    ratio = (value - min_val) / (max_val - min_val)
    green = int(255 * ratio)   # Higher percentage (closer to 100) is more green
    red = int(255 * (1 - ratio))  # Lower percentage (closer to 0) is more red

    return f'rgb({red},{green},0)'

def calculate_era_color(value, min_val=0, max_val=9):
    """Calculate color based on a scaled value from 0 to 9."""
    if value == 'N/A' or pd.isna(value):
        return '#ffffff'  # White for 'N/A' values

    # Convert value to a float
    try:
        value = float(value)
    except ValueError:
        return '#ffffff'  # Return white for invalid numbers

    # Ensure value is within the min-max range
    if value < min_val:
        value = min_val
    elif value > max_val:
        value = max_val

    # Scale value from 0 to 9
    scaled_value = 9 * (value - min_val) / (max_val - min_val)
    scaled_value = min(max(scaled_value, 0), 9)  # Ensure the value is between 0 and 9

    # Map scaled value to a color gradient
    red = int(255 * (scaled_value / 9))
    green = int(255 * (1 - scaled_value / 9))

    return f'rgb({red},{green},0)'

def calculate_streak_color(value):
    if value > 0:
        return '#00FF00'
    else:
        return '#FF0000'



@app.route('/')
def display_data():
    # Load data from the existing CSV files
    matchups_df = pd.read_csv('mlb_pitcher_matchups.csv')
    team_data_df = pd.read_csv('mlb_fi_team_data.csv')
    pitcher_data_df = pd.read_csv('mlb_fi_pitcher_data.csv')

    # Calculate min and max values for relevant columns
    team_min_max = {
        'Away RS': calculate_min_max(team_data_df, 'Away RS'),
        'Away NRFI': calculate_min_max(team_data_df, 'Away NRFI'),
        'Away YRFI': calculate_min_max(team_data_df, 'Away YRFI'),

        'Home RS': calculate_min_max(team_data_df, 'Home RS'),
        'Home NRFI': calculate_min_max(team_data_df, 'Home NRFI'),
        'Home YRFI': calculate_min_max(team_data_df, 'Home YRFI')
    }

    pitcher_min_max = {
        'Away ERA': calculate_min_max(pitcher_data_df, 'Away ERA'),
        'Away RA': calculate_min_max(pitcher_data_df, 'Away RA'),
        'Away NRFI': calculate_min_max(pitcher_data_df, 'Away NRFI'),
        'Away YRFI': calculate_min_max(pitcher_data_df, 'Away YRFI'),
        'Away Total NRFI': calculate_min_max(pitcher_data_df, 'Total NRFI'),
        'Away Total YRFI': calculate_min_max(pitcher_data_df, 'Total YRFI'),

        'Home ERA': calculate_min_max(pitcher_data_df, 'Home ERA'),
        'Home RA': calculate_min_max(pitcher_data_df, 'Home RA'),
        'Home NRFI': calculate_min_max(pitcher_data_df, 'Home NRFI'),
        'Home YRFI': calculate_min_max(pitcher_data_df, 'Home YRFI'),
        'Home Total NRFI': calculate_min_max(pitcher_data_df, 'Total NRFI'),
        'Home Total YRFI': calculate_min_max(pitcher_data_df, 'Total YRFI')
    }

    # Prepare a list to store the updated rows
    updated_data = []

    # Iterate over the rows in mlb_pitcher_matchups.csv
    for _, row in matchups_df.iterrows():
        away_team = row['Away Team']
        home_team = row['Home Team']
        away_pitcher = row['Away Pitcher']
        home_pitcher = row['Home Pitcher']

        # Extract the data for the away team from mlb_team_data.csv
        away_team_data = team_data_df[team_data_df['Name'] == away_team]
        if not away_team_data.empty:
            away_team_data = away_team_data.iloc[0]
            away_team_rs = away_team_data['Away RS']
            away_team_nrfi = away_team_data['Away NRFI']
            away_team_yrfi = away_team_data['Away YRFI']
            away_team_nrsfi = away_team_data['Away NRSFI']
            away_team_yrsfi = away_team_data['Away YRSFI']
            away_team_total_nrfi = away_team_data['Total NRFI']
            away_team_total_yrfi = away_team_data['Total YRFI']
            away_team_total_nrsfi = away_team_data['Total NRSFI']
            away_team_total_yrsfi = away_team_data['Total YRSFI']
            away_team_right_nrsfi = away_team_data['Righties NRSFI']
            away_team_right_yrsfi = away_team_data['Righties YRSFI']
            away_team_left_nrsfi = away_team_data['Lefties NRSFI']
            away_team_left_yrsfi = away_team_data['Lefties YRSFI']
            away_team_intra_nrsfi = away_team_data['Intra NRSFI']
            away_team_intra_yrsfi = away_team_data['Intra YRSFI']
            away_team_l10_games = away_team_data['L10 Streak']
            away_team_nrsfi_streak = away_team_data['NRSFI Streak']
            away_team_yrsfi_streak = away_team_data['YRSFI Streak']
        else:
            away_team_rs = away_team_nrfi = away_team_yrfi = away_team_nrsfi = away_team_yrsfi = away_team_total_nrfi = away_team_total_yrfi = away_team_total_nrsfi = away_team_total_yrsfi = away_team_right_nrsfi = away_team_right_yrsfi = away_team_left_nrsfi = away_team_left_yrsfi = away_team_intra_nrsfi = away_team_intra_yrsfi = away_team_l10_games = away_team_nrsfi_streak = away_team_yrsfi_streak = 'N/A'

        # Extract the data for the home team from mlb_team_data.csv
        home_team_data = team_data_df[team_data_df['Name'] == home_team]
        if not home_team_data.empty:
            home_team_data = home_team_data.iloc[0]
            home_team_rs = home_team_data['Home RS']
            home_team_nrfi = home_team_data['Home NRFI']
            home_team_yrfi = home_team_data['Home YRFI']
            home_team_nrsfi = home_team_data['Home NRSFI']
            home_team_yrsfi = home_team_data['Home YRSFI']
            home_team_total_nrfi = home_team_data['Total NRFI']
            home_team_total_yrfi = home_team_data['Total YRFI']
            home_team_total_nrsfi = home_team_data['Total NRSFI']
            home_team_total_yrsfi = home_team_data['Total YRSFI']
            home_team_right_nrsfi = home_team_data['Righties NRSFI']
            home_team_right_yrsfi = home_team_data['Righties YRSFI']
            home_team_left_nrsfi = home_team_data['Lefties NRSFI']
            home_team_left_yrsfi = home_team_data['Lefties YRSFI']
            home_team_intra_nrsfi = home_team_data['Intra NRSFI']
            home_team_intra_yrsfi = home_team_data['Intra YRSFI']
            home_team_l10_games = home_team_data['L10 Streak']
            home_team_nrsfi_streak = home_team_data['NRSFI Streak']
            home_team_yrsfi_streak = home_team_data['YRSFI Streak']
        else:
            home_team_rs = home_team_nrfi = home_team_yrfi = home_team_nrsfi = home_team_yrsfi = home_team_total_nrfi = home_team_total_yrfi = home_team_total_nrsfi = home_team_total_yrsfi = home_team_right_nrsfi = home_team_right_yrsfi = home_team_left_nrsfi = home_team_left_yrsfi = home_team_intra_nrsfi = home_team_intra_yrsfi = home_team_l10_games = home_team_nrsfi_streak = home_team_yrsfi_streak = 'N/A'

        # Format pitcher names for matching
        formatted_away_pitcher = format_pitcher_name(away_pitcher)
        formatted_home_pitcher = format_pitcher_name(home_pitcher)

        # Extract the data for the away pitcher from mlb_pitcher_data.csv
        away_pitcher_data = pitcher_data_df[pitcher_data_df['Name'] == formatted_away_pitcher]
        if not away_pitcher_data.empty:
            away_pitcher_data = away_pitcher_data.iloc[0]
            away_era = away_pitcher_data['Away ERA']
            away_ra = away_pitcher_data['Away RA']
            away_nrfi = away_pitcher_data['Away NRFI']
            away_yrfi = away_pitcher_data['Away YRFI']
            away_total_nrfi = away_pitcher_data['Total NRFI']
            away_total_yrfi = away_pitcher_data['Total YRFI']
            away_throw = away_pitcher_data['Throw']
            away_pitcher_l5_games = away_pitcher_data['L5 Streak']
            away_pitcher_nrfi_streak = away_pitcher_data['NRFI Streak']
            away_pitcher_yrfi_streak = away_pitcher_data['YRFI Streak']
        else:
            away_era = away_ra = away_nrfi = away_yrfi = away_total_nrfi = away_total_yrfi = away_throw = away_pitcher_l5_games = away_pitcher_nrfi_streak = away_pitcher_yrfi_streak = 'N/A'

        # Extract the data for the home pitcher from mlb_pitcher_data.csv
        home_pitcher_data = pitcher_data_df[pitcher_data_df['Name'] == formatted_home_pitcher]
        if not home_pitcher_data.empty:
            home_pitcher_data = home_pitcher_data.iloc[0]
            home_era = home_pitcher_data['Home ERA']
            home_ra = home_pitcher_data['Home RA']
            home_nrfi = home_pitcher_data['Home NRFI']
            home_yrfi = home_pitcher_data['Home YRFI']
            home_total_nrfi = home_pitcher_data['Total NRFI']
            home_total_yrfi = home_pitcher_data['Total YRFI']
            home_throw = home_pitcher_data['Throw']
            home_pitcher_l5_games = home_pitcher_data['L5 Streak']
            home_pitcher_nrfi_streak = home_pitcher_data['NRFI Streak']
            home_pitcher_yrfi_streak = home_pitcher_data['YRFI Streak']
        else:
            home_era = home_ra = home_nrfi = home_yrfi = home_total_nrfi = home_total_yrfi = home_throw = home_pitcher_l5_games = home_pitcher_nrfi_streak = home_pitcher_yrfi_streak = 'N/A'

        # Calculate colors
        away_rs_color = calculate_color(away_team_rs, team_min_max['Away RS'][0], team_min_max['Away RS'][1])

        home_rs_color = calculate_color(home_team_rs, team_min_max['Home RS'][0], team_min_max['Home RS'][1])

        away_ra_pitcher_color = calculate_color(away_ra, pitcher_min_max['Away RA'][0], pitcher_min_max['Away RA'][1])
        away_nrfi_pitcher_color = calculate_color(away_nrfi, pitcher_min_max['Away NRFI'][0], pitcher_min_max['Away NRFI'][1], inverse=True)
        away_yrfi_pitcher_color = calculate_color(away_yrfi, pitcher_min_max['Away YRFI'][0], pitcher_min_max['Away YRFI'][1])
        home_ra_pitcher_color = calculate_color(home_ra, pitcher_min_max['Home RA'][0], pitcher_min_max['Home RA'][1])
        home_nrfi_pitcher_color = calculate_color(home_nrfi, pitcher_min_max['Home NRFI'][0], pitcher_min_max['Home NRFI'][1], inverse=True)
        home_yrfi_pitcher_color = calculate_color(home_yrfi, pitcher_min_max['Home YRFI'][0], pitcher_min_max['Home YRFI'][1])

        # Calculate NRFI percentages
        away_nrfi_percent = round((away_team_nrfi / (away_team_nrfi + away_team_yrfi)) * 100) if (away_team_nrfi != 'N/A' and away_team_yrfi != 'N/A') else 'N/A'
        home_nrfi_percent = round((home_team_nrfi / (home_team_nrfi + home_team_yrfi)) * 100) if (home_team_nrfi != 'N/A' and home_team_yrfi != 'N/A') else 'N/A'
        away_nrsfi_percent = round((away_team_nrsfi / (away_team_nrsfi + away_team_yrsfi)) * 100) if (away_team_nrsfi != 'N/A' and away_team_yrsfi != 'N/A') else 'N/A'
        home_nrsfi_percent = round((home_team_nrsfi / (home_team_nrsfi + home_team_yrsfi)) * 100) if (home_team_nrsfi != 'N/A' and home_team_yrsfi != 'N/A') else 'N/A'
        away_total_nrfi_percent = round((away_team_total_nrfi / (away_team_total_nrfi + away_team_total_yrfi)) * 100) if (away_team_total_nrfi != 'N/A' and away_team_total_yrfi != 'N/A') else 'N/A'
        home_total_nrfi_percent = round((home_team_total_nrfi / (home_team_total_nrfi + home_team_total_yrfi)) * 100) if (home_team_total_nrfi != 'N/A' and home_team_total_yrfi != 'N/A') else 'N/A'
        away_total_nrsfi_percent = round((away_team_total_nrsfi / (away_team_total_nrsfi + away_team_total_yrsfi)) * 100) if (away_team_total_nrsfi != 'N/A' and away_team_total_yrsfi != 'N/A') else 'N/A'
        home_total_nrsfi_percent = round((home_team_total_nrsfi / (home_team_total_nrsfi + home_team_total_yrsfi)) * 100) if (home_team_total_nrsfi != 'N/A' and home_team_total_yrsfi != 'N/A') else 'N/A'
        # away_intra_nrsfi_percent = round((away_team_intra_nrsfi / (away_team_intra_nrsfi + away_team_intra_yrsfi)) * 100) if (away_team_intra_nrsfi != 'N/A' and away_team_intra_yrsfi != 'N/A') else 'N/A'
        # home_intra_nrsfi_percent = round((home_team_intra_nrsfi / (home_team_intra_nrsfi + home_team_intra_yrsfi)) * 100) if (home_team_intra_nrsfi != 'N/A' and home_team_intra_yrsfi != 'N/A') else 'N/A'


        team_to_division = {}
        for division, teams in divisions.items():
            for team in teams:
                team_to_division[team] = division

        intradivision_game = team_to_division[away_team] == team_to_division[home_team]

        if intradivision_game:
            if away_team_intra_nrsfi != 'N/A' and away_team_intra_yrsfi != 'N/A':
                away_intra_nrsfi_percent = round((away_team_intra_nrsfi / (away_team_intra_nrsfi + away_team_intra_yrsfi)) * 100)
            else:
                away_intra_nrsfi_percent = 'N/A'

            if home_team_intra_nrsfi != 'N/A' and home_team_intra_yrsfi != 'N/A':
                home_intra_nrsfi_percent = round((home_team_intra_nrsfi / (home_team_intra_nrsfi + home_team_intra_yrsfi)) * 100)
            else:
                home_intra_nrsfi_percent = 'N/A'
        else:
            away_intra_nrsfi_percent = 'N/A'
            home_intra_nrsfi_percent = 'N/A'


        away_throw_nrsfi_percent = (
            round((away_team_right_nrsfi / (away_team_right_nrsfi + away_team_right_yrsfi)) * 100)
            if (home_throw == "Right" and away_team_right_nrsfi != 'N/A' and away_team_right_yrsfi != 'N/A')
            else (
                round((away_team_left_nrsfi / (away_team_left_nrsfi + away_team_left_yrsfi)) * 100)
                if (home_throw == "Left" and away_team_left_nrsfi != 'N/A' and away_team_left_yrsfi != 'N/A')
                else 'N/A'
            )
        )
        home_throw_nrsfi_percent = (
            round((home_team_right_nrsfi / (home_team_right_nrsfi + home_team_right_yrsfi)) * 100)
            if (away_throw == "Right" and home_team_right_nrsfi != 'N/A' and home_team_right_yrsfi != 'N/A')
            else (
                round((home_team_left_nrsfi / (home_team_left_nrsfi + home_team_left_yrsfi)) * 100)
                if (away_throw == "Left" and home_team_left_nrsfi != 'N/A' and home_team_left_yrsfi != 'N/A')
                else 'N/A'
            )
        )


        away_nrfi_pitcher_percent = round((away_nrfi / (away_nrfi + away_yrfi)) * 100, 1) if (away_nrfi != 'N/A' and away_yrfi != 'N/A') else 'N/A'
        home_nrfi_pitcher_percent = round((home_nrfi / (home_nrfi + home_yrfi)) * 100, 1) if (home_nrfi != 'N/A' and home_yrfi != 'N/A') else 'N/A'
        away_total_nrfi_pitcher_percent = round((away_total_nrfi / (away_total_nrfi + away_total_yrfi)) * 100, 1) if (away_total_nrfi != 'N/A' and away_total_yrfi != 'N/A') else 'N/A'
        home_total_nrfi_pitcher_percent = round((home_total_nrfi / (home_total_nrfi + home_total_yrfi)) * 100, 1) if (home_total_nrfi != 'N/A' and home_total_yrfi != 'N/A') else 'N/A'
        nrfi_pitchers_percent = round(home_nrfi_pitcher_percent * away_nrfi_pitcher_percent / 100) if (home_nrfi_pitcher_percent != 'N/A' and not pd.isna(home_nrfi_pitcher_percent) and away_nrfi_pitcher_percent != 'N/A' and not pd.isna(away_nrfi_pitcher_percent)) else 'N/A'



    # Calculate colors based on NRFI percentages
        away_nrfi_percent_color = calculate_nrfi_color(away_nrfi_percent)
        home_nrfi_percent_color = calculate_nrfi_color(home_nrfi_percent)
        away_nrsfi_percent_color = calculate_nrsfi_color(away_nrsfi_percent)
        home_nrsfi_percent_color = calculate_nrsfi_color(home_nrsfi_percent)
        away_total_nrfi_percent_color = calculate_nrfi_color(away_total_nrfi_percent)
        home_total_nrfi_percent_color = calculate_nrfi_color(home_total_nrfi_percent)
        away_total_nrsfi_percent_color = calculate_nrsfi_color(away_total_nrsfi_percent)
        home_total_nrsfi_percent_color = calculate_nrsfi_color(home_total_nrsfi_percent)
        away_throw_nrsfi_percent_color = calculate_nrsfi_color(away_throw_nrsfi_percent)
        home_throw_nrsfi_percent_color = calculate_nrsfi_color(home_throw_nrsfi_percent)
        away_intra_nrsfi_percent_color = calculate_nrsfi_color(away_intra_nrsfi_percent)
        home_intra_nrsfi_percent_color = calculate_nrsfi_color(home_intra_nrsfi_percent)


        away_nrfi_pitcher_percent_color = calculate_nrfi_color(away_nrfi_pitcher_percent)
        home_nrfi_pitcher_percent_color = calculate_nrfi_color(home_nrfi_pitcher_percent)
        away_total_nrfi_pitcher_percent_color = calculate_nrfi_color(away_total_nrfi_pitcher_percent)
        home_total_nrfi_pitcher_percent_color = calculate_nrfi_color(home_total_nrfi_pitcher_percent)
        nrfi_pitchers_percent_color = calculate_nrfi_color(nrfi_pitchers_percent)

        # Calculate colors based on ERA
        away_era_color = calculate_era_color(away_era)
        home_era_color = calculate_era_color(home_era)

        if home_team_nrsfi_streak > 0:
            home_streak = home_team_nrsfi_streak
        else:
            home_streak = home_team_yrsfi_streak

        if away_team_nrsfi_streak > 0:
            away_streak = away_team_nrsfi_streak
        else:
            away_streak = away_team_yrsfi_streak

        home_streak_color = calculate_streak_color(home_team_nrsfi_streak)
        away_streak_color = calculate_streak_color(away_team_nrsfi_streak)

        if home_pitcher_nrfi_streak != 'N/A' and home_pitcher_nrfi_streak > 0:
            home_pitcher_streak = home_pitcher_nrfi_streak
        elif home_pitcher_yrfi_streak != 'N/A':
            home_pitcher_streak = home_pitcher_yrfi_streak
        else:
            home_pitcher_streak = 'N/A'

        if away_pitcher_nrfi_streak != 'N/A' and away_pitcher_nrfi_streak > 0:
            away_pitcher_streak = away_pitcher_nrfi_streak
        elif away_pitcher_yrfi_streak != 'N/A':
            away_pitcher_streak = away_pitcher_yrfi_streak
        else:
            away_pitcher_streak = 'N/A'

        if home_pitcher_streak != 'N/A':
            home_pitcher_streak_color = calculate_streak_color(home_pitcher_nrfi_streak)
        else:
            home_pitcher_streak_color = 'N/A'

        if away_pitcher_streak != 'N/A':
            away_pitcher_streak_color = calculate_streak_color(away_pitcher_nrfi_streak)
        else:
            away_pitcher_streak_color = 'N/A'











        def safe_float(value):
            try:
                return float(value)
            except (ValueError, TypeError):
                return float('nan')  # or a default value like 0

        algo_away_pitcher = 'N/A'
        algo_home_pitcher = 'N/A'
        algo_away_team = 'N/A'
        algo_home_team = 'N/A'

        if away_nrfi_pitcher_percent != 'N/A':
            away_nrfi_pitcher_percent = safe_float(away_nrfi_pitcher_percent)
            away_total_nrfi_pitcher_percent = safe_float(away_total_nrfi_pitcher_percent)
            if (away_nrfi+away_yrfi) >= 2 and (away_total_nrfi+away_total_yrfi) >= 5:
                if away_pitcher_nrfi_streak > 0:
                    algo_away_pitcher = ((away_nrfi_pitcher_percent * 2) + away_total_nrfi_pitcher_percent) / 3 + (3 * (away_pitcher_nrfi_streak - 3.5)) + (1 / 3 * (away_pitcher_nrfi_streak))
                elif away_pitcher_yrfi_streak > 0:
                    algo_away_pitcher = ((away_nrfi_pitcher_percent * 2) + away_total_nrfi_pitcher_percent) / 3 + (3 * (away_pitcher_l5_games - 3.5)) - (1 * (away_pitcher_yrfi_streak))

        if home_nrfi_pitcher_percent != 'N/A':
            home_nrfi_pitcher_percent = safe_float(home_nrfi_pitcher_percent)
            home_total_nrfi_pitcher_percent = safe_float(home_total_nrfi_pitcher_percent)
            if (home_nrfi+home_yrfi) >= 2 and (home_total_nrfi+home_total_yrfi) >= 5:
                if home_pitcher_nrfi_streak > 0:
                    algo_home_pitcher = ((home_nrfi_pitcher_percent * 2) + home_total_nrfi_pitcher_percent) / 3 + (3 * (home_pitcher_l5_games - 3.5)) + (1 / 3 * (home_pitcher_nrfi_streak))
                elif home_pitcher_yrfi_streak > 0:
                    algo_home_pitcher = ((home_nrfi_pitcher_percent * 2) + home_total_nrfi_pitcher_percent) / 3 + (3 * (home_pitcher_l5_games - 3.5)) - (1 * (home_pitcher_yrfi_streak))

        # Convert all necessary variables to floats
        away_throw_nrsfi_percent = safe_float(away_throw_nrsfi_percent)
        away_nrsfi_percent = safe_float(away_nrsfi_percent)
        away_intra_nrsfi_percent = safe_float(away_intra_nrsfi_percent)
        home_throw_nrsfi_percent = safe_float(home_throw_nrsfi_percent)
        home_nrsfi_percent = safe_float(home_nrsfi_percent)
        home_intra_nrsfi_percent = safe_float(home_intra_nrsfi_percent)

        if away_team_nrsfi_streak > 0:
            if not math.isnan(away_intra_nrsfi_percent):
                algo_away_team = ((away_throw_nrsfi_percent + away_nrsfi_percent) / 2 + away_intra_nrsfi_percent) / 2 + (2 * (away_team_l10_games - 7)) + (1 / 2 * (away_team_nrsfi_streak))
            else:
                algo_away_team = ((away_throw_nrsfi_percent + away_nrsfi_percent) / 2) + (2 * (away_team_l10_games - 7)) + (1 / 2 * (away_team_nrsfi_streak))
        elif away_team_yrsfi_streak > 0:
            if not math.isnan(away_intra_nrsfi_percent):
                algo_away_team = ((away_throw_nrsfi_percent + away_nrsfi_percent) / 2 + away_intra_nrsfi_percent) / 2 + (2 * (away_team_l10_games - 7)) - (1 / 2 * (away_team_yrsfi_streak))
            else:
                algo_away_team = ((away_throw_nrsfi_percent + away_nrsfi_percent) / 2) + (2 * (away_team_l10_games - 7)) - (1 / 2 * (away_team_yrsfi_streak))

        if home_team_nrsfi_streak > 0:
            if not math.isnan(home_intra_nrsfi_percent):
                algo_home_team = ((home_throw_nrsfi_percent + home_nrsfi_percent) / 2 + home_intra_nrsfi_percent) / 2 + (2 * (home_team_l10_games - 7)) + (1 / 2 * (home_team_nrsfi_streak))
            else:
                algo_home_team = ((home_throw_nrsfi_percent + home_nrsfi_percent) / 2) + (2 * (home_team_l10_games - 7)) + (1 / 2 * (home_team_nrsfi_streak))
        elif home_team_yrsfi_streak > 0:
            if not math.isnan(home_intra_nrsfi_percent):
                algo_home_team = ((home_throw_nrsfi_percent + home_nrsfi_percent) / 2 + home_intra_nrsfi_percent) / 2 + (2 * (home_team_l10_games - 7)) - (1 / 2 * (home_team_yrsfi_streak))
            else:
                algo_home_team = ((home_throw_nrsfi_percent + home_nrsfi_percent) / 2) + (2 * (home_team_l10_games - 7)) - (1 / 2 * (home_team_yrsfi_streak))



        if algo_away_pitcher != 'N/A' and algo_home_team != 'N/A':
            if algo_home_team > 100:
                algo_home_team = 100
            if algo_away_pitcher > 100:
                algo_away_pitcher = 100

            algo_away_pitcher = safe_float(algo_away_pitcher) / 100
            algo_home_team = safe_float(algo_home_team) / 100

            home_algo_percentage = round(((algo_home_team + algo_away_pitcher)/2) * 100, 1)
        else:
            home_algo_percentage = 'N/A'


        if algo_home_pitcher != 'N/A' and algo_away_team != 'N/A':
            if algo_away_team > 100:
                algo_away_team = 100
            if algo_home_pitcher > 100:
                algo_home_pitcher = 100

            algo_home_pitcher = safe_float(algo_home_pitcher) / 100
            algo_away_team = safe_float(algo_away_team) / 100

            away_algo_percentage = round(((algo_away_team + algo_home_pitcher)/2) * 100, 1)
        else:
            away_algo_percentage = 'N/A'


        if algo_away_pitcher != 'N/A' and algo_home_pitcher != 'N/A' and algo_away_team != 'N/A' and algo_home_team != 'N/A':
            # if algo_away_pitcher > 100:
            #     algo_away_pitcher = 100
            # if algo_home_pitcher > 100:
            #     algo_home_pitcher = 100
            # if algo_away_team > 100:
            #     algo_away_team = 100
            # if algo_home_team > 100:
            #     algo_home_team = 100
            #
            # algo_away_pitcher = safe_float(algo_away_pitcher) / 100
            # algo_home_pitcher = safe_float(algo_home_pitcher) / 100
            # algo_away_team = safe_float(algo_away_team) / 100
            # algo_home_team = safe_float(algo_home_team) / 100
            #
            # home_algo_percentage = round(((algo_home_team + algo_away_pitcher)/2) * 100, 1)
            # away_algo_percentage = round(((algo_away_team + algo_home_pitcher)/2) * 100, 1)
            algo_percentage = round(((algo_home_team + algo_away_pitcher)/2) * ((algo_away_team + algo_home_pitcher)/2) * 100, 1)
        else:
            algo_percentage = 'N/A'
            # home_algo_percentage = 'N/A'
            # away_algo_percentage = 'N/A'




    # Append the row with the extracted data and colors to the updated_data list
        updated_data.append({
            'Away Team': away_team,
            'Away RS': away_team_rs,
            'Away RS Color': away_rs_color,
            'Away NRFI %': away_nrfi_percent,
            'Away NRFI % Color': away_nrfi_percent_color,
            'Away NRSFI %': away_nrsfi_percent,
            'Away NRSFI % Color': away_nrsfi_percent_color,
            'Away Total NRFI %': away_total_nrfi_percent,
            'Away Total NRFI % Color': away_total_nrfi_percent_color,
            'Away Total NRSFI %': away_total_nrsfi_percent,
            'Away Total NRSFI % Color': away_total_nrsfi_percent_color,
            'Away Intra NRSFI %': away_intra_nrsfi_percent,
            'Away Intra NRSFI % Color': away_intra_nrsfi_percent_color,

            'Away Throw NRSFI %': away_throw_nrsfi_percent,
            'Away Throw NRSFI % Color': away_throw_nrsfi_percent_color,
            'Away L10': away_team_l10_games,
            'Away Streak': away_streak,
            'Away Streak Color': away_streak_color,

            'Home Team': home_team,
            'Home RS': home_team_rs,
            'Home RS Color': home_rs_color,
            'Home NRFI %': home_nrfi_percent,
            'Home NRFI % Color': home_nrfi_percent_color,
            'Home NRSFI %': home_nrsfi_percent,
            'Home NRSFI % Color': home_nrsfi_percent_color,
            'Home Total NRFI %': home_total_nrfi_percent,
            'Home Total NRFI % Color': home_total_nrfi_percent_color,
            'Home Total NRSFI %': home_total_nrsfi_percent,
            'Home Total NRSFI % Color': home_total_nrsfi_percent_color,
            'Home Intra NRSFI %': home_intra_nrsfi_percent,
            'Home Intra NRSFI % Color': home_intra_nrsfi_percent_color,

            'Home Throw NRSFI %': home_throw_nrsfi_percent,
            'Home Throw NRSFI % Color': home_throw_nrsfi_percent_color,
            'Home L10': home_team_l10_games,
            'Home Streak': home_streak,
            'Home Streak Color': home_streak_color,

            # 'Away ERA': away_era,
            # 'Away ERA Color': away_era_color,
            'Away Pitcher': away_pitcher,
            # 'Away RA (Pitcher)': away_ra,
            # 'Away RA (Pitcher) Color': away_ra_pitcher_color,
            'Away NRFI (Pitcher)': away_nrfi,
            'Away NRFI (Pitcher) Color': away_nrfi_pitcher_color,
            'Away YRFI (Pitcher)': away_yrfi,
            'Away YRFI (Pitcher) Color': away_yrfi_pitcher_color,
            'Away NRFI % (Pitcher)': away_nrfi_pitcher_percent,
            'Away NRFI % (Pitcher) Color': away_nrfi_pitcher_percent_color,
            'Away Total NRFI (Pitcher)': away_total_nrfi,
            'Away Total YRFI (Pitcher)': away_total_yrfi,
            'Away Total NRFI % (Pitcher)': away_total_nrfi_pitcher_percent,
            'Away Total NRFI % (Pitcher) Color': away_total_nrfi_pitcher_percent_color,
            'Away L5 (Pitcher)': away_pitcher_l5_games,
            'Away Streak (Pitcher)': away_pitcher_streak,
            'Away Streak (Pitcher) Color': away_pitcher_streak_color,

            # 'Home ERA': home_era,
            # 'Home ERA Color': home_era_color,
            'Home Pitcher': home_pitcher,
            # 'Home RA (Pitcher)': home_ra,
            # 'Home RA (Pitcher) Color': home_ra_pitcher_color,
            'Home NRFI (Pitcher)': home_nrfi,
            'Home NRFI (Pitcher) Color': home_nrfi_pitcher_color,
            'Home YRFI (Pitcher)': home_yrfi,
            'Home YRFI (Pitcher) Color': home_yrfi_pitcher_color,
            'Home NRFI % (Pitcher)': home_nrfi_pitcher_percent,
            'Home NRFI % (Pitcher) Color': home_nrfi_pitcher_percent_color,
            'Home Total NRFI (Pitcher)': home_total_nrfi,
            'Home Total YRFI (Pitcher)': home_total_yrfi,
            'Home Total NRFI % (Pitcher)': home_total_nrfi_pitcher_percent,
            'Home Total NRFI % (Pitcher) Color': home_total_nrfi_pitcher_percent_color,
            'Home L5 (Pitcher)': home_pitcher_l5_games,
            'Home Streak (Pitcher)': home_pitcher_streak,
            'Home Streak (Pitcher) Color': home_pitcher_streak_color,

            'NRFI % (Pitchers)': nrfi_pitchers_percent,
            'NRFI % (Pitchers) Color': nrfi_pitchers_percent_color,

            'Away NRSFI Algo Percentage': away_algo_percentage,
            'Home NRSFI Algo Percentage': home_algo_percentage,
            'Algo Percentage': algo_percentage
        })

    # Get the current date
    current_date = datetime.date.today().strftime("%B %d, %Y")

    return render_template('mlb_fi_display_matchups_data.html', data=updated_data, date=current_date)

if __name__ == '__main__':
    app.run(debug=True)
