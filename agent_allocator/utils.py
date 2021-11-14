import requests

BASE_URL = 'https://multichannel.qiscus.com'
_APP_CODE = 'levor-xygzjzzdpnaa8jt'
_APP_SECRET = '6733c0b3d61210de875c21d615b9ab39'
_ADMIN_TOKEN = 'QEX9CCgl9xREBcmZfhWHpuYcZpW0otGObdBVPU97QFt'


def is_chat_event(payload):
    """
    Check if data from webhook is chat event data

    Args:
        payload: data from webhook
    
    Returns:
        True if chat event, False otherwise
    """
    chat_keys_set = {
        'app_id', 'avatar_url', 'candidate_agent', 'email', \
        'extras', 'is_new_session', 'is_resolved', 'latest_service', \
        'name', 'room_id', 'source'
    }
    data_keys_set = set(payload.keys())
    if data_keys_set == chat_keys_set:
        return True
    return False

def is_resolved_event(payload):
    """
    Check if data from webhook is resolved event data

    Args:
        payload: data from webhook
    
    Returns:
        True if resolved event, False otherwise
    """
    resolve_keys_set = {'customer', 'resolved_by', 'service'}
    data_keys_set = set(payload.keys())
    if data_keys_set == resolve_keys_set:
        return True
    return False

def get_agent_by_id(agent_ids):
    """
    Get agent(s) data using Get Agent by IDs endpoint

    Args:
        agent_id: agent id list
    
    Returns:
        dictionary of agent data
    """
    url = '{}/api/v1/admin/agents/get_by_ids'.format(BASE_URL)
    id_params = ['ids[]={}'.format(id) for id in agent_ids]
    id_params = '&'.join(id_params)
    headers = {
        'Content-Type': 'application/json',
        'Qiscus-App-Id': _APP_CODE,
        'Qiscus-Secret-Key': _APP_SECRET,
    }
    response = requests.request("GET", url, headers=headers, params=id_params)
    return response.json()

def is_agent_available(agent_data):
    """
    Check if an agent is available to be assigned to a room
    by checking if agent's customer count < 2

    Args:
        agent_data: agent data returned from Get Agent by IDs endpoint
    
    Returns:
        True if agent available, False otherwise
    """
    available = agent_data.get('is_available', None)
    count = agent_data.get('current_customer_count', None)
    if available is not None and count is not None:
        if available and count < 2:
            return True
    return False

def get_available_agent():
    """
    Get agent availability using is_agent_available
    for all known agents.
    This function and is_agent_available function are
    made because the 'current_customer_count' data
    from Get All Agent endpoint is not updated
    immediately for some reason after there is a change,
    hence the hardcoded agent ids.
    
    Returns:
        agent data dictionary
    """
    agent_ids = [150850, 150851, 150880]
    agents = get_agent_by_id(agent_ids)['data']
    for agent in agents:
        free = is_agent_available(agent)
        if free:
            return agent
    return None

def assign_agent(room_id, agent_id):
    """
    Assing agent to a room using Post Assign Agent endpoint

    Args:
        agent_id: agent id
        room_id: room id
    
    Returns:
        response as documented
    """

    url = '{}/api/v1/admin/service/assign_agent'.format(BASE_URL)
    payload='room_id={}&agent_id={}&max_agent=2'.format(room_id, agent_id)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Qiscus-App-Id': _APP_CODE,
        'Qiscus-Secret-Key': _APP_SECRET
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()