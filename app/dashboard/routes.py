from flask import flash, render_template
from flask_login import login_required, current_user
from app.models.wallet import Wallet
from app.models.conversion import Conversion
from app.extensions import db
from . import dashboard_bp
from collections import defaultdict


@dashboard_bp.route("/")
@login_required
def dashboard():

    wallet = Wallet.query.filter_by(user_id=current_user.id).first()

    conversions = (
        Conversion.query.filter_by(user_id=current_user.id)
        .order_by(Conversion.created_at.desc())
        .all()
    )

    recent_activities = (
        Conversion.query.filter_by(user_id=current_user.id)
        .order_by(Conversion.created_at.desc())
        .limit(5)
        .all()
    )

    total_conversions = len(conversions)

    total_fees = sum(c.fee_charged for c in conversions)


    date_map = defaultdict(int)
    fee_map = defaultdict(float)

    for c in conversions:
        date = c.created_at.strftime("%Y-%m-%d")
        date_map[date] += 1
        fee_map[date] += c.fee_charged

    dates = list(date_map.keys())
    counts = list(date_map.values())
    fees = list(fee_map.values())

    return render_template(
        "dashboard/dashboard.html",
        recent_activities=recent_activities,
        wallet=wallet,
        conversions=conversions,
        total_conversions=total_conversions,
        total_fees=total_fees,
        dates=dates,
        fees=fees,
        counts=counts,
    )


@dashboard_bp.route("/history")
@login_required
def history():

    conversions = (
        Conversion.query.filter_by(user_id=current_user.id)
        .order_by(Conversion.created_at.desc())
        .all()
    )

    return render_template("dashboard/history.html", conversions=conversions)