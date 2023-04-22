from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from database import db, create_tables
from list_groups import get_all_groups
from group_details import get_group_details
from send_message import send_message_to_group
import os

def create_app():
    app = Flask(__name__, template_folder='list_groups.html')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///groups.db'
    # register the SQLAlchemy instance with the Flask app
    db.init_app(app)
    
    with app.app_context():
        create_tables()

     # Set TEMPLATES_AUTO_RELOAD to True if not defined
    if 'TEMPLATES_AUTO_RELOAD' not in app.config:
        app.config['TEMPLATES_AUTO_RELOAD'] = True

      # create a route for the home page
    @app.route('/home')
    def index():
        with app.app_context():
            groups = get_all_groups()
            return render_template('list_groups.html', groups=groups)
        
    # suppress a warning
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # create a route for the group details page
    @app.route('/group_details/<int:group_id>')
    def group_details(group_id):
        return render_template('group_details.html', group=get_group_details(group_id))

    # create a route for sending message to a group
    @app.route('/send_message', methods=['POST'])

    def send_message():
        return send_message_to_group()

    return app
    
# start the app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
