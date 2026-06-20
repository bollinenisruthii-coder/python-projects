"""
College Enquiry AI Chatbot - Main Flask Application
"""

import os
import logging
from flask import Flask, render_template, send_from_directory, jsonify

from config import config
from database import init_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)


def create_app(config_name: str = 'default') -> Flask:
    """Application factory."""
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # Load config
    app.config.from_object(config[config_name])

    # Ensure upload folder exists
    os.makedirs(app.config.get('UPLOAD_FOLDER', 'static/uploads'), exist_ok=True)

    # Initialize extensions and DB
    init_db(app)

    # Register blueprints
    from routes.auth import auth_bp
    from routes.chat import chat_bp
    from routes.faq import faq_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(faq_bp)
    app.register_blueprint(admin_bp)

    # Train chatbot on startup
    with app.app_context():
        try:
            from chatbot import retrain_chatbot
            retrain_chatbot()
            logger.info("Chatbot trained successfully on startup.")
        except Exception as e:
            logger.error(f"Failed to train chatbot on startup: {e}")

    # ─── Frontend Routes ──────────────────────────────────────────────────────

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login')
    def login_page():
        return render_template('login.html')

    @app.route('/register')
    def register_page():
        return render_template('register.html')

    @app.route('/chatbot')
    def chatbot_page():
        return render_template('chatbot.html')

    @app.route('/profile')
    def profile_page():
        return render_template('profile.html')

    @app.route('/history')
    def history_page():
        return render_template('history.html')

    @app.route('/faq')
    def faq_page():
        return render_template('faq.html')

    @app.route('/about')
    def about_page():
        return render_template('about.html')

    @app.route('/courses')
    def courses_page():
        return render_template('courses.html')

    @app.route('/contact')
    def contact_page():
        return render_template('contact.html')

    @app.route('/admin')
    def admin_page():
        return render_template('admin.html')

    # ─── Error Handlers ───────────────────────────────────────────────────────

    @app.errorhandler(404)
    def not_found(e):
        if _is_api_request():
            return jsonify({'success': False, 'error': 'Resource not found.'}), 404
        return render_template('index.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        logger.error(f"Server error: {e}")
        if _is_api_request():
            return jsonify({'success': False, 'error': 'Internal server error.'}), 500
        return render_template('index.html'), 500

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({'success': False, 'error': 'Method not allowed.'}), 405

    # ─── Health Check ─────────────────────────────────────────────────────────

    @app.route('/api/health')
    def health():
        from chatbot import get_chatbot
        bot = get_chatbot()
        return jsonify({
            'status': 'ok',
            'chatbot_trained': bot.is_trained,
            'faq_count': len(bot.faq_questions) if bot.is_trained else 0
        })

    return app


def _is_api_request() -> bool:
    from flask import request
    return request.path.startswith('/api/')


# ─── Entry Point ──────────────────────────────────────────────────────────────

app = create_app(os.environ.get('FLASK_ENV', 'development'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True') == 'True'
    logger.info(f"Starting College Chatbot on port {port} (debug={debug})")
    app.run(host='0.0.0.0', port=port, debug=debug)
