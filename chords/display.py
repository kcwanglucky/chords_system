from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from chords.db_models import db, Chord, User
import validators

from chords.auth import login_required
bp = Blueprint('display', __name__)    # no url_prefix because treating it as a main index

@bp.route('/')
def index():
    chords = db.session.query(Chord).all()
    return display(chords)

def display(chords, query=False):
    return render_template('chords/index.html', chords=chords, query=query)

@bp.route('/add_chords', methods=('GET', 'POST'))
@login_required
def add_chords():
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        key = request.form['key']
        artist = request.form['artist']

        error = None

        if not name:
            error = "Song name is required."
        else:
            prev_add = Chord.query.filter(
                Chord.name == name
            ).first()

            if prev_add:
                error = 'This song {} is already added.'.format(name)

        if not validators.url(url):
            error = 'Invalid URL'

        if error is not None:
            flash(error)
        else:
            new_song = Chord(
                name = name,
                url = url,
                key = key,
                artist = artist,
            )
            db.session.add(new_song)  # Adds new User record to database
            db.session.commit()  # Commits all changes

            return redirect(url_for('display.index'))

    return render_template('chords/add_song.html')

@bp.route('/<name>/update', methods=('GET', 'POST'))
@login_required
def update(name):
    chord = db.session.query(Chord).filter(
        Chord.name == name
    ).first()

    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        key = request.form['key']
        artist = request.form['artist']

        error = None

        if not name:
            error = "Song name is required."

        if error is not None:
            flash(error)
        else:
            chord.name = name
            chord.url = url
            chord.key = key
            chord.artist = artist

            db.session.commit()
            return redirect(url_for('display.index'))

    return render_template('chords/update.html', chord=chord)

@bp.route('/query', methods=('GET', 'POST'))
@bp.route('/<artist>/query')
def query(artist = None):
    chords = db.session.query(Chord).filter(
        Chord.artist == artist
    ).all()
    if chords:
        """
        If it is a query based on artist, then chords is not None.
        Can directly display the songs belonged to the provided artist
        """
        return display(chords, query=artist)

    if request.method == 'POST':
        name = request.form['name']
        artist = request.form['artist']

        error = None

        if not name and not artist:
            error = "Should provide either song name or artist"

        if error is not None:
            flash(error)
        else:
            if name and artist:
                chords = db.session.query(Chord).filter(
                    Chord.name == name,
                    Chord.artist == artist
                ).all()
            elif name:
                chords = db.session.query(Chord).filter(
                    Chord.name == name
                ).all()
            elif artist:
                chords = db.session.query(Chord).filter(
                    Chord.artist == artist
                ).all()
            
            query = ""
            if artist:
                query += artist
            if query and name:
                query += "-" + name
            else:
                query += name
            
            return display(chords, query=query)

    return render_template('chords/query.html')

@bp.route('/artist', methods=('GET',))
def artist():
    artists = db.session.query(Chord.artist).distinct()
    
    return render_template('chords/artist.html', artists=artists)

@bp.route('/<name>/delete', methods=('POST',))
@login_required
def delete(name):
    chord = db.session.query(Chord).filter(
        Chord.name == name
    ).first()

    db.session.delete(chord)
    return redirect(url_for('display.index'))
