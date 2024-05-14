from flask import (Blueprint, current_app, flash, g, redirect, render_template, request, send_from_directory, session, url_for)
from app.utils import login_required
from app.db.db import get_db
import os

galerie_bp = Blueprint('galerie', __name__, url_prefix='/galerie')

@galerie_bp.route('/', methods=['GET'])
@login_required
def show_galeries():
    galeries = get_galeries()
    file_contents = read_files(galeries)
    return render_template('user/galerie.html', file_contents=file_contents)

def get_galeries():
    Personne_ID = session.get('Personne_ID')
    if Personne_ID is None:
        return redirect(url_for('auth.login'))
    
    db = get_db()
    galeries = db.execute('SELECT chemin_galerie FROM Galeries WHERE Personne_ID = ?', (Personne_ID,)).fetchall()
    db.close()
    return [galerie['chemin_galerie'] for galerie in galeries]

def read_files(galeries):
    file_contents = []
    for galerie in galeries:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], galerie)
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                file_contents.append({'path': galerie, 'content': content})
        except FileNotFoundError:
            flash(f'File not found: {file_path}')
    return file_contents
