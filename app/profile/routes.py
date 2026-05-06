# ================= PROFILE ROUTES =================

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app
)

from flask_login import (
    login_required,
    current_user
)

from app.extensions import db
from . import profile_bp

import os
from werkzeug.utils import secure_filename


# ================= CONFIG =================

UPLOAD_FOLDER = "static/uploads"

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}


# ================= CHECK EXTENSION =================

def allowed_file(filename):

    return (
        "." in filename
        and
        filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# ================= PROFILE =================

@profile_bp.route("/", methods=["GET", "POST"])
@login_required
def profile():

    if request.method == "POST":

        # ================= FORM DATA =================

        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        username = request.form.get("username")
        phone = request.form.get("phone")

        # ================= UPDATE USER =================

        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.username = username
        current_user.phone = phone

        # ================= IMAGE =================

        image = request.files.get("image")

        if image and image.filename != "":

            # VALIDATE IMAGE TYPE
            if not allowed_file(image.filename):

                flash(
                    "Only PNG, JPG, JPEG and WEBP images are allowed",
                    "error"
                )

                return redirect(url_for("profile.profile"))

            # SAFE FILE NAME
            filename = secure_filename(image.filename)

            # UNIQUE FILE NAME
            unique_name = f"{current_user.id}_{filename}"

            # FULL PATH
            upload_path = os.path.join(
                current_app.root_path,
                UPLOAD_FOLDER,
                unique_name
            )

            # CREATE FOLDER IF NOT EXISTS
            os.makedirs(
                os.path.dirname(upload_path),
                exist_ok=True
            )

            # SAVE IMAGE
            image.save(upload_path)

            # DELETE OLD IMAGE
            if (
                current_user.image
                and
                current_user.image != "default.png"
            ):

                old_path = os.path.join(
                    current_app.root_path,
                    UPLOAD_FOLDER,
                    current_user.image
                )

                if os.path.exists(old_path):

                    try:
                        os.remove(old_path)
                    except:
                        pass

            # SAVE TO DATABASE
            current_user.image = unique_name

        # ================= SAVE =================

        db.session.commit()

        flash(
            "Profile updated successfully",
            "success"
        )

        return redirect(url_for("profile.profile"))

    return render_template(
        "profile/profile.html"
    )