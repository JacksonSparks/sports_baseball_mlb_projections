from flask import Flask, render_template
import pandas as pd
import datetime

app = Flask(__name__)

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
        return '#ffffff'
    try:
        value = float(value)
    except ValueError:
        return '#ffffff'
    value = max(min_val, min(value, max_val))
    ratio = (value - min_val) / (max_val - min_val)
    green = int(255 * ratio)
    red = int(255 * (1 - ratio))
    return f'rgb({red},{green},0)'


def calculate_nrsfi_color(value, min_val=50, max_val=100):
    """Calculate color for NRFI percentages based on a fixed scale (0 to 100)."""
    if value == 'N/A' or pd.isna(value):
        return '#ffffff'
    try:
        value = float(value)
    except ValueError:
        return '#ffffff'
    value = max(min_val, min(value, max_val))
    ratio = (value - min_val) / (max_val - min_val)
    green = int(255 * ratio)
    red = int(255 * (1 - ratio))
    return f'rgb({red},{green},0)'


def calculate_intra_total_color(value, min_val=-25, max_val=25):
    """Calculate color for NRFI percentages based on a fixed scale (0 to 100)."""
    if value == 'N/A' or pd.isna(value):
        return '#ffffff'
    try:
        value = float(value)
    except ValueError:
        return '#ffffff'
    value = max(min_val, min(value, max_val))
    ratio = (value - min_val) / (max_val - min_val)
    green = int(255 * ratio)
    red = int(255 * (1 - ratio))
    return f'rgb({red},{green},0)'


