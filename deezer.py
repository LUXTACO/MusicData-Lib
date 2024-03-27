import re
import json
import logging
import datetime
import urllib.request

from bs4 import BeautifulSoup

DZ_URL_REGEX = re.compile('https://www\.deezer\.com/(?P<type>[^/]*)/(?P<id>[^?]*)')

class Deezer:
    
    def __init__(self, url: str, logger: logging.Logger, experimental: bool = False):
        
        self.logger = logger
        self.experimental = experimental
        
        if url.find("deezer.com") != -1:
            logger.debug("Deezer URL detected!")
            self.found_id = DZ_URL_REGEX.search(url.split("?")[0]).group("id")
            if self.found_id.find("/") != -1:
                self.found_id = self.found_id.split("/")[1]
        else:
            logger.debug("Deezer ID detected!")
            self.found_id = url
            
        self.song_url = f"https://www.deezer.com/en/track/{self.found_id}"
        self.album_url = f"https://www.deezer.com/en/album/{self.found_id}"
        
        logger.debug(f"Song ID: {self.found_id}")
        logger.debug(f"Song URL: {self.song_url}")
        logger.debug(f"Album URL: {self.album_url}")
        
    def get_song(self) -> dict:
        
        """
        * Get the metadata of a Deezer song
        
            Data Returned:
            - artwork_url (str)
                DESCRIPTION: The URL of the song's artwork
            - duration (int)
                DESCRIPTION: The duration of the song in milliseconds
            - title (str)
                DESCRIPTION: The title of the song
            - artist (str)
                DESCRIPTION: The artist of the song
            - release_date (str)
                DESCRIPTION: The date the song was released
        """
        
        try:
            soup = self.get_webpage(self.song_url)
            self.metatags = soup.findAll("meta")
            metadata = self.get_metadata(self.metatags, "song")
            
            if self.experimental:
                script_tag = soup.find('script', string=re.compile('window.__DZR_APP_STATE__'))
                if script_tag:
                    script_tag = script_tag.string.replace('window.__DZR_APP_STATE__ = {', '').replace('};', '')
                    script_tag = "{" + script_tag 
                    json_data = json.loads(script_tag)
                
                if metadata.release_date == "Unknown":
                    metadata.release_date = json_data['DATA']['PHYSICAL_RELEASE_DATE']
            
            self.album_url = f"{metadata.album}"
            metadata.album = self.get_album()
            return metadata
        except Exception as e:
            self.logger.error(f"Failed to get song: {e}")
            return False
        
    def get_album(self) -> dict:
        
        """
        * Get the metadata of a Deezer album
        
            Data Returned:
            - artwork_url (str)
                DESCRIPTION: The URL of the album's artwork
            - title (str)
                DESCRIPTION: The title of the album
            - artist (str)
                DESCRIPTION: The artist of the album
            - release_date (str)
                DESCRIPTION: The date the album was released
        """
        
        try:
            soup = self.get_webpage(self.album_url)
            self.metatags = soup.findAll("meta")
            metadata = self.get_metadata(self.metatags, "album")
            
            if self.experimental:
                script_tag = soup.find('script', string=re.compile('window.__DZR_APP_STATE__'))
                if script_tag:
                    script_tag = script_tag.string.replace('window.__DZR_APP_STATE__ = {', '').replace('};', '')
                    script_tag = "{" + script_tag 
                    json_data = json.loads(script_tag)
                    
                if metadata.release_date == "Unknown":
                    metadata.release_date = json_data['DATA']['PHYSICAL_RELEASE_DATE']
            
            return metadata
        except Exception as e:
            self.logger.error(f"Failed to get webpage: {e}")
            return False
        
    @staticmethod
    def get_webpage(song_url) -> BeautifulSoup:
        
        """
        * Get the HTML of a webpage
        
            Data Used:
            - url (str)
                DESCRIPTION: The URL of the webpage
                
            Data Returned:
            - soup (BeautifulSoup)
                DESCRIPTION: The HTML of the webpage
        """
        
        try:
            resp = urllib.request.urlopen(song_url)
        except urllib.error.HTTPError:
            logging.error("got error urllib.error.HTTPError with " + song_url)
            return False
        except urllib.error.URLError:
            logging.error("got error urllib.error.URLError with " + song_url)
            return False

        if resp.code != 200:
            logging.error("got httperror 200 with " + song_url)
            return False
        else:
            return BeautifulSoup(resp.read(), "html.parser")
            
    @staticmethod
    def get_metadata(found_tags: list, metadata_type: str = "song") -> dict:
        
        """
        * Get the metadata of a Spotify song
        
            Data Used:
            - found_tags (list)
                DESCRIPTION: The metadata tags found on the webpage
            - metadata_type (str)
                DESCRIPTION: The type of metadata to get
                
            Data Returned:
            - song_data (dict)
                DESCRIPTION: The metadata of the song
            - album_data (dict)
                DESCRIPTION: The metadata of the album
        """
        
        if metadata_type == "song":
            found_data = SongData()
            
            """
            * SongMetadata Tags:
            
                artwork_url: str
                duration: int
                genre: str
                album: str
                title: str
                artist: str
                release_date: str
            """
            
            for tag in found_tags:
                # artwork_url
                if tag.get("property") == "og:image":
                    found_data.artwork_url = tag.get("content")
                # duration
                elif tag.get("property") == "music:duration":
                    found_data.duration = int(tag.get("content"))
                # genre
                elif tag.get("name") == "music:genre":
                    found_data.genre = tag.get("content")
                # album
                elif tag.get("property") == "music:album:url":
                    found_data.album = tag.get("content")
                # artist
                elif tag.get("property") == "music:musician":
                    soup = Deezer.get_webpage(tag.get("content"))
                    tags = soup.findAll("meta")
                    for tag in tags:
                        if tag.get("property") == "og:title":
                            found_data.artist = tag.get("content")
                # release_date
                elif tag.get("name") == "music:release_date":
                    found_data.release_date = tag.get("content")
                # title
                elif tag.get("property") == "og:title":
                    found_data.title = tag.get("content")
            
        elif metadata_type == "album":
            found_data = AlbumData()
            
            """
            * AlbumMetadata Tags:
                
                artwork_url (str)
                title (str)
                artist (str)
                description (str)
                release_date (str)
            """
            
            for tag in found_tags:
                # artwork_url
                if tag.get("property") == "og:image":
                    found_data.artwork_url = tag.get("content")
                # title
                elif tag.get("property") == "og:title":
                    found_data.title = tag.get("content")
                # artist
                elif tag.get("property") == "music:musician":
                    soup = Deezer.get_webpage(tag.get("content"))
                    tags = soup.findAll("meta")
                    for tag in tags:
                        if tag.get("property") == "og:title":
                            found_data.artist = tag.get("content")
                # description
                elif tag.get("property") == "og:description":
                    found_data.description = tag.get("content")
                # release_date
                elif tag.get("name") == "music:release_date":
                    found_data.release_date = tag.get("content")
                    
        # Refill NoneType values with "Unknown"
        for key, value in found_data.__dict__.items():
            if value == None:
                found_data.__dict__[key] = "Unknown"
                
        return found_data
    
    
