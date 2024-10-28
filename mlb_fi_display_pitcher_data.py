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

def calculate_nrfi_color(value, min_val=50, max_val=100):
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

def calculate_era_color(value, min_val=0, max_val=9):
    """Calculate color for ERA based on a fixed scale (0 to 9)."""
    if value == 'N/A' or pd.isna(value):
        return '#ffffff'
    try:
        value = float(value)
    except ValueError:
        return '#ffffff'
    value = max(min_val, min(value, max_val))
    ratio = (value - min_val) / (max_val - min_val)
    green = int(255 * (1 - ratio))
    red = int(255 * ratio)
    return f'rgb({red},{green},0)'

def extract_pitcher_data(row, pitcher_min_max):
    """Extract and format pitcher data from the row."""
    def get_color_and_value(stat, stat_min_max, inverse=False, era=False):
        value = row.get(stat, 'N/A')
        if era:
            color = calculate_era_color(value) if value != 'N/A' else '#ffffff'
        else:
            color = calculate_color(value, *stat_min_max, inverse=inverse) if value != 'N/A' else '#ffffff'
        return value, color

    def get_percentage_color(nrfi, yrfi):
        if nrfi != 'N/A' and yrfi != 'N/A':
            try:
                percent = round((nrfi / (nrfi + yrfi)) * 100)
            except ZeroDivisionError:
                percent = 'N/A'
        else:
            percent = 'N/A'
        color = calculate_nrfi_color(percent) if percent != 'N/A' else '#ffffff'
        return percent, color

    data = {}
    data['Name'] = row['Name']
    data['Throw'] = row['Throw']
    data['Season ERA'], data['Season ERA Color'] = get_color_and_value('Season ERA', pitcher_min_max['Season ERA'], era=True)

    for location in ['Away', 'Home']:
        for stat in ['ERA', 'RA', 'NRFI', 'YRFI']:
            value, color = get_color_and_value(f'{location} {stat}', pitcher_min_max[f'{location} {stat}'], inverse=(stat == 'NRFI'), era=(stat == 'ERA'))
            data[f'{location} {stat}'] = value
            data[f'{location} {stat} Color'] = color

        nrfi_percent, nrfi_percent_color = get_percentage_color(row.get(f'{location} NRFI', 'N/A'), row.get(f'{location} YRFI', 'N/A'))
        data[f'{location} NRFI %'] = nrfi_percent
        data[f'{location} NRFI % Color'] = nrfi_percent_color

    for stat in ['Total NRFI', 'Total YRFI']:
        value, color = get_color_and_value(stat, pitcher_min_max[stat], inverse=(stat == 'Total NRFI'))
        data[stat] = value
        data[f'{stat} Color'] = color

    total_nrfi_percent, total_nrfi_percent_color = get_percentage_color(row.get('Total NRFI', 'N/A'), row.get('Total YRFI', 'N/A'))
    data['Total NRFI %'] = total_nrfi_percent
    data['Total NRFI % Color'] = total_nrfi_percent_color

    for streak in ['L5 Streak', 'NRFI Streak', 'YRFI Streak']:
        data[streak] = row.get(streak, 'N/A')

    return data

@app.route('/')
def display_data():
    pitcher_data_df = pd.read_csv('mlb_fi_pitcher_data.csv')
    pitcher_min_max = {col: calculate_min_max(pitcher_data_df, col) for col in pitcher_data_df.columns if col not in ['Name', 'Throw']}

    updated_data = [extract_pitcher_data(row, pitcher_min_max) for _, row in pitcher_data_df.iterrows()]

    return render_template('mlb_fi_display_pitchers_data.html', updated_data=updated_data)

if __name__ == '__main__':
    app.run(debug=True)
