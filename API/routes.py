from flask import Blueprint, request, jsonify
from models import db, Project, Agent, Task

api = Blueprint('api', __name__)

@api.route('/project', methods=['POST'])
def create_project():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Project name is required'}), 400

    # Updated to include new optional fields from Project model
    project = Project(
        name=name,
        process=data.get('process'),
        verbose=data.get('verbose'),
        manager_llm=data.get('manager_llm'),
        function_calling_llm=data.get('function_calling_llm'),
        config=data.get('config'),
        max_rpm=data.get('max_rpm'),
        language=data.get('language'),
        language_file=data.get('language_file'),
        memory=data.get('memory'),
        cache=data.get('cache'),
        embedder=data.get('embedder'),
        full_output=data.get('full_output'),
        step_callback=data.get('step_callback'),
        task_callback=data.get('task_callback'),
        share_crew=data.get('share_crew'),
        output_log_file=data.get('output_log_file'),
        manager_agent=data.get('manager_agent'),
        manager_callbacks=data.get('manager_callbacks'),
        prompt_file=data.get('prompt_file')
    )
    db.session.add(project)
    db.session.commit()
    return jsonify({'id': project.id, 'name': project.name}), 201

@api.route('/agent', methods=['POST'])
def create_agent():
    data = request.get_json()
    # Updated to match the Agent model changes
    agent = Agent(
        role=data.get('role', 'engineer'),
        goal=data.get('goal', 'Default goal'),
        backstory=data.get('backstory_context', 'Default context'),
        llm=data.get('llm', 'Default llm'),
        tools=data.get('tools', 'Default tools'),
        function_calling_llm=data.get('function_calling_llm'),
        max_iter=data.get('max_iter', 10),
        max_rpm=data.get('max_rpm'),
        max_execution_time=data.get('max_execution_time'),
        verbose=data.get('verbose', False),
        allow_delegation=data.get('allow_delegation', True),
        step_callback=data.get('step_callback'),
        cache=data.get('cache', True),
        system_template=data.get('system_template'),
        prompt_template=data.get('prompt_template'),
        response_template=data.get('response_template'),
        project_id=data.get('project_id')
    )
    db.session.add(agent)
    db.session.commit()
    return jsonify({'id': agent.id, 'role': agent.role}), 201

@api.route('/task', methods=['POST'])
def create_task():
    data = request.get_json()
    # Updated to match the Task model changes
    task = Task(
        name=data.get('name'),
        description=data.get('description'),
        agent=data.get('agent'),
        expected_output=data.get('expected_output', 'Default output'),
        tools=data.get('tools', 'Default tools'),
        context=data.get('context', 'Default context'),
        async_execution=data.get('async_execution', False),
        config=data.get('config'),
        output_json=data.get('output_json'),
        output_pydantic=data.get('output_pydantic'),
        output_file=data.get('output_file'),
        callback=data.get('callback'),
        human_input=data.get('human_input', False),
        project_id=data.get('project_id')
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({'id': task.id, 'description': task.description}), 201

@api.route('/project/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = Project.query.get_or_404(project_id)
    agents = [{'id': agent.id, 'role': agent.role} for agent in project.agents]
    tasks = [{'id': task.id, 'description': task.description} for task in project.tasks]
    return jsonify({'id': project.id, 'name': project.name, 'agents': agents, 'tasks': tasks})
