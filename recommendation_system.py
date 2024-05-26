import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import warnings
warnings.filterwarnings('ignore')


# # Importing Data from CSV

# Import and display the CSV file
tracks = pd.read_csv('tracks_transformed.csv')

# Import and display artist data
artists = pd.read_csv('./artists_transformed.csv')

# Import and display genre data
genres = pd.read_csv('./data_by_genres_o.csv', na_filter=False)


# # Data Prepping

# Check for null rows in the data
null_rows_artist = (artists.isnull().any(axis=1)).sum()
null_rows_tracks = (tracks.isnull().any(axis=1)).sum()
null_rows_genre = (genres.isnull().any(axis=1)).sum()

# Remove rows with null values 
artists = artists.dropna()
tracks = tracks.dropna()

# Transform followers to numeric -> helps with further processing and analysis
artists['followers'] = pd.to_numeric(artists['followers'])


# # Song Recommendation Functionality

# Since the dataset is quite large, for now I will only make use of the first 5000 most popular songs. This number can be adjusted for the actual implementation in MySpace.
popular_songs = tracks.sort_values(by=['popularity'], ascending=False).head(10000)

# Transform textual genre information(textual) into a numerical format that can be used for similarity calculations.
vectorizer = CountVectorizer()
vectorizer.fit(popular_songs['genres'])

# This function suggests 5 songs based on a song name which is given as a parameter
# A similarity score is generated for each song, the songs wtih the highest similarity and popularity are returened.

def song_recommender(song_name):
    try:
        # Columns for numerical features
        numeric_cols = ['release_year', 'duration_s', 'popularity', 'danceability', 'energy', 'key', 'loudness',
                    'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']

        # Check to see if the song exists
        song = popular_songs[popular_songs['name'] == song_name]
        
        if song.empty:
            return None

        # Create vectors for the given song -> The cosine similarity function requires numerical vectors to compute the similarity between items
        song_genre_vect = vectorizer.transform(song['genres']).toarray()
        song_feature_vect = song[numeric_cols].to_numpy()

        # Calculate similarity scores
        def calculate_similarity(row):
            other_song_genre_vect = vectorizer.transform([row['genres']]).toarray()
            other_song_feature_vect = row[numeric_cols].to_numpy().reshape(1, -1)

            genre_similarity = cosine_similarity(song_genre_vect, other_song_genre_vect)[0][0]
            feature_similarity = cosine_similarity(song_feature_vect, other_song_feature_vect)[0][0]

            return (genre_similarity + feature_similarity) / 2

        popular_songs['similarity'] = popular_songs.apply(calculate_similarity, axis=1)

        # Sort by similarity and popularity
        recommended_songs = popular_songs.sort_values(by=['similarity', 'popularity'],
                                                      ascending=[False, False])

        # Select top 5 most similar songs
        recommended_songs = recommended_songs[['name', 'artists', 'release_year']].iloc[1:6]

        return recommended_songs

    except Exception as e:
        print(f"An error occurred: {e}")


# # Artist Recommendation Functionality

# Since the dataset is quite large, for now I will only make use of the first 5000 most popular artists. This number can be adjusted for the actual implementation in MySpace.
popular_artists = artists.sort_values(by=['popularity', 'followers'], ascending=[False, False]).head(5000)

# Transform textual genre information(textual) into a numerical format that can be used for similarity calculations.
artist_vectorizer = CountVectorizer()
artist_vectorizer.fit(popular_artists['genres'])

# This function suggests 5 artists based on an artist name which is given as a parameter
# A similarity score is generated for each artist, the artist wtih the highest similarity and popularity are returened.

def artist_recommender(artist_name):
    try:
        # Columns for numerical features
        numeric_cols = ['followers', 'popularity']

        # Check to see if the song exists
        artist = popular_artists[popular_artists['name'] == artist_name]
        
        if artist.empty:
            return None

        # Create vectors for the given artist -> The cosine similarity function requires numerical vectors to compute the similarity between items
        artist_genre_vect = artist_vectorizer.transform(artist['genres']).toarray()
        artist_feature_vect = artist[numeric_cols].to_numpy()

        # Calculate similarity scores
        def calculate_similarity(row):
            other_artist_genre_vect = artist_vectorizer.transform([row['genres']]).toarray()
            other_artist_feature_vect = row[numeric_cols].to_numpy().reshape(1, -1)

            genre_similarity = cosine_similarity(artist_genre_vect, other_artist_genre_vect)[0][0]
            feature_similarity = cosine_similarity(artist_feature_vect, other_artist_feature_vect)[0][0]

            return (genre_similarity + feature_similarity) / 2

        popular_artists['similarity'] = popular_artists.apply(calculate_similarity, axis=1)

        # Sort by similarity and popularity
        recommended_artists = popular_artists.sort_values(by=['similarity', 'popularity', 'followers'],
                                                      ascending=[False, False, False])

        recommended_artists = recommended_artists[recommended_artists['name'] != artist_name]
        recommended_artists = recommended_artists[['name', 'genres', 'followers', 'popularity']].iloc[:5]

        return recommended_artists

    except Exception as e:
        print(f"An error occurred: {e}")

