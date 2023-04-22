from typing import List, Dict
from models import Group

def get_group_data(group_name):
    group = Group.query.filter_by(name=group_name).first()

    if not group:
        group = Group(name=group_name)
        group.save()

    return group

def extract_group_data(group) -> Dict:
    """
    Extracts group data from a Twilio API response object.
    """
    group_data = {
        'group_sid': group.sid,
        'group_name': group.friendly_name,
        'created_by': group.created_by,
        'created_date': group.date_created,
        'updated_date': group.date_updated,
        'members': []
    }

    for member in group.members.list():
        member_data = {
            'member_sid': member.sid,
            'phone_number': member.phone_number,
            'name': member.friendly_name,
            'joined_date': member.date_created
        }
        group_data['members'].append(member_data)

    return group_data

def get_total_group_members(group_data: Dict) -> int:
    """
    Returns the total number of group members in a group data dictionary.
    """
    return len(group_data['members'])

def get_group_members(group_data: Dict) -> List[Dict]:
    """
    Returns a list of dictionaries containing information about the members of a group.
    """
    return group_data['members']

def filter_admins(members: List[Dict]) -> List[Dict]:
    """
    Filters a list of group member dictionaries to only include members who are not group admins.
    """
    return [member for member in members if not member['is_admin']]
