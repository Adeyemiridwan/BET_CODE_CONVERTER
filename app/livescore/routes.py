from flask import render_template
from flask_login import login_required
from . import livescore_bp

@livescore_bp.route("/")
@login_required
def livescore():
    return render_template(
        "common/coming_soon.html",
        title="LiveScore"
    )