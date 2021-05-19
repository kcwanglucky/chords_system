from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    # __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(120), unique=True, nullable=False)

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

class Chord(db.Model):
    # __tablename__ = 'chords'

    name = Column(String(80), unique=True, nullable=False, primary_key=True)
    url = Column(String(150), nullable=False, primary_key=True)
    key = Column(String(10), nullable=False)
    artist = Column(String(80))

    def __init__(self, name=None, url=None, key=None, artist=None):
        self.name = name
        self.url = url
        self.key = key
        self.artist = artist

    def __repr__(self):
        # return '<Song Info>\n \t<Name %r>\n \t<Name %r>\n \t<URL %r>\n \t<Key %r>\n' % \
        #     self.username
        
        return "<Song Info>\n \t<Name {}>\n \t<Artist {}>\n \t<Key {}>\n \t<URL {}>\n".format( \
            self.name, self.artist, self.key, self.url)
