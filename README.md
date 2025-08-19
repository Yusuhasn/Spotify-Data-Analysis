**Analyze the Most Streamed Songs on Spotify**

This project examins a dataset of the most streamed songs on Spotify provided on Kaggle. The purpose of the project is to clean, explore, and visualize trends in music streaming to gain insigts on trends regarding popular songs, artists influence, and types of content.

**Dataset**

Source: Kaggle - Spotify Most Streamed Songs
Size: 4600 songs with 29 attributes per song
Original format: .csv
Tools & Libraries
Python
Pandas - data wrangling/analysis
Matplotlib - data visualizations
Github Codespaces - Cloud IDE for example development

**Data Cleaning**

Prior to any analysis, the dataset was cleaned carefully through:
Transforming Spotify Streams to numeric value
Transforming Release Date to correct datetime
Removing leading/trailing whitespace from string fields

**Handling null values**

All missing stream counts were replaced with a 0
Columns with missing values were dropped due to over treshold (e.g. TIDAL Popularity)
Duplicates rows were dropped
Final clean dataset resulted in 4,598 x 8 rows/columns
key Columns Used Column Description Track Song Title Album Name Album the track is associated with Release Date Official release date ISRC Individual track ID All Time Rank Ranking from all-time stream list Track Score Composite popularity score Spotify Streams Total number of Spotify streams Explicit Track 1 = Explicit, 0 = Clean

**Example Visualizations**

Histogram of Spotify Stream distributions
Analysis of explicit vs. clean songs
Top 10 most streamed songs (coming soon)

**Insights (examples) **
Most songs in dataset are non-explicit.
Stream counts are very skewed - few songs are very popular
There wasn't enough data for streaming platforms such as Youtube and SoundCloud to be inluded in the core analysis

How to Run:
Clone the repo:
git clone https://github.com/Yusuhasn/Spotify-Data-Analysis.git
Open in GitHub Codespaces or Jupyter/Colab.
Run spotifydata.py or the notebook file to view analysis and plots.
Future Work
More visualization options
Weather app
Budget app
Use other platform data such as Youtube, Tiktok, SoundCloud if cleaned
Author
Yusra H - 12th grade student working on Data sciencee
see my other GitHub Projects for more ideas and inspirations
""Star this repo""
