from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import io
import matplotlib
import os

# Use 'Agg' backend for environments without a display (e.g. Codespaces)
matplotlib.use('Agg')

# Debugging: Check directories
print("Current working directory:", os.getcwd()) # returns current working directory, this helps understand where the script is looking for files like templates, static assets, etc. 
print("Files in cwd:", os.listdir()) # lists all files and folders in the current working directory, this helps confirm wheter specific folders are there
try:
    print("Files in templates:", os.listdir('templates'))
except FileNotFoundError:
    print("'templates' directory not found.")

app = Flask(__name__)

def clean_spotify_data():
    url = 'https://github.com/Yusuhasn/Spotify-Data-Analysis/raw/refs/heads/main/Most%20Streamed%20Spotify%20Songs%202024.csv'
    df = pd.read_csv(url, encoding='latin1')

    # Clean column headers (just in case)
    df.columns = df.columns.str.strip()

    # Clean and convert 'Spotify Streams'
    if 'Spotify Streams' in df.columns:
        df['Spotify Streams'] = (
            df['Spotify Streams']
            .astype(str)
            .str.replace(',', '', regex=False)
            .str.extract(r'(\d+)', expand=False)
            .astype(float)
        )
    else:
        print("❗ 'Spotify Streams' column not found!")

    # Clean other columns
    df['Artist'] = df['Artist'].str.strip()
    df['Release Date'] = pd.to_datetime(df['Release Date'], errors='coerce')

    # Drop missing or duplicate rows
    df = df.dropna(subset=['Track', 'Artist', 'All Time Rank', 'Spotify Streams'])
    df = df.drop_duplicates()

    insights = {}
    playlist_analysis = {}

    # Correlation and analysis
    if 'Spotify Playlist Count' in df.columns:
        df['Spotify Playlist Count'] = pd.to_numeric(df['Spotify Playlist Count'], errors='coerce')
        corr_df = df[['Spotify Playlist Count', 'Spotify Streams']].dropna()

        if len(corr_df) > 1:
            playlist_corr, _ = pearsonr(
                corr_df['Spotify Playlist Count'],
                corr_df['Spotify Streams']
            )
            insights['playlist_correlation'] = playlist_corr

            # Basic analysis on top 10%
            top_10_percent = corr_df.nlargest(int(len(corr_df) * 0.1), 'Spotify Streams')
            playlist_analysis['top_10_playlists'] = top_10_percent['Spotify Playlist Count'].mean()

    # Create static folder if not exists
    if not os.path.exists('static'):
        os.makedirs('static')

    # Generate histogram plot
    plt.figure(figsize=(10, 6))
    df['Spotify Streams'].hist(bins=30)
    plt.title('Distribution of Spotify Streams')
    plt.xlabel('Streams')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig('static/streams_histogram.png')
    plt.close()

    # Capture df.info() output
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    buffer.close()

    return df, info_str

@app.route('/')
def home():
    df, info_str = clean_spotify_data()

    numeric_cols = ['All Time Rank', 'Spotify Streams']
    # Create HTML tables for web
    table_html = df[['Track', 'Artist', 'All Time Rank', 'Spotify Streams']].head().to_html(classes='data')
    summary_html = df[['Track', 'Artist', 'All Time Rank', 'Spotify Streams']].head().describe().to_html(classes='data')


    return render_template(
        'index.html',
        data_table=table_html,
        stats_table=summary_html,
        info_output=info_str,
        plot_path='static/streams_histogram.png'
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
