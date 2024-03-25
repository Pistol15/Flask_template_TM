from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)

prestation_bp = Blueprint('prestation', __name__, url_prefix='/prestation')

@prestation_bp.route('/prestation', methods=('GET', 'POST'))
def prestation():
    return render_template("Prestation/prestation.html")

@prestation_bp.route('/sport', methods=('GET', 'POST'))
def Sport():
    return render_template("Prestation/Sport.html")

@prestation_bp.route('/anniversaire', methods=('GET', 'POST'))
def anniversaire():
    return render_template("Prestation/anniversaire.html")

@prestation_bp.route('/animaux', methods=('GET', 'POST'))
def animaux():
    return render_template("Prestation/animaux.html")

@prestation_bp.route('/portrait', methods=('GET', 'POST'))
def portrait():
    return render_template("Prestation/portrait.html")

@prestation_bp.route('/concert', methods=('GET', 'POST'))
def concert():
    return render_template("Prestation/concert.html")