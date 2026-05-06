from flask import render_template
from flask_login import login_required
from . import predictions_bp

@predictions_bp.route("/")
@login_required
def predictions():
    return render_template(
        "common/coming_soon.html",
        title="Predictions"
    )