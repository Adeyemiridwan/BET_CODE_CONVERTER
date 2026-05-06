from . import wallet_bp
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.wallet import Wallet
from app.models.transaction import Transaction
from app.models.user import User
from app.extensions import db


@wallet_bp.route("/", methods=["GET", "POST"])
@login_required
def wallet():

    wallet = Wallet.query.filter_by(user_id=current_user.id).first()

    # 🔴 Ensure wallet exists
    if not wallet:
        wallet = Wallet(user_id=current_user.id, balance=0)
        db.session.add(wallet)
        db.session.commit()

    transactions = (
        Transaction.query.filter_by(user_id=current_user.id)
        .order_by(Transaction.created_at.desc())
        .all()
    )

    if request.method == "POST":

        action = request.form.get("action")

        try:
            amount = float(request.form.get("amount"))
        except:
            flash("Invalid amount format", "error")
            return redirect(url_for("wallet.wallet"))

        # ================= DEPOSIT =================
        if action == "deposit":

            if amount <= 0:
                flash("Amount must be greater than 0", "error")
                return redirect(url_for("wallet.wallet"))

            wallet.balance += amount

            db.session.add(Transaction(
                user_id=current_user.id,
                type="deposit",
                amount=amount
            ))

            flash("Funds added successfully", "success")

        # ================= WITHDRAW =================
        elif action == "withdraw":

            if amount <= 0:
                flash("Invalid amount", "error")
                return redirect(url_for("wallet.wallet"))

            if amount > wallet.balance:
                flash("Insufficient balance", "error")
                return redirect(url_for("wallet.wallet"))

            wallet.balance -= amount

            db.session.add(Transaction(
                user_id=current_user.id,
                type="withdraw",
                amount=amount
            ))

            flash("Withdrawal successful", "success")

        # ================= TRANSFER =================
        elif action == "transfer":

            receiver_email = request.form.get("receiver")

            receiver = User.query.filter_by(email=receiver_email).first()

            if not receiver:
                flash("User not found", "error")
                return redirect(url_for("wallet.wallet"))

            if receiver.id == current_user.id:
                flash("You cannot send money to yourself", "error")
                return redirect(url_for("wallet.wallet"))

            if amount <= 0:
                flash("Invalid amount", "error")
                return redirect(url_for("wallet.wallet"))

            if amount > wallet.balance:
                flash("Insufficient balance", "error")
                return redirect(url_for("wallet.wallet"))

            receiver_wallet = Wallet.query.filter_by(user_id=receiver.id).first()

            # 🔴 Create receiver wallet if not exists
            if not receiver_wallet:
                receiver_wallet = Wallet(user_id=receiver.id, balance=0)
                db.session.add(receiver_wallet)

            # 🔒 ATOMIC TRANSACTION
            try:
                wallet.balance -= amount
                receiver_wallet.balance += amount

                db.session.add(Transaction(
                    user_id=current_user.id,
                    type="transfer_out",
                    amount=amount
                ))

                db.session.add(Transaction(
                    user_id=receiver.id,
                    type="transfer_in",
                    amount=amount
                ))

                flash("Transfer successful", "success")

            except Exception as e:
                db.session.rollback()
                flash("Transfer failed", "error")
                return redirect(url_for("wallet.wallet"))

        db.session.commit()
        return redirect(url_for("wallet.wallet"))

    return render_template(
        "wallet/wallet.html",
        wallet=wallet,
        transactions=transactions
    )