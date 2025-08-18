from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import io
import matplotlib
import os
print("Current working directory:", os.getcwd())
print("Files in cwd:", os.listdir())
print("Files in templates:", os.listdir('templates'))


# Use 'Agg' backend for environments without a display (like Codespaces)
matplotlib.use('Agg')

app = Flask(__name__)

def clean_spotify_data():
    url = 'https://github.com/Yusuhasn/Spotify-Data-Analysis/raw/refs/heads/main/Most%20Streamed%20Spotify%20Songs%202024.csv'
    df = pd.read_csv(url, encoding='latin1')  # or pd.read_csv(url) if csv

    # Clean
    df['Spotify Streams'] = pd.to_numeric(df['Spotify Streams'], errors='coerce').fillna(0)
    df['Artist'] = df['Artist'].str.strip()
    df['Release Date'] = pd.to_datetime(df['Release Date'], errors='coerce')
    df = df.dropna(axis=1)
    df = df.drop_duplicates()

    # Save Histogram
    if not os.path.exists('static'):
        os.makedirs('static')
    plt.figure(figsize=(10, 6))
    df['Spotify Streams'].hist(bins=30)
    plt.title('Distribution of Streams')
    plt.xlabel('Streams')
    plt.ylabel('Frequency')
    plt.savefig('static/streams_histogram.png')  # Fixed filename
    plt.close()

    # Capture df.info() output
    buffer = io.StringIO()
    df.info(buf=buffer)  # Fixed argument name
    info_str = buffer.getvalue()
    buffer.close()

    return df, info_str

@app.route('/')
def home():
    df, info_str = clean_spotify_data()

    table_html = df.head().to_html(classes='data')
    summary_html = df.describe().to_html(classes='data')

    return render_template(
        'index.html',
        data_table=table_html,
        stats_table=summary_html,
        info_output=info_str
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


