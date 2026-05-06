# ================= AUTH ROUTES =================

import random
import uuid

from flask import (
    render_template,
    redirect,
    url_for,
    request,
    flash,
    session,
    jsonify
)

from flask_login import (
    login_user,
    logout_user,
    current_user,
    login_required
)

from . import auth_bp
from app.extensions import db
from app.models.user import User
from app.models.wallet import Wallet


# =========================================================
# LOGIN
# =========================================================

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    # BLOCK AUTHENTICATED USERS
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":

        identifier = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        # FIND USER
        user = User.query.filter(
            (User.email == identifier) |
            (User.phone == identifier) |
            (User.username == identifier)
        ).first()

        # INVALID LOGIN
        if not user or not user.check_password(password):

            flash("Invalid login details", "error")

            return redirect(url_for("auth.login"))

        # LOGIN USER
        login_user(user)

        # SESSION TOKEN
        token = str(uuid.uuid4())

        user.session_token = token

        db.session.commit()

        session["session_token"] = token

        flash("Login successful", "success")

        return redirect(url_for("dashboard.dashboard"))

    return render_template("auth/login.html")


# =========================================================
# SIGNUP
# =========================================================

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":

        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()

        password = request.form.get("password", "").strip()
        confirm_password = request.form.get(
            "confirm_password",
            ""
        ).strip()

        # PASSWORD CHECK
        if password != confirm_password:

            flash("Passwords do not match", "error")

            return redirect(url_for("auth.signup"))

        # EMAIL CHECK
        if User.query.filter_by(email=email).first():

            flash("Email already exists", "error")

            return redirect(url_for("auth.signup"))

        # USERNAME CHECK
        if User.query.filter_by(username=username).first():

            flash("Username already exists", "error")

            return redirect(url_for("auth.signup"))

        # PHONE CHECK
        if User.query.filter_by(phone=phone).first():

            flash("Phone already exists", "error")

            return redirect(url_for("auth.signup"))

        # CREATE USER
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            phone=phone
        )

        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        # CREATE WALLET
        wallet = Wallet(
            user_id=new_user.id,
            balance=0
        )

        db.session.add(wallet)
        db.session.commit()

        flash(
            "Account created successfully",
            "success"
        )

        return redirect(url_for("auth.login"))

    return render_template("auth/signup.html")


# =========================================================
# FORGOT PASSWORD
# =========================================================

@auth_bp.route(
    "/forgot-password",
    methods=["GET", "POST"]
)
def forgot_password():

    if request.method == "POST":

        identifier = request.form.get(
            "email",
            ""
        ).strip()

        # FIND USER
        user = User.query.filter(
            (User.email == identifier) |
            (User.phone == identifier) |
            (User.username == identifier)
        ).first()

        # USER NOT FOUND
        if not user:

            flash("No account found", "error")

            return redirect(
                url_for("auth.forgot_password")
            )

        # SAVE TEMP SESSION
        session["temp_user_id"] = user.id

        return redirect(
            url_for("auth.select_verification")
        )

    return render_template(
        "auth/forgot_password.html"
    )


# =========================================================
# SELECT VERIFICATION
# =========================================================

@auth_bp.route("/select-verification")
def select_verification():

    user_id = session.get("temp_user_id")

    if not user_id:

        flash("Session expired", "error")

        return redirect(
            url_for("auth.forgot_password")
        )

    user = User.query.get(user_id)

    # MASK EMAIL
    def mask_email(email):

        if not email:
            return ""

        name, domain = email.split("@")

        return f"{name[0]}***@{domain}"

    # MASK PHONE
    def mask_phone(phone):

        if not phone:
            return ""

        return (
            phone[:3] +
            "****" +
            phone[-2:]
        )

    return render_template(
        "auth/select_verification.html",
        user=user,
        masked_email=mask_email(user.email),
        masked_phone=mask_phone(user.phone)
    )


# =========================================================
# SEND RESET CODE
# =========================================================