class SongData:
    
    artwork_url: str
    duration: int
    genre: str
    album: str
    title: str
    artist: str
    release_date: str
    
    def __init__(self):
        self.artwork_url = None
        self.duration = None
        self.genre = None
        self.album = None
        self.title = None
        self.artist = None
        self.release_date = None
    
class AlbumData:
    
    artwork_url: str
    title: str
    artist: str
    description: str
    release_date: str
    
    def __init__(self):
        self.artwork_url = None
        self.title = None
        self.artist = None
        self.description = None
        self.release_date = None
        
if __name__ == "__main__":
        
    logger = logging.getLogger("Deezer")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    
    deezer = Deezer("https://www.deezer.com/es/track/1566859182?host=0", logger)
    song_metadata = deezer.get_song()
    deezer = Deezer("https://www.deezer.com/es/album/275547892", logger)
    album_metadata = deezer.get_album()
    
    print("\nOrder: artwork_url, duration, genre, album, title, artist, release_date")
    
    print(song_metadata, "\n", song_metadata.artwork_url, "\n", song_metadata.duration, "\n", song_metadata.genre, "\n", song_metadata.album, "\n", song_metadata.title, "\n", song_metadata.artist, "\n", song_metadata.release_date, "\n")
    
    print("\nOrder: artwork_url, title, artist, description, release_date")
    
    print(album_metadata, "\n", album_metadata.artwork_url, "\n", album_metadata.title, "\n", album_metadata.artist, "\n", album_metadata.description, "\n", album_metadata.release_date, "\n")