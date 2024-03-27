# Spotify-Lib

Spotify-Lib is a simple Python library designed to fetch song and album metadata from Spotify. It utilizes web scraping techniques to extract information directly from Spotify's web pages. This library is particularly useful for developers looking to integrate Spotify's rich music metadata into their applications without relying on Spotify's official API.

## Features

- Fetches song and album metadata from Spotify.
- Supports both Spotify URLs and Spotify IDs.
- Extracts detailed information such as artwork URL, duration, genre, album, title, artist, and release date for songs.
- Extracts album title, artist, description, and release date for albums.
- Utilizes logging for debugging and error tracking.

## Installation

Spotify-Lib does not require any external dependencies beyond the Python Standard Library. However, it does rely on the `BeautifulSoup` library for parsing HTML. You can install BeautifulSoup using pip:

```bash
pip install beautifulsoup4
```

## Usage

To use Spotify-Lib, you need to import the `Spotify` class and create an instance of it by passing a Spotify URL or Spotify ID and a logger instance. Here's a basic example:

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

## Documentation

### `Spotify` Class

The `Spotify` class is the main entry point for using Spotify-Lib. It requires a Spotify URL or Spotify ID and a logger instance for debugging purposes.

#### Methods

- `get_song()`: Fetches metadata for a Spotify song.
- `get_album()`: Fetches metadata for a Spotify album.

#### Attributes

- `found_id`: The Spotify ID extracted from the URL or provided directly.
- `song_url`: The URL of the Spotify song.
- `album_url`: The URL of the Spotify album.

### `SongData` and `AlbumData` Classes

These classes are used internally to store the metadata fetched from Spotify. They include attributes for various pieces of metadata such as artwork URL, duration, genre, album, title, artist, and release date for songs, and artwork URL, title, artist, description, and release date for albums.

## Limitations

- Spotify-Lib relies on web scraping, which is less reliable than using an official API. Spotify's web page structure can change, potentially breaking the library.
- The library does not support all Spotify features. It is focused on fetching basic metadata for songs and albums.

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue on GitHub. If you'd like to contribute code, please fork the repository and submit a pull request.

## License

Spotify-Lib is released under the MIT License. See the `LICENSE` file for more details.