@auth_bp.route("/send-reset-code/<method>")
def send_reset_code(method):

    user_id = session.get("temp_user_id")

    if not user_id:
        flash("Session expired", "error")
        return redirect(url_for("auth.forgot_password"))

    user = User.query.get(user_id)

    if not user:
        flash("User not found", "error")
        return redirect(url_for("auth.forgot_password"))

    # GENERATE CODE
    code = str(random.randint(1000, 9999))

    user.verification_code = code
    user.verification_type = "reset"

    db.session.commit()

    # IMPORTANT
    session["reset_user_id"] = user.id

    # TEMP TESTING
    flash(f"Verification code: {code}", "success")

    return redirect(url_for("auth.verify_code"))


# =========================================================
# VERIFY CODE
# =========================================================

@auth_bp.route("/verify-code", methods=["GET", "POST"])
def verify_code():

    user = None

    # RESET FLOW
    if "reset_user_id" in session:
        user = User.query.get(session["reset_user_id"])

    # NORMAL LOGGED USER FLOW
    elif current_user.is_authenticated:
        user = current_user

    if not user:
        flash("Session expired", "error")
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        code = request.form.get("code")

        # CHECK CODE
        if code != user.verification_code:

            flash("Invalid verification code", "error")

            return redirect(url_for("auth.verify_code"))

        # SUCCESS
        if user.verification_type == "email":
            user.is_email_verified = True

        elif user.verification_type == "phone":
            user.is_phone_verified = True

        elif user.verification_type == "reset":

            # KEEP SESSION ACTIVE
            session["reset_user_id"] = user.id

        # CLEAR CODE AFTER SUCCESS
        user.verification_code = None
        user.verification_type = None

        db.session.commit()

        flash("Verification successful", "success")

        return redirect(url_for("auth.reset_password"))

    return render_template("auth/verify_code.html")


# =========================================================
# SEND VERIFICATION
# =========================================================

@auth_bp.route("/send-verification/<type>")
@login_required
def send_verification(type):

    code = str(random.randint(1000, 9999))

    current_user.verification_code = code
    current_user.verification_type = type

    db.session.commit()

    # TEMP
    return jsonify({
        "success": True,
        "message": f"Verification code: {code}"
    })


# =========================================================
# RESEND CODE
# =========================================================

@auth_bp.route("/resend-code")
def resend_code():

    user = None

    if "reset_user_id" in session:
        user = User.query.get(session["reset_user_id"])

    elif current_user.is_authenticated:
        user = current_user

    if not user:
        return jsonify({
            "success": False,
            "message": "Session expired"
        })

    # GENERATE NEW CODE
    code = str(random.randint(1000, 9999))

    user.verification_code = code

    db.session.commit()

    # TEMP TEST MODE
    return jsonify({
        "success": True,
        "message": f"New verification code: {code}"
    })


# =========================================================
# RESET PASSWORD
# =========================================================

@auth_bp.route(
    "/reset-password",
    methods=["GET", "POST"]
)
def reset_password():

    user_id = session.get("reset_user_id")

    if not user_id:

        flash(
            "Session expired. Start again.",
            "error"
        )

        return redirect(
            url_for("auth.forgot_password")
        )

    user = User.query.get(user_id)

    if request.method == "POST":

        password = request.form.get(
            "password",
            ""
        ).strip()

        confirm = request.form.get(
            "confirm_password",
            ""
        ).strip()

        # PASSWORD CHECK
        if password != confirm:

            flash(
                "Passwords do not match",
                "error"
            )

            return redirect(
                url_for("auth.reset_password")
            )

        # UPDATE PASSWORD
        user.set_password(password)

        # CLEAR VERIFY
        user.verification_code = None
        user.verification_type = None

        db.session.commit()

        # CLEAR SESSION
        session.pop("reset_user_id", None)
        session.pop("temp_user_id", None)

        flash(
            "Password updated successfully",
            "success"
        )

        return redirect(url_for("auth.login"))

    return render_template(
        "auth/reset_password.html"
    )


# =========================================================
# LOGOUT
# =========================================================

@auth_bp.route("/logout")
@login_required
def logout():

    session.pop("session_token", None)

    logout_user()

    flash("Logged out successfully", "success")

    return redirect(url_for("main.home"))