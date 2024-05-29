## MartinAmez_ML
Repository dedicated to machine learning projects.

**Problem Definition**

The objective is to create a playlist based on the mood provided by the songs.

**Datasets**

music_verify: A small dataset of 4 different playlists with songs categorized as sad, happy, calm, and energetic. It includes data such as song name, album, artist, duration, popularity, and audio features.

music_df: A large dataset of Top 50 songs from different countries. It includes data such as country, song name, album, artist, duration, popularity, and audio features.

**Solution**

To achieve this, I will follow these steps:

- Obtain the 'base data' by web scraping Spotify for the current top tracks in each country.
- Obtain the audio features in several batches.
- Create labels for each song using K-means according to references.
- Build a song classifier based on moods.
- Compose a playlist for every mood/country.

Additionally:

- Analyze the emotional trend for each country.
- Determine the trend of my preferences.

**Folders**
- data: with the 2 datasets
- data_sample: final dataset with labels
- img: with some images from web scraping
- steps: notebooks, datasets saved, and functions to obtain the data, trying models, clustering, and other experiments...
- model: best_model.pkl
- root: Guide project, readme, and abstract

**Bibliography**

https://spotipy.readthedocs.io/en/2.22.1/
https://sites.tufts.edu/eeseniordesignhandbook/2015/music-mood-classification/
