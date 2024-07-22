from flask import Blueprint, request
from flask_restx import Api, Resource, fields, Namespace
from models import db, Project, Agent, Task, Tool

# Blueprint para la API
api_bp = Blueprint('api', __name__)
api = Api(api_bp, version='1.0', title='Project API', description='API endpoints for managing projects, agents, tasks, and tools')

# Modelos utilizando api.model
project_input_model = api.model('Project Input', {
    'name': fields.String(required=True, description='Project Name'),
    'process': fields.String(description='Project Process'),
    'verbose': fields.Boolean(description='Verbose', default=False),
    'manager_llm': fields.String(description='Manager LLM'),
    'function_calling_llm': fields.String(description='Function Calling LLM'),
    'config': fields.String(description='Project Configuration'),
    'max_rpm': fields.Integer(description='Max RPM'),
    'language': fields.String(description='Language'),
    'language_file': fields.String(description='Language File'),
    'memory': fields.String(description='Memory'),
    'cache': fields.Boolean(description='Cache', default=False),
    'embedder': fields.String(description='Embedder'),
    'full_output': fields.Boolean(description='Full Output', default=False),
    'step_callback': fields.String(description='Step Callback'),
    'task_callback': fields.String(description='Task Callback'),
    'share_crew': fields.Boolean(description='Share Crew', default=False),
    'output_log_file': fields.String(description='Output Log File'),
    'manager_agent_id': fields.Integer(description='Manager Agent ID'),
    'manager_callbacks': fields.String(description='Manager Callbacks'),
    'prompt_file': fields.String(description='Prompt File')
})

project_output_model = api.inherit('Project Output', project_input_model, {
    'id': fields.Integer(description='Project ID')
})


agent_input_model = api.model('Agent Input', {
    'role': fields.String(required=True, description='Agent Role'),
    'goal': fields.String(description='Agent Goal'),
    'backstory': fields.String(description='Agent Backstory'),
    'llm': fields.String(description='Agent LLM'),
    'tools': fields.Raw(description='Agent Tools'),
    'function_calling_llm': fields.String(description='Function Calling LLM'),
    'max_iter': fields.Integer(description='Max Iterations'),
    'max_rpm': fields.Integer(description='Max RPM'),
    'max_execution_time': fields.Integer(description='Max Execution Time'),
    'verbose': fields.Boolean(description='Verbose'),
    'allow_delegation': fields.Boolean(description='Allow Delegation'),
    'step_callback': fields.String(description='Step Callback'),
    'cache': fields.Boolean(description='Cache'),
    'system_template': fields.String(description='System Template'),
    'prompt_template': fields.String(description='Prompt Template'),
    'response_template': fields.String(description='Response Template')
})

agent_output_model = api.inherit('Agent Output', agent_input_model, {
    'id': fields.Integer(description='Agent ID')
})


task_input_model = api.model('Task Input', {
    'name': fields.String(required=True, description='Task Name'),
    'description': fields.String(required=True, description='Task Description'),
    'project_id': fields.Integer(required=True, description='Project ID'),
    'agent_id': fields.Integer(required=True, description='Agent ID'),
    'expected_output': fields.String(required=True, description='Expected Output'),
    'tools': fields.String(description='Task Tools'),
    'context': fields.String(description='Task Context'),
    'async_execution': fields.Boolean(description='Async Execution'),
    'config': fields.String(description='Task Configuration'),
    'output_json': fields.String(description='Output JSON'),
    'output_pydantic': fields.String(description='Output Pydantic'),
    'output_file': fields.String(description='Output File'),
    'callback': fields.String(description='Callback Function'),
    'human_input': fields.Boolean(description='Requires Human Input'),
})

task_output_model = api.inherit('Task Output', task_input_model, {
    'id': fields.Integer(description='Task ID')
})


