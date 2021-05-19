from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from chords.db_models import db, Chord, User
import validators

from chords.auth import login_required
bp = Blueprint('song_display', __name__)    # no url_prefix because treating it as a main index

@bp.route('/')
def index():
    chords = Chord.query.all()

    return render_template('chords/index.html', chords=chords)

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
            )  # Create an instance of the User class
            db.session.add(new_song)  # Adds new User record to database
            db.session.commit()  # Commits all changes

            return redirect(url_for('song_display.index'))

    return render_template('chords/add_song.html')

@bp.route('/<name>/update', methods=('GET', 'POST'))
@login_required
def update(name):
    chord = Chord.query.filter(
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
            return redirect(url_for('song_display.index'))

    return render_template('chords/update.html', chord=chord)

# @bp.route('/sort', methods=('GET', 'POST'))
# @login_required
# def sort():
#     chords = Chord.query.all()

#     if request.method == 'POST':
#         name = request.form['name']
#         artist = request.form['artist']

#         error = None

#         if not name and not artist:
#             error = "Should provide either song name or artist"

#         if error is not None:
#             flash(error)
#         else:
#             if name and artist:
#                 chords = Chord.query.filter(
#                     Chord.name == name,
#                     Chord.artist == artist
#                 ).all()
#             elif name:
#                 chords = Chord.query.filter(
#                     Chord.name == name
#                 ).all()
#             elif artist:
#                 chords = Chord.query.filter(
#                     Chord.artist == artist
#                 ).all()
        
#             return redirect(url_for('song_display.index'))

#     return render_template('chords/sort.html', chords=chords)

@bp.route('/<name>/delete', methods=('POST',))
@login_required
def delete(name):
    chord = Chord.query.filter(
        Chord.name == name
    ).first()

    db.session.delete(chord)
    return redirect(url_for('song_display.index'))
