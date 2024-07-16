from flask import Blueprint, request
from flask_restx import Api, Resource, fields
from models import db, Project, Agent, Task, Tool

# Blueprint para la API
api_bp = Blueprint('api', __name__)
api = Api(api_bp, version='1.0', title='Project API', description='API endpoints for managing projects, agents, tasks, and tools')

# Modelos utilizando api.model
project_model = api.model('Project', {
    'name': fields.String(required=True, description='Project Name'),
    'process': fields.String(description='Project Process'),
    'verbose': fields.Boolean(description='Verbose'),
    'manager_llm': fields.String(description='Manager LLM'),
    'function_calling_llm': fields.String(description='Function Calling LLM'),
    'config': fields.Raw(description='Project Configuration'),
    'max_rpm': fields.Integer(description='Max RPM'),
    'language': fields.String(description='Language'),
    'language_file': fields.String(description='Language File'),
    'memory': fields.Raw(description='Memory'),
    'cache': fields.Boolean(description='Cache'),
    'embedder': fields.Raw(description='Embedder'),
    'full_output': fields.Boolean(description='Full Output'),
    'step_callback': fields.String(description='Step Callback'),
    'task_callback': fields.String(description='Task Callback'),
    'share_crew': fields.Boolean(description='Share Crew'),
    'output_log_file': fields.String(description='Output Log File'),
    'manager_agent_id': fields.Integer(description='Manager Agent ID'),
    'manager_callbacks': fields.Raw(description='Manager Callbacks'),
    'prompt_file': fields.String(description='Prompt File')
})

agent_model = api.model('Agent', {
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

task_model = api.model('Task', {
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

tool_model = api.model('Tool', {
    'name': fields.String(required=True, description='Tool Name'),
    'description': fields.String(description='Tool Description')
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
    @ns_project.marshal_list_with(project_model)
    def get(self):
        """ Return the list of all projects """
        projects = Project.query.all()
        return projects

    @ns_project.expect(project_model)
    @ns_project.marshal_with(project_model, code=201)
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
    @ns_project.marshal_with(project_model)
    def get(self, id):
        """ Return details of a specific project """
        project = Project.query.get_or_404(id)
        return project

    @ns_project.expect(project_model)
    @ns_project.marshal_with(project_model)
    def put(self, id):
        """ Update an existing project """
        project = Project.query.get_or_404(id)
        data = request.json
        project.update(data)
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
    @ns_agent.marshal_list_with(agent_model)
    def get(self):
        """ Return the list of all agents """
        agents = Agent.query.all()
        return agents

    @ns_agent.expect(agent_model)
    @ns_agent.marshal_with(agent_model, code=201)
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
    @ns_agent.marshal_with(agent_model)
    def get(self, id):
        """ Return details of a specific agent """
        agent = Agent.query.get_or_404(id)
        return agent

    @ns_agent.expect(agent_model)
    @ns_agent.marshal_with(agent_model)
    def put(self, id):
        """ Update an existing agent """
        agent = Agent.query.get_or_404(id)
        data = request.json
        agent.update(data)
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
    @ns_tool.marshal_list_with(tool_model)
    def get(self):
        """ Return the list of all tools """
        tools = Tool.query.all()
        return tools

    @ns_tool.expect(tool_model)
    @ns_tool.marshal_with(tool_model, code=201)
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
    @ns_tool.marshal_with(tool_model)
    def get(self, id):
        """ Return details of a specific tool """
        tool = Tool.query.get_or_404(id)
        return tool

    @ns_tool.expect(tool_model)
    @ns_tool.marshal_with(tool_model)
    def put(self, id):
        """ Update an existing tool """
        tool = Tool.query.get_or_404(id)
        data = request.json
        tool.update(data)
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
    @ns_task.marshal_list_with(task_model)
    def get(self):
        """ Return the list of all tasks """
        tasks = Task.query.all()
        return tasks

    @ns_task.expect(task_model)
    @ns_task.marshal_with(task_model, code=201)
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
    @ns_task.marshal_with(task_model)
    def get(self, id):
        """ Returns details of a specific task """
        task = Task.query.get_or_404(id)
        return task

    @ns_task.expect(task_model)
    @ns_task.marshal_with(task_model)
    def put(self, id):
        """ Update an existing task """
        task = Task.query.get_or_404(id)
        data = request.json
        task.update(data)
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
    @ns_project.expect({'agent_id': fields.Integer(required=True, description='Agent ID')})
    @ns_project.response(200, 'Agent successfully assigned to project')
    def post(self, project_id):
        """ Asign an agent to a specific project """
        data = request.json
        agent_id = data.get('agent_id')
        project = Project.query.get_or_404(project_id)
        agent = Agent.query.get_or_404(agent_id)
        project.agents.append(agent)
        db.session.commit()
        return {'message': 'Agent assigned to project'}, 200

@ns_project.route('/<int:project_id>/assign_tool')
class AssignToolToProjectResource(Resource):
    @ns_project.expect({'tool_id': fields.Integer(required=True, description='Tool ID')})
    @ns_project.response(200, 'Tool successfully assigned to project')
    def post(self, project_id):
        """ Asign a tool to a specific project """
        data = request.json
        tool_id = data.get('tool_id')
        project = Project.query.get_or_404(project_id)
        tool = Tool.query.get_or_404(tool_id)
        project.tools.append(tool)
        db.session.commit()
        return {'message': 'Tool assigned to project'}, 200

# Registra los namespaces en la aplicación Flask
api.add_namespace(ns_project)
api.add_namespace(ns_agent)
api.add_namespace(ns_task)
api.add_namespace(ns_tool)

# No es necesario iniciar la aplicación o ejecutarla aquí, este archivo solo define los endpoints y modelos

# Asegúrate de que db y los modelos estén importados correctamente desde models.py