tool_input_model = api.model('Tool Input', {
    'id': fields.Integer(description='Tool ID'),
    'name': fields.String(required=True, description='Tool Name'),
    'description': fields.String(description='Tool Description')
})

tool_output_model = api.inherit('Tool Output', tool_input_model, {
    'id': fields.Integer(description='Tool ID')
})


# Simple models
task_simple_model = api.model('TaskSimple', {
    'id': fields.Integer(description='Task ID'),
    'name': fields.String(description='Task Name'),
    'description': fields.String(description='Task Description'),
})

agent_simple_model = api.model('AgentSimple', {
    'id': fields.Integer(description='Agent ID'),
    'role': fields.String(description='Agent Role'),
    'goal': fields.String(description='Agent Goal'),
})

tool_simple_model = api.model('ToolSimple', {
    'id': fields.Integer(description='Tool ID'),
    'name': fields.String(description='Tool Name'),
    'description': fields.String(description='Tool Description'),
})

# Modifica el modelo del proyecto para incluir listas de relaciones
project_detailed_model = api.inherit('ProjectDetailed', project_output_model, {
    'tasks': fields.List(fields.Nested(task_simple_model)),
    'agents': fields.List(fields.Nested(agent_simple_model)),
    'tools': fields.List(fields.Nested(tool_simple_model)),
})

agent_task_assignment_model = api.model('AgentTaskAssignment', {
    'agent_id': fields.Integer(required=True, description='Agent ID')
})


# Espacios de nombres (namespaces) para cada recurso
ns_project = api.namespace('projects', description='Project operations')
ns_agent = api.namespace('agents', description='Agent operations')
ns_task = api.namespace('tasks', description='Task operations')
ns_tool = api.namespace('tools', description='Tools operations')

# Definición de las clases de recursos para CRUD

# Project Resources
@ns_project.route('/')
class ProjectListResource(Resource):
    @ns_project.marshal_list_with(project_output_model)
    def get(self):
        """ Return the list of all projects """
        projects = Project.query.all()
        return projects

    @ns_project.expect(project_input_model)
    @ns_project.marshal_with(project_output_model, code=201)
    def post(self):
        """ Create a new project """
        data = request.json
        project = Project(**data)
        db.session.add(project)
        db.session.commit()
        return project, 201

@ns_project.route('/<int:id>')
@ns_project.response(404, 'Project not found')
class ProjectResource(Resource):
    @ns_project.marshal_with(project_detailed_model)
    def get(self, id):
        """ Return details of a specific project including tasks, agents, and tools """
        project = Project.query.get_or_404(id)
        project_data = {
            'id': project.id,
            'name': project.name,
            'process': project.process,
            'verbose': project.verbose,
            'manager_llm': project.manager_llm,
            'function_calling_llm': project.function_calling_llm,
            'config': project.config,
            'max_rpm': project.max_rpm,
            'language': project.language,
            'language_file': project.language_file,
            'memory': project.memory,
            'cache': project.cache,
            'embedder': project.embedder,
            'full_output': project.full_output,
            'step_callback': project.step_callback,
            'task_callback': project.task_callback,
            'share_crew': project.share_crew,
            'output_log_file': project.output_log_file,
            'manager_agent_id': project.manager_agent_id,
            'manager_callbacks': project.manager_callbacks,
            'prompt_file': project.prompt_file,
            'tasks': [{'id': task.id, 'name': task.name, 'description': task.description} for task in project.tasks],
            'agents': [{'id': agent.id, 'role': agent.role, 'goal': agent.goal} for agent in project.agents],
            'tools': [{'id': tool.id, 'name': tool.name, 'description': tool.description} for tool in project.tools]
        }
        return project_data

    @ns_project.expect(project_input_model)
    @ns_project.marshal_with(project_output_model)
    def put(self, id):
        """ Update an existing project """
        project = Project.query.get_or_404(id)
        data = request.json
        for key, value in data.items():
            if hasattr(project, key): 
                setattr(project, key, value)
        db.session.commit()
        return project

    @ns_project.response(204, 'Project successfully deleted')
    def delete(self, id):
        """ Delete an existing project """
        project = Project.query.get_or_404(id)
        db.session.delete(project)
        db.session.commit()
        return '', 204

