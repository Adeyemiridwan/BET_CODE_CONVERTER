from flask import Flask, app, url_for, session, redirect, url_for
from .config import Config
from .extensions import db, login_manager, migrate
from flask_login import current_user, logout_user
from app.extensions import db, login_manager


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # 🔥 ADD THIS HERE
    @app.before_request
    def check_session():

        if current_user.is_authenticated:

            if session.get("session_token") != current_user.session_token:
                logout_user()
                return redirect(url_for("auth.login"))

    # Import Blueprints
    from .main.routes import main_bp
    from .auth.routes import auth_bp
    from .dashboard.routes import dashboard_bp
    from .converter.routes import converter_bp
    from .wallet.routes import wallet_bp
    from .profile.routes import profile_bp
    from .livescore.routes import livescore_bp
    from .predictions.routes import predictions_bp


    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(converter_bp)
    app.register_blueprint(wallet_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(livescore_bp)
    app.register_blueprint(predictions_bp)

    return app