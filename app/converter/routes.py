from flask import render_template, request, redirect, session, url_for, flash
from flask_login import login_required, current_user
from app.models.wallet import Wallet
from app.models.conversion import Conversion
from app.models.transaction import Transaction
from app.extensions import db
from . import converter_bp


@converter_bp.route("/", methods=["GET", "POST"])
@login_required
def converter():

    wallet = Wallet.query.filter_by(user_id=current_user.id).first()

    if not wallet:
        flash("Wallet not found")
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":

        input_code = request.form.get("code")

        if not input_code:
            flash("Please enter a code")
            return redirect(url_for("converter.converter"))

        user_conversions = Conversion.query.filter_by(user_id=current_user.id).count()

        if user_conversions > 100:
            flash("Daily conversion limit reached")
            return redirect(url_for("dashboard.dashboard"))

        CONVERSION_FEE = 0.20

        if wallet.balance < CONVERSION_FEE:
            flash("Insufficient wallet balance")
            return redirect(url_for("converter.converter"))

        output_code = input_code[::-1]

        wallet.balance -= CONVERSION_FEE

        conversion = Conversion(
            user_id=current_user.id,
            input_code=input_code,
            output_code=output_code,
            fee_charged=CONVERSION_FEE,
        )

        transaction = Transaction(
            user_id=current_user.id, type="conversion_fee", amount=CONVERSION_FEE
        )

        db.session.add(transaction)

        db.session.add(conversion)
        db.session.commit()

        flash("Code converted successfully")
        
        # AFTER conversion, store the converted code in the session to display in the template

        session["converted_code"] = output_code

        return redirect(url_for("converter.converter"))

    converted_code = session.pop("converted_code", None)

    return render_template(
    "converter/converter.html",
    result=converted_code,
    show_modal=True if converted_code else False
)