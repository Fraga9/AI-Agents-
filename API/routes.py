from flask import Blueprint, request, jsonify
from flask_restx import api, Resource, fields
from models import db, Project, Agent, Task, Tool
from api import ns_project, ns_agent, ns_task, ns_tool, project_model, agent_model, task_model, tool_model, project_detailed_model, agent_detailed_model, task_detailed_model, tool_detailed_model, agent_task_assignment_model

# Projects
@ns_project.route('/')
class ProjectListResource(Resource):
    @ns_project.marshal_list_with(project_model)
    def get(self):
        """ Retorna la lista de todos los proyectos """
        projects = Project.query.all()
        return projects

    @ns_project.expect(project_model)
    @ns_project.marshal_with(project_model, code=201)
    def post(self):
        """ Crea un nuevo proyecto """
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
        """ Retorna detalles de un proyecto específico """
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

    @ns_project.expect(project_model)
    @ns_project.marshal_with(project_model)
    def put(self, id):
        """ Actualiza un proyecto existente """
        project = Project.query.get_or_404(id)
        data = request.json
        for key, value in data.items():
            if hasattr(project, key): 
                setattr(project, key, value)
        db.session.commit()
        return project

    @ns_project.response(204, 'Project successfully deleted')
    def delete(self, id):
        """ Elimina un proyecto existente """
        project = Project.query.get_or_404(id)
        db.session.delete(project)
        db.session.commit()
        return '', 204

# Asignación de agentes a proyectos
@ns_project.route('/<int:project_id>/assign_agent')
class AssignAgentToProjectResource(Resource):
    @ns_project.expect({'agent_id': fields.Integer(required=True, description='Agent ID')})
    @ns_project.response(200, 'Agent successfully assigned to project')
    def post(self, project_id):
        """ Asigna un agente a un proyecto específico """
        data = request.json
        if not data or 'agent_id' not in data:
            api.abort(400, "Invalid request. Must include agent_id in the JSON body.")
        
        agent_id = data['agent_id']
        project = Project.query.get_or_404(project_id)
        agent = Agent.query.get_or_404(agent_id)
        
        if agent not in project.agents:
            project.agents.append(agent)
            db.session.commit()
            return {'message': 'Agente asignado al proyecto'}, 200
        else:
            return {'message': 'Agente ya asignado al proyecto'}, 200

# Asignación de herramientas a proyectos
@ns_project.route('/<int:project_id>/assign_tool')
class AssignToolToProjectResource(Resource):
    @ns_project.expect({'tool_id': fields.Integer(required=True, description='Tool ID')})
    @ns_project.response(200, 'Tool successfully assigned to project')
    def post(self, project_id):
        """ Asigna una herramienta a un proyecto específico """
        data = request.json
        if not data or 'tool_id' not in data:
            api.abort(400, "Invalid request. Must include tool_id in the JSON body.")
        
        tool_id = data['tool_id']
        project = Project.query.get_or_404(project_id)
        tool = Tool.query.get_or_404(tool_id)
        
        if tool not in project.tools:
            project.tools.append(tool)
            db.session.commit()
            return {'message': 'Herramienta asignada al proyecto'}, 200
        else:
            return {'message': 'Herramienta ya asignada al proyecto'}, 200



# Agents
@ns_agent.route('/')
class AgentListResource(Resource):
    @ns_agent.marshal_list_with(agent_model)
    def get(self):
        """ Retorna la lista de todos los agentes """
        agents = Agent.query.all()
        return agents

    @ns_agent.expect(agent_model)
    @ns_agent.marshal_with(agent_model, code=201)
    def post(self):
        """ Crea un nuevo agente """
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
        """ Retorna detalles de un agente específico """
        agent = Agent.query.get_or_404(id)
        return agent

    @ns_agent.expect(agent_model)
    @ns_agent.marshal_with(agent_model)
    def put(self, id):
        """ Actualiza un agente existente """
        agent = Agent.query.get_or_404(id)
        data = request.json
        for key, value in data.items():
            if hasattr(agent, key): 
                setattr(agent, key, value)
        db.session.commit()
        return agent

    @ns_agent.response(204, 'Agent successfully deleted')
    def delete(self, id):
        """ Elimina un agente existente """
        agent = Agent.query.get_or_404(id)
        db.session.delete(agent)
        db.session.commit()
        return '', 204


# Tools
@ns_tool.route('/')
class ToolListResource(Resource):
    @ns_tool.marshal_list_with(tool_model)
    def get(self):
        """ Retorna la lista de todas las herramientas """
        tools = Tool.query.all()
        return tools

    @ns_tool.expect(tool_model)
    @ns_tool.marshal_with(tool_model, code=201)
    def post(self):
        """ Crea una nueva herramienta """
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
        """ Retorna detalles de una herramienta específica """
        tool = Tool.query.get_or_404(id)
        return tool

    @ns_tool.expect(tool_model)
    @ns_tool.marshal_with(tool_model)
    def put(self, id):
        """ Actualiza una herramienta existente """
        tool = Tool.query.get_or_404(id)
        data = request.json
        for key, value in data.items():
            if hasattr(tool, key): 
                setattr(tool, key, value)
        db.session.commit()
        return tool

    @ns_tool.response(204, 'Tool successfully deleted')
    def delete(self, id):
        """ Elimina una herramienta existente """
        tool = Tool.query.get_or_404(id)
        db.session.delete(tool)
        db.session.commit()
        return '', 204


# Tasks
@ns_task.route('/')
class TaskListResource(Resource):
    @ns_task.marshal_list_with(task_model)
    def get(self):
        """ Retorna la lista de todas las tareas """
        tasks = Task.query.all()
        return tasks

    @ns_task.expect(task_model)
    @ns_task.marshal_with(task_model, code=201)
    def post(self):
        """ Crea una nueva tarea """
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
        """ Retorna detalles de una tarea específica """
        task = Task.query.get_or_404(id)
        return task

    @ns_task.expect(task_model)
    @ns_task.marshal_with(task_model)
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