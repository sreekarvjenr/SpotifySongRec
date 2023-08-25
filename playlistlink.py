import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = '4b3b03fe5f6c4b67b121fac734ca70d1'
client_secret = '418f088659664e2390a6f1035fb322a9'
redirect_uri = 'https://localhost:8888/callback'  # For example, 'http://localhost:8888/callback'

# Set up Spotipy OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                                                redirect_uri=redirect_uri, scope='playlist-modify-private'))

def get_similar_songs(song_name):
    
    # Search for the given song
    results = sp.search(q=song_name, type='track', limit=1)
    if not results['tracks']['items']:
        print('No matching song found.')
        return

    # Get the track ID of the given song
    track_id = results['tracks']['items'][0]['id']

    # Get audio features of the given song
    audio_features = sp.audio_features([track_id])
    if not audio_features[0]:
        print('No audio features found for the song.')
        return

    # Extract relevant audio features
    danceability = audio_features[0]['danceability']
    energy = audio_features[0]['energy']
    valence = audio_features[0]['valence']

    # Search for similar songs based on audio features
    results = sp.recommendations(seed_tracks=[track_id], limit=10, target_danceability=danceability,
                                 target_energy=energy, target_valence=valence)

    # Extract the names of the similar songs
    similar_songs = [track['name'] for track in results['tracks']]
    return similar_songs

def create_playlist(user_id, playlist_name, song_uris):
    # Create an empty playlist
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)

    # Add songs to the playlist
    sp.playlist_add_items(playlist_id=playlist['id'], items=song_uris)
    print('Playlist created successfully.')

    # Get the playlist link
    playlist_link = playlist['external_urls']['spotify']
    print('Playlist link:', playlist_link)

# Example usage
song_name = input("Enter a song name: ")
similar_songs = get_similar_songs(song_name)
print("Similar songs:")
for song in similar_songs:
    print(song)

user_id = input("Enter the user ID for whom you want to create the playlist: ")
playlist_name = input("Enter a name for the playlist: ")

# Get the URIs of the similar songs
song_uris = []
for song in similar_songs:
    results = sp.search(q=song, type='track', limit=1)
    if results['tracks']['items']:
        song_uris.append(results['tracks']['items'][0]['uri'])

# Create the playlist for the specified user and add songs to it
create_playlist(user_id=user_id, playlist_name=playlist_name, song_uris=song_uris)
