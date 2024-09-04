import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

def read_data():
    # Read the CSV file into a pandas DataFrame
    data = pd.read_csv('batter_h_matchups_update.csv')
    return data

def calculate_avg_color(value, min_val=0, max_val=0.5):
    """Calculate color based on a scaled value from 0 to 0.5."""
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

    # Scale value from 0 to 0.5
    scaled_value = 0.5 * (value - min_val) / (max_val - min_val)
    scaled_value = min(max(scaled_value, 0), 0.5)  # Ensure the value is between 0 and 0.5

    # Map scaled value to a color gradient
    red = int(255 * (1 - scaled_value / 0.5))
    green = int(255 * (scaled_value / 0.5))

    return f'rgb({red},{green},0)'

def calculate_sums(group):
    # Calculate the sum for the first 5 batters and the full lineup
    first_5 = group.head(5).sum(numeric_only=True)
    full_lineup = group.sum(numeric_only=True)

    # Calculate AVG for first 5 and full lineup
    first_5_avg = first_5['H'] / first_5['AB'] if first_5['AB'] > 0 else 0
    full_lineup_avg = full_lineup['H'] / full_lineup['AB'] if full_lineup['AB'] > 0 else 0

    # Convert to dict and add names
    first_5 = first_5.to_dict()
    first_5['Batter'] = 'First 5'
    first_5['Opposing Pitcher'] = group['Opposing Pitcher'].iloc[0]
    first_5['AVG'] = f'{first_5_avg:.3f}' if first_5['AB'] > 0 else 'N/A'
    first_5['OBP'] = ''
    first_5['SLG'] = ''
    first_5['OPS'] = ''

    full_lineup = full_lineup.to_dict()
    full_lineup['Batter'] = 'Full Lineup'
    full_lineup['Opposing Pitcher'] = group['Opposing Pitcher'].iloc[0]
    full_lineup['AVG'] = f'{full_lineup_avg:.3f}' if full_lineup['AB'] > 0 else 'N/A'
    full_lineup['OBP'] = ''
    full_lineup['SLG'] = ''
    full_lineup['OPS'] = ''

    # Add these rows to the group
    return [first_5, full_lineup] + group.to_dict(orient='records')

@app.route('/')
def display_data():
    # Get the data
    data = read_data()

    # Group data by 'Opposing Pitcher' and calculate sums
    grouped_data = data.groupby('Opposing Pitcher').apply(calculate_sums).reset_index(drop=True)
    table_data = [item for sublist in grouped_data for item in sublist]

    # Render HTML template with data
    return render_template('display_battervpitcher_data.html', table_data=table_data, calculate_avg_color=calculate_avg_color)

if __name__ == '__main__':
    app.run(debug=True)