# Agent Resources
@ns_agent.route('/')
class AgentListResource(Resource):
    @ns_agent.marshal_list_with(agent_output_model)
    def get(self):
        """ Return the list of all agents """
        agents = Agent.query.all()
        return agents

    @ns_agent.expect(agent_input_model)
    @ns_agent.marshal_with(agent_output_model, code=201)
    def post(self):
        """ Create a new agent """
        data = request.json
        agent = Agent(**data)
        db.session.add(agent)
        db.session.commit()
        return agent, 201

@ns_agent.route('/<int:id>')
@ns_agent.response(404, 'Agent not found')
class AgentResource(Resource):
    @ns_agent.marshal_with(agent_output_model)
    def get(self, id):
        """ Return details of a specific agent """
        agent = Agent.query.get_or_404(id)
        return agent

    @ns_agent.expect(agent_input_model)
    @ns_agent.marshal_with(agent_output_model)
    def put(self, id):
        """ Update an existing agent """
        agent = Agent.query.get_or_404(id)
        data = request.json
        for key, value in data.items():
            if hasattr(agent, key): 
                setattr(agent, key, value)
        db.session.commit()
        return agent

    @ns_agent.response(204, 'Agent successfully deleted')
    def delete(self, id):
        """ Delete an existing agent """
        agent = Agent.query.get_or_404(id)
        db.session.delete(agent)
        db.session.commit()
        return '', 204

# Tool Resources
@ns_tool.route('/')
class ToolListResource(Resource):
    @ns_tool.marshal_list_with(tool_output_model)
    def get(self):
        """ Return the list of all tools """
        tools = Tool.query.all()
        return tools

    @ns_tool.expect(tool_input_model)
    @ns_tool.marshal_with(tool_output_model, code=201)
    def post(self):
        """ Create a new tool """
        data = request.json
        tool = Tool(**data)
        db.session.add(tool)
        db.session.commit()
        return tool, 201

@ns_tool.route('/<int:id>')
@ns_tool.response(404, 'Tool not found')
class ToolResource(Resource):
    @ns_tool.marshal_with(tool_output_model)
    def get(self, id):
        """ Return details of a specific tool """
        tool = Tool.query.get_or_404(id)
        return tool

    @ns_tool.expect(tool_input_model)
    @ns_tool.marshal_with(tool_output_model)
    def put(self, id):
        """ Update an existing tool """
        tool = Tool.query.get_or_404(id)
        data = request.json
        for key, value in data.items():
            if hasattr(tool, key): 
                setattr(tool, key, value)
        db.session.commit()
        return tool

    @ns_tool.response(204, 'Tool successfully deleted')
    def delete(self, id):
        """ Delete an existing tool """
        tool = Tool.query.get_or_404(id)
        db.session.delete(tool)
        db.session.commit()
        return '', 204

# Task Resources
@ns_task.route('/')
class TaskListResource(Resource):
    @ns_task.marshal_list_with(task_output_model)
    def get(self):
        """ Return the list of all tasks """
        tasks = Task.query.all()
        return tasks

    @ns_task.expect(task_input_model)
    @ns_task.marshal_with(task_output_model, code=201)
    def post(self):
        """ Create a new task """
        data = request.json
        task = Task(**data)
        db.session.add(task)
        db.session.commit()
        return task, 201

