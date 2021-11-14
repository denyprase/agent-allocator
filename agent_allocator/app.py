from flask import Flask
from flask import request
from werkzeug.wrappers import response
from agent_allocator.utils import (
    is_chat_event,
    is_resolved_event,
    get_available_agent,
    assign_agent
)
from queue import Queue

app = Flask(__name__)

q = Queue()

@app.route("/", methods=['POST'])
def index():
    data = request.json
    if is_chat_event(data):
        room_id = data.get('room_id')
        user_email = data.get('email')
        message = (room_id, user_email)
        if message in q.queue:
            return 'OK'
        agent = get_available_agent()
        if agent:
            response = assign_agent(room_id, agent['id'])
            return response
        q.put(message)
        return {
            'status': 'added to queue'
        }
    if is_resolved_event(data):
        if len(q.queue) > 0:
            data = q.get()
            room_id, user_email = data
            agent = get_available_agent()
            if agent:
                response = assign_agent(room_id, agent['id'])
                return response
        return 'OK'

