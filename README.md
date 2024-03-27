# MusicData-Lib

Spotify-Lib is a Python library designed to fetch song and album metadata from Spotify and Deezer without relying on their official APIs. It utilizes web scraping techniques to extract information directly from Spotify's and Deezer's web pages. This library is particularly useful for developers looking to integrate rich music metadata into their applications.

## Features

- Fetches song and album metadata from Spotify and Deezer.
- Supports both Spotify and Deezer URLs and IDs.
- Extracts detailed information such as artwork URL, duration, genre, album, title, artist, and release date for songs.
- Extracts album title, artist, description, and release date for albums.
- Utilizes logging for debugging and error tracking.

## Installation

Spotify-Lib requires the BeautifulSoup library for parsing HTML. Install it using pip:

```bash
pip install beautifulsoup4
```

## Usage

To use Spotify-Lib, import the `Spotify` and `Deezer` classes and create instances by passing a Spotify or Deezer URL or ID and a logger instance. Here's a basic example for both:

### Spotify

```python
import logging
from spotify_lib import Spotify

# Set up logging
logger = logging.getLogger("Spotify")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

# Initialize Spotify instance with a URL or ID
spotify = Spotify("https://open.spotify.com/track/0ax4ZXW4EOk4zUvdP9Fu2H", logger)

# Fetch song metadata
song_metadata = spotify.get_song()
print(song_metadata)

# Fetch album metadata
spotify = Spotify("https://open.spotify.com/album/1vLfxO3ZzXc9k2EGPGLwX6", logger)
album_metadata = spotify.get_album()
print(album_metadata)
```

### Deezer

```python
import logging
from deezer_lib import Deezer

# Set up logging
logger = logging.getLogger("Deezer")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

# Initialize Deezer instance with a URL or ID
deezer = Deezer("https://www.deezer.com/track/123456789", logger)

# Fetch song metadata
song_metadata = deezer.get_song()
print(song_metadata)

# Fetch album metadata
deezer = Deezer("https://www.deezer.com/album/987654321", logger)
album_metadata = deezer.get_album()
print(album_metadata)
```

## Limitations

- Spotify-Lib relies on web scraping, which is less reliable than using an official API. Spotify's and Deezer's web page structure can change, potentially breaking the library.
- The library does not support all Spotify and Deezer features. It is focused on fetching basic metadata for songs and albums.

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue on GitHub. If you'd like to contribute code, please fork the repository and submit a pull request.

## License

Spotify-Lib is released under the MIT License. See the [LICENSE](LICENSE) file for more details.

This README provides a clear and concise overview of the Spotify-Lib project, including how to install and use the library, its features, limitations, and contribution guidelines. It's designed to be a comprehensive resource for developers interested in integrating Spotify and Deezer metadata into their applications.