@ns_task.route('/<int:id>')
@ns_task.response(404, 'Task not found')
class TaskResource(Resource):
    @ns_task.marshal_with(task_output_model)
    def get(self, id):
        """ Return details of a specific task including the project it belongs to """
        task = Task.query.get_or_404(id)
        task_data = {
            'id': task.id,
            'name': task.name,
            'agent_id': task.agent_id,
            'project_id': task.project_id,
            'description': task.description,
            'expected_output': task.expected_output,
            'tools': task.tools,
            'context': task.context,
            'async_execution': task.async_execution,
            'config': task.config,
            'output_json': task.output_json,
            'output_pydantic': task.output_pydantic,
            'output_file': task.output_file,
            'callback': task.callback,
            'human_input': task.human_input,
            'project': {
                'id': task.project.id,
                'name': task.project.name
            } if task.project else None
        }
        return task_data

    @ns_task.expect(task_input_model)
    @ns_task.marshal_with(task_output_model)
    def put(self, id):
        """ Update an existing task """
        task = Task.query.get_or_404(id)
        data = request.json
        for key, value in data.items():
            if hasattr(task, key): 
                setattr(task, key, value)
        db.session.commit()
        return task

    @ns_task.response(204, 'Task successfully deleted')
    def delete(self, id):
        """ Elimina una tarea existente """
        task = Task.query.get_or_404(id)
        db.session.delete(task)
        db.session.commit()
        return '', 204

# Asignación de agentes y herramientas a proyectos
@ns_project.route('/<int:project_id>/assign_agent')
class AssignAgentToProjectResource(Resource):
    @ns_project.expect(api.model('AgentAssignment', {
        'agent_id': fields.Integer(required=True, description='Agent ID')
    }))
    @ns_project.response(200, 'Agent successfully assigned to project')
    def post(self, project_id):
        """ Assign an agent to a specific project """
        data = request.json
        if not data or 'agent_id' not in data:
            api.abort(400, "Invalid request. Must include agent_id in the JSON body.")
        
        agent_id = data['agent_id']
        project = Project.query.get_or_404(project_id)
        agent = Agent.query.get_or_404(agent_id)
        
        if agent not in project.agents:
            project.agents.append(agent)
            db.session.commit()
            return {'message': 'Agent successfully assigned to project'}, 200
        else:
            return {'message': 'Agent already assigned to project'}, 200

@ns_project.route('/<int:project_id>/assign_tool')
class AssignToolToProjectResource(Resource):
    @ns_project.expect(api.model('ToolAssignment', {
        'tool_id': fields.Integer(required=True, description='Tool ID')
    }))
    @ns_project.response(200, 'Tool successfully assigned to project')
    def post(self, project_id):
        """ Assign a tool to a specific project """
        data = request.json
        if not data or 'tool_id' not in data:
            api.abort(400, "Invalid request. Must include tool_id in the JSON body.")
        
        tool_id = data['tool_id']
        project = Project.query.get_or_404(project_id)
        tool = Tool.query.get_or_404(tool_id)
        
        if tool not in project.tools:
            project.tools.append(tool)
            db.session.commit()
            return {'message': 'Tool successfully assigned to project'}, 200
        else:
            return {'message': 'Tool already assigned to project'}, 200

@ns_task.route('/<int:task_id>/assign_agent')
class AssignAgentToTaskResource(Resource):
    @ns_task.expect(agent_task_assignment_model)
    @ns_task.response(200, 'Agent successfully assigned to task')
    def post(self, task_id):
        """ Asigna un agente a una tarea específica """
        data = request.json
        if not data or 'agent_id' not in data:
            api.abort(400, "Invalid request. Must include agent_id in the JSON body.")
        
        agent_id = data['agent_id']
        task = Task.query.get_or_404(task_id)
        agent = Agent.query.get_or_404(agent_id)
        
        task.agent_id = agent_id
        db.session.commit()
        return {'message': 'Agente asignado a la tarea'}, 200


# Registra los namespaces en la aplicación Flask
api.add_namespace(ns_project)
api.add_namespace(ns_agent)
api.add_namespace(ns_task)
api.add_namespace(ns_tool)


