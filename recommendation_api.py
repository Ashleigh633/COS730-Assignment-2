#Imports
from flask import Flask, request, jsonify
from recommendation_system import song_recommender
from recommendation_system import artist_recommender

import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)


@app.route('/get-recommended-songs', methods=['GET'])
def get_recommended_songs():
    song_name = request.args.get('song_name')
    if not song_name:
        return jsonify({'error': 'Please provide a song name'}), 400
    
    recommended_songs = song_recommender(song_name)
    if recommended_songs is None:
        return jsonify({'error': f'Song "{song_name}" not found.'}), 404

    recommended_songs_dict = recommended_songs.to_dict(orient='records') # DataFrames are not directly serializable to JSON, but dictionaries are -> hence the conversion
    
    return jsonify(recommended_songs_dict)


@app.route('/get-recommended-artists', methods=['GET'])
def get_recommended_artists():
    artist_name = request.args.get('artist_name')
    if not artist_name:
        return jsonify({'error': 'Please provide an artist name'}), 400
    
    recommended_artists = artist_recommender(artist_name)
    if recommended_artists is None:
        return jsonify({'error': f'Song "{artist_name}" not found.'}), 404

    recommended_artists_dict = recommended_artists.to_dict(orient='records')
    
    return jsonify(recommended_artists_dict)


if __name__ == '__main__':
    app.run(debug=True)




