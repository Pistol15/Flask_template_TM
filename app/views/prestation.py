from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)

prestation_bp = Blueprint('prestation', __name__, url_prefix='/prestation')

@prestation_bp.route('/prestation', methods=('GET', 'POST'))
def prestation():
    return render_template("Prestation/prestation.html")