@app.route('/')
def display_data():
    team_data_df = pd.read_csv('mlb_fi_team_data.csv')
    team_min_max = {col: calculate_min_max(team_data_df, col) for col in team_data_df.columns if col not in ['Name']}

    updated_data = []
    for _, row in team_data_df.iterrows():
        team = row['Name']
        away_data = team_data_df[team_data_df['Name'] == team]
        home_data = team_data_df[team_data_df['Name'] == team]
        total_data = team_data_df[team_data_df['Name'] == team]

        if not away_data.empty:
            away_data = away_data.iloc[0]
            away_rs, away_ra, away_nrfi, away_yrfi = away_data[['Away RS', 'Away RA', 'Away NRFI', 'Away YRFI']]
            away_nrsfi, away_yrsfi = away_data[['Away NRSFI', 'Away YRSFI']]
        else:
            away_rs = away_ra = away_nrfi = away_yrfi = 'N/A'
            away_nrsfi = away_yrsfi = 'N/A'

        if not home_data.empty:
            home_data = home_data.iloc[0]
            home_rs, home_ra, home_nrfi, home_yrfi = home_data[['Home RS', 'Home RA', 'Home NRFI', 'Home YRFI']]
            home_nrsfi, home_yrsfi = home_data[['Home NRSFI', 'Home YRSFI']]
        else:
            home_rs = home_ra = home_nrfi = home_yrfi = 'N/A'
            home_nrsfi = home_yrsfi = 'N/A'

        if not total_data.empty:
            total_data = total_data.iloc[0]
            total_nrfi, total_yrfi = total_data[['Total NRFI', 'Total YRFI']]
            total_nrsfi, total_yrsfi = total_data[['Total NRSFI', 'Total YRSFI']]
            intra_nrfi, intra_yrfi = total_data[['Intra NRFI', 'Intra YRFI']]
            intra_nrsfi, intra_yrsfi = total_data[['Intra NRSFI', 'Intra YRSFI']]
            righties_nrsfi, righties_yrsfi = total_data[['Righties NRSFI', 'Righties YRSFI']]
            lefties_nrsfi, lefties_yrsfi = total_data[['Lefties NRSFI', 'Lefties YRSFI']]
            l10_streak, nrsfi_streak, yrsfi_streak = total_data[['L10 Streak', 'NRSFI Streak', 'YRSFI Streak']]
        else:
            total_nrfi = total_yrfi = total_nrsfi = total_yrsfi = intra_nrfi = intra_yrfi = intra_nrsfi = intra_yrsfi = righties_nrsfi = righties_yrsfi = lefties_nrsfi = lefties_yrsfi = l10_streak = nrsfi_streak = yrsfi_streak = 'N/A'

        away_rs_color = calculate_color(away_rs, *team_min_max['Away RS'])
        away_ra_color = calculate_color(away_ra, *team_min_max['Away RA'])
        away_nrfi_color = calculate_color(away_nrfi, *team_min_max['Away NRFI'], inverse=True)
        away_yrfi_color = calculate_color(away_yrfi, *team_min_max['Away YRFI'])
        away_nrsfi_color = calculate_color(away_nrsfi, *team_min_max['Away NRSFI'], inverse=True)
        away_yrsfi_color = calculate_color(away_yrsfi, *team_min_max['Away YRSFI'])

        home_rs_color = calculate_color(home_rs, *team_min_max['Home RS'])
        home_ra_color = calculate_color(home_ra, *team_min_max['Home RA'])
        home_nrfi_color = calculate_color(home_nrfi, *team_min_max['Home NRFI'], inverse=True)
        home_yrfi_color = calculate_color(home_yrfi, *team_min_max['Home YRFI'])
        home_nrsfi_color = calculate_color(home_nrsfi, *team_min_max['Home NRSFI'], inverse=True)
        home_yrsfi_color = calculate_color(home_yrsfi, *team_min_max['Home YRSFI'])

        total_nrfi_color = calculate_color(total_nrfi, *team_min_max['Total NRFI'], inverse=True)
        total_yrfi_color = calculate_color(total_yrfi, *team_min_max['Total YRFI'])
        total_nrsfi_color = calculate_color(total_nrsfi, *team_min_max['Total NRSFI'], inverse=True)
        total_yrsfi_color = calculate_color(total_yrsfi, *team_min_max['Total YRSFI'])
        intra_nrfi_color = calculate_color(intra_nrfi, *team_min_max['Intra NRFI'], inverse=True)
        intra_yrfi_color = calculate_color(intra_yrfi, *team_min_max['Intra YRFI'])
        intra_nrsfi_color = calculate_color(intra_nrsfi, *team_min_max['Intra NRSFI'], inverse=True)
        intra_yrsfi_color = calculate_color(intra_yrsfi, *team_min_max['Intra YRSFI'])
        righties_nrsfi_color = calculate_color(righties_nrsfi, *team_min_max['Righties NRSFI'], inverse=True)
        righties_yrsfi_color = calculate_color(righties_yrsfi, *team_min_max['Righties YRSFI'])
        lefties_nrsfi_color = calculate_color(lefties_nrsfi, *team_min_max['Lefties NRSFI'], inverse=True)
        lefties_yrsfi_color = calculate_color(lefties_yrsfi, *team_min_max['Lefties YRSFI'])

        away_nrfi_percent = round((away_nrfi / (away_nrfi + away_yrfi)) * 100) if (away_nrfi != 'N/A' and away_yrfi != 'N/A') else 'N/A'
        home_nrfi_percent = round((home_nrfi / (home_nrfi + home_yrfi)) * 100) if (home_nrfi != 'N/A' and home_yrfi != 'N/A') else 'N/A'
        away_nrsfi_percent = round((away_nrsfi / (away_nrsfi + away_yrsfi)) * 100) if (away_nrsfi != 'N/A' and away_yrsfi != 'N/A') else 'N/A'
        home_nrsfi_percent = round((home_nrsfi / (home_nrsfi + home_yrsfi)) * 100) if (home_nrsfi != 'N/A' and home_yrsfi != 'N/A') else 'N/A'
        total_nrfi_percent = round((total_nrfi / (total_nrfi + total_yrfi)) * 100) if (total_nrfi != 'N/A' and total_yrfi != 'N/A') else 'N/A'
        total_nrsfi_percent = round((total_nrsfi / (total_nrsfi + total_yrsfi)) * 100) if (total_nrsfi != 'N/A' and total_yrsfi != 'N/A') else 'N/A'
        intra_nrfi_percent = round((intra_nrfi / (intra_nrfi + intra_yrfi)) * 100) if (intra_nrfi != 'N/A' and intra_yrfi != 'N/A') else 'N/A'
        intra_nrsfi_percent = round((intra_nrsfi / (intra_nrsfi + intra_yrsfi)) * 100) if (intra_nrsfi != 'N/A' and intra_yrsfi != 'N/A') else 'N/A'
        righties_nrsfi_percent = round((righties_nrsfi / (righties_nrsfi + righties_yrsfi)) * 100) if (righties_nrsfi != 'N/A' and righties_yrsfi != 'N/A') else 'N/A'
        lefties_nrsfi_percent = round((lefties_nrsfi / (lefties_nrsfi + lefties_yrsfi)) * 100) if (lefties_nrsfi != 'N/A' and lefties_yrsfi != 'N/A') else 'N/A'


        away_nrfi_percent_color = calculate_nrfi_color(away_nrfi_percent)
        home_nrfi_percent_color = calculate_nrfi_color(home_nrfi_percent)
        away_nrsfi_percent_color = calculate_nrsfi_color(away_nrsfi_percent)
        home_nrsfi_percent_color = calculate_nrsfi_color(home_nrsfi_percent)
        total_nrfi_percent_color = calculate_nrfi_color(total_nrfi_percent)
        total_nrsfi_percent_color = calculate_nrsfi_color(total_nrsfi_percent)
        intra_nrfi_percent_color = calculate_nrfi_color(intra_nrfi_percent)
        intra_nrsfi_percent_color = calculate_nrsfi_color(intra_nrsfi_percent)
        righties_nrsfi_percent_color = calculate_nrsfi_color(righties_nrsfi_percent)
        lefties_nrsfi_percent_color = calculate_nrsfi_color(lefties_nrsfi_percent)


        intra_total_nrfi_percent = round((intra_nrfi_percent - total_nrfi_percent)) if (total_nrfi_percent != 'N/A' and intra_nrfi_percent != 'N/A') else 'N/A'
        intra_total_nrsfi_percent = round((intra_nrsfi_percent - total_nrsfi_percent)) if (total_nrsfi_percent != 'N/A' and intra_nrsfi_percent != 'N/A') else 'N/A'
        intra_total_nrfi_percent_color = calculate_intra_total_color(intra_total_nrfi_percent)
        intra_total_nrsfi_percent_color = calculate_intra_total_color(intra_total_nrsfi_percent)



        updated_data.append({
            'Team': team,
            'Away RS': away_rs,
            'Away RS Color': away_rs_color,
            'Away RA': away_ra,
            'Away RA Color': away_ra_color,
            'Away NRFI': away_nrfi,
            'Away NRFI Color': away_nrfi_color,
            'Away YRFI': away_yrfi,
            'Away YRFI Color': away_yrfi_color,
            'Away NRFI %': away_nrfi_percent,
            'Away NRFI % Color': away_nrfi_percent_color,
            'Away NRSFI': away_nrsfi,
            'Away NRSFI Color': away_nrsfi_color,
            'Away YRSFI': away_yrsfi,
            'Away YRSFI Color': away_yrsfi_color,
            'Away NRSFI %': away_nrsfi_percent,
            'Away NRSFI % Color': away_nrsfi_percent_color,



            'Home RS': home_rs,
            'Home RS Color': home_rs_color,
            'Home RA': home_ra,
            'Home RA Color': home_ra_color,
            'Home NRFI': home_nrfi,
            'Home NRFI Color': home_nrfi_color,
            'Home YRFI': home_yrfi,
            'Home YRFI Color': home_yrfi_color,
            'Home NRFI %': home_nrfi_percent,
            'Home NRFI % Color': home_nrfi_percent_color,
            'Home NRSFI': home_nrsfi,
            'Home NRSFI Color': home_nrsfi_color,
            'Home YRSFI': home_yrsfi,
            'Home YRSFI Color': home_yrsfi_color,
            'Home NRSFI %': home_nrsfi_percent,
            'Home NRSFI % Color': home_nrsfi_percent_color,



            'Total NRFI': total_nrfi,
            'Total NRFI Color': total_nrfi_color,
            'Total YRFI': total_yrfi,
            'Total YRFI Color': total_yrfi_color,
            'Total NRFI %': total_nrfi_percent,
            'Total NRFI % Color': total_nrfi_percent_color,

            'Total NRSFI': total_nrsfi,
            'Total NRSFI Color': total_nrsfi_color,
            'Total YRSFI': total_yrsfi,
            'Total YRSFI Color': total_yrsfi_color,
            'Total NRSFI %': total_nrsfi_percent,
            'Total NRSFI % Color': total_nrsfi_percent_color,


            'Intra NRFI': intra_nrfi,
            'Intra NRFI Color': intra_nrfi_color,
            'Intra YRFI': intra_yrfi,
            'Intra YRFI Color': intra_yrfi_color,
            'Intra NRFI %': intra_nrfi_percent,
            'Intra NRFI % Color': intra_nrfi_percent_color,

            'Intra NRSFI': intra_nrsfi,
            'Intra NRSFI Color': intra_nrsfi_color,
            'Intra YRSFI': intra_yrsfi,
            'Intra YRSFI Color': intra_yrsfi_color,
            'Intra NRSFI %': intra_nrsfi_percent,
            'Intra NRSFI % Color': intra_nrsfi_percent_color,


            'Intra-Total NRFI %': intra_total_nrfi_percent,
            'Intra-Total NRFI % Color': intra_total_nrfi_percent_color,
            'Intra-Total NRSFI %': intra_total_nrsfi_percent,
            'Intra-Total NRSFI % Color': intra_total_nrsfi_percent_color,


            'Righties NRSFI': righties_nrsfi,
            'Righties NRSFI Color': righties_nrsfi_color,
            'Righties YRSFI': righties_yrsfi,
            'Righties YRSFI Color': righties_yrsfi_color,
            'Righties NRSFI %': righties_nrsfi_percent,
            'Righties NRSFI % Color': righties_nrsfi_percent_color,

            'Lefties NRSFI': lefties_nrsfi,
            'Lefties NRSFI Color': lefties_nrsfi_color,
            'Lefties YRSFI': lefties_yrsfi,
            'Lefties YRSFI Color': lefties_yrsfi_color,
            'Lefties NRSFI %': lefties_nrsfi_percent,
            'Lefties NRSFI % Color': lefties_nrsfi_percent_color,

            'L10 Games': l10_streak,
            'NRSFI Streak': nrsfi_streak,
            'YRSFI Streak': yrsfi_streak
        })

    return render_template('mlb_fi_display_teams_data.html', updated_data=updated_data)

if __name__ == '__main__':
    app.run(debug=True)
