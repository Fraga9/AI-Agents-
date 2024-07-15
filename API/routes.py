from flask import Blueprint, request, jsonify
from models import db, Dashboard, Agent, Task

api = Blueprint('api', __name__)

@api.route('/dashboard', methods=['POST'])
def create_dashboard():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Dashboard name is required'}), 400

    dashboard = Dashboard(name=name)
    db.session.add(dashboard)
    db.session.commit()
    return jsonify({'id': dashboard.id, 'name': dashboard.name}), 201

@api.route('/agent', methods=['POST'])
def create_agent():
    data = request.get_json()
    role = data.get('role', 'engineer')  
    goal = data.get('goal', 'Default goal')
    backstory_context = data.get('backstory_context', 'Default context')
    llm = data.get('llm', 'Default llm')
    tools = data.get('tools', 'Default tools')
    max_iter = data.get('max_iter', 10)  
    dashboard_id = data.get('dashboard_id')

    if not dashboard_id:
        return jsonify({'error': 'Dashboard ID is required'}), 400

    agent = Agent(
        role=role,
        goal=goal,
        backstory_context=backstory_context,
        llm=llm,
        tools=tools,
        max_iter=max_iter,
        dashboard_id=dashboard_id
    )
    db.session.add(agent)
    db.session.commit()
    return jsonify({'id': agent.id, 'role': agent.role}), 201

@api.route('/task', methods=['POST'])
def create_task():
    data = request.get_json()
    description = data.get('description')
    agent = data.get('agent')
    expected_output = data.get('expected_output', 'Default output')
    tools = data.get('tools', 'Default tools')
    context = data.get('context', 'Default context')
    dashboard_id = data.get('dashboard_id')

    if not description or not agent or not dashboard_id:
        return jsonify({'error': 'Description, agent, and dashboard ID are required'}), 400

    task = Task(
        description=description,
        agent=agent,
        expected_output=expected_output,
        tools=tools,
        context=context,
        dashboard_id=dashboard_id
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({'id': task.id, 'description': task.description}), 201

@api.route('/dashboard/<int:dashboard_id>', methods=['GET'])
def get_dashboard(dashboard_id):
    dashboard = Dashboard.query.get_or_404(dashboard_id)
    agents = [{'id': agent.id, 'role': agent.role} for agent in dashboard.agents]
    tasks = [{'id': task.id, 'description': task.description} for task in dashboard.tasks]
    return jsonify({'id': dashboard.id, 'name': dashboard.name, 'agents': agents, 'tasks': tasks})
