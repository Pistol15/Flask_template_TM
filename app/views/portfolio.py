from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)

portfolio_bp = Blueprint('portfolio', __name__, url_prefix='/portfolio')

@portfolio_bp.route('/portfolio', methods=('GET', 'POST'))
def portfolio():
    return render_template("Portfolio/portfolio.html")