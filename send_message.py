from flask import jsonify, request
from database import Group
from twilio.rest import Client
import os

def send_message_to_group():
    data = request.get_json()

    # Extract necessary data from request
    group_id = data.get('group_id')
    message = data.get('message')

    # Fetch the group from the database
    group = Group.query.filter_by(id=group_id).first()

    if group is None:
        return jsonify({'error': 'Group not found'}), 404

    # Send the message to the group
    account_sid = os.environ['AC977127e77386524a5006eecbe2274968']
    auth_token = os.environ['8a5e37bdaa418903603c18b4c3852e9b']
    client = Client(account_sid, auth_token)

    for member in group.members:
        message = client.messages.create(
            body=message,
            from_='whatsapp:' + os.environ['+16074007197'],
            to='whatsapp:' + member.phone_number
        )

    return jsonify({'message': 'Message sent to group successfully'}), 200
