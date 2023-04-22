from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from flask import Blueprint, render_template
from models import Group
from database import db

app = Flask(__name__, template_folder='list_groups.html')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///whatsapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize db
db.init_app(app)

list_groups_bp = Blueprint('list_groups', __name__)

# Set TEMPLATES_AUTO_RELOAD to True if not defined
if 'TEMPLATES_AUTO_RELOAD' not in app.config:
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    
@list_groups_bp.route('/')
def get_all_groups():
    groups = Group.query.all()
    return render_template('list_groups.html', groups=groups)

def add_groups_to_db():
    groups = [
        Group(group_name='Group A', group_link='https://chat.whatsapp.com/groupa'),
        Group(group_name='Group B', group_link='https://chat.whatsapp.com/groupb'),
        Group(group_name='Group C', group_link='https://chat.whatsapp.com/groupc')
    ]
    db.session.add_all(groups)
    db.session.commit()
    
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    admin_name = db.Column(db.String(200), nullable=False)
    admin_phone = db.Column(db.String(20), nullable=False)
    members = db.Column(db.PickleType, nullable=False)
    total_members = db.Column(db.Integer, nullable=False)

def get_groups():
    """
    Function to retrieve all groups from the database
    """
    groups = Group.query.all()
    return groups

def get_group_details(group_id):
    """
    Function to retrieve details of a specific group from the database
    """
    group = Group.query.filter_by(id=group_id).first()
    return group

def create_groups_sheet():
    """
    Function to create a new Google Sheet to store group details
    """
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    sheet_name = 'Groups'
    worksheet = client.create(sheet_name).sheet1
    headers = ['Group Name', 'Admin Name', 'Admin Phone', 'Members', 'Total Members']
    worksheet.append_row(headers)
    return worksheet.id

def get_groups_data():
    """
    Function to retrieve data of all groups from the Google Sheet
    """
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    worksheet_id = create_groups_sheet()
    worksheet = client.open_by_key(worksheet_id).sheet1
    groups_data = worksheet.get_all_values()[1:]
    return groups_data

def add_group_to_db(group_data):
    """
    Function to add a new group to the database
    """
    group = Group(name=group_data['name'], admin_name=group_data['admin_name'], admin_phone=group_data['admin_phone'], members=group_data['members'], total_members=group_data['total_members'])
    db.session.add(group)
    db.session.commit()

def add_groups_to_db():
    """
    Function to add all groups to the database
    """
    groups_data = get_groups_data()
    for group_data in groups_data:
        group = {
            'name': group_data[0],
            'admin_name': group_data[1],
            'admin_phone': group_data[2],
            'members': group_data[3],
            'total_members': group_data[4]
        }
        add_group_to_db(group)

@app.route('/')
def groups():
    """
    Function to display a list of all groups
    """
    groups = get_groups()
    return render_template('groups.html', groups=groups)

@app.route('/group/<int:group_id>')
def group(group_id):
    """
    Function to display details of a specific group
    """
    group = get_group_details(group_id)
    return render_template('group.html', group=group)

if __name__ == '__main__':
    db.create_all()
    add_groups_to_db()

    app.run()