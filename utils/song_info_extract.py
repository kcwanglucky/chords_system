from chords.db_models import Chord
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Song:
    def __init__(self, name, artist, key, url=None):
        self.name = name
        self.key = key
        self.url = url
        self.artist = artist
    
    def set_url(self, url):
        self.url = url

    def __repr__(self):
        return "Name: {}\nKey: {}\nURL: {}Artist: {}\n".format(
            self.name, self.key, self.url, self.artist
        )

def extract(input_file):
    """
    Extract the song-chord info from given `input_file`
    Return a list of `Song` class objects
    """
    with open(input_file) as f:
        lines = f.readlines()
        f.close()
    
    songs = []
    song = None
    for line in lines:
        if line == '\n':
            continue

        if line[0] == '^':
            # To mark the songs I am not familiar
            line = line[1:]

        if song:
            # Second line: Looking for the url
            song.set_url(line)
            songs.append(song)
            song = None
        else:
            # First line: Looking for name, key, artist
            line = line.split()
            if len(line) >= 3:
                if line[0].isascii():
                    continue
                # info enough: Do not lack info
                song = Song(line[0], line[1], line[2])
    
    return songs

if __name__ == "__main__":
    songs = extract("entry.txt")

    engine = create_engine("sqlite:////tmp/test.db")
    Session = sessionmaker(engine)

    with Session() as session:
        for song in songs:
            print(song)
            new_song = Chord(
                name = song.name,
                url = song.url,
                key = song.key,
                artist = song.artist,
            )
        
            prev_add = session.query(Chord).filter(
                Chord.url == new_song.url
            ).first()

            if not prev_add:
                session.add(new_song)  # Adds new User record to database
                session.commit()  # Commits all changes
