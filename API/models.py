from flask_sqlalchemy import SQLAlchemy
import os
import json

db = SQLAlchemy()

agents_projects = db.Table(
    "agents_projects",
    db.Column("agent_id", db.Integer, db.ForeignKey("agent.id"), primary_key=True),
    db.Column("project_id", db.Integer, db.ForeignKey("project.id"), primary_key=True),
)

tools_projects = db.Table(
    "tools_projects",
    db.Column("tool_id", db.Integer, db.ForeignKey("tool.id"), primary_key=True),
    db.Column("project_id", db.Integer, db.ForeignKey("project.id"), primary_key=True),
)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    tasks = db.relationship("Task", backref="project", lazy=True)
    context = db.Column(db.String(200), nullable=True)  # Optional, specifies the context of the project
    process = db.Column(db.String(100), nullable=True)  # Optional
    verbose = db.Column(db.Boolean, nullable=True)  # Optional
    manager_llm = db.Column(db.String(50), nullable=True)  # Optional, required for hierarchical process
    function_calling_llm = db.Column(db.String(200), nullable=True)  # Optional
    config = db.Column(db.String(200), nullable=True)  # Optional, JSON or Dict[str, Any]
    max_rpm = db.Column(db.Integer, nullable=True)  # Optional
    language = db.Column(db.String(50), nullable=True)  # Optional, defaults to English
    language_file = db.Column(db.String(200), nullable=True)  # Optional
    memory = db.Column(db.String(200), nullable=True)  # Optional, for execution memories
    cache = db.Column(db.Boolean, nullable=True)  # Optional
    embedder = db.Column(db.String(200), nullable=True)  # Optional, configuration for the embedder
    full_output = db.Column(db.Boolean, nullable=True)  # Optional
    step_callback = db.Column(db.String(200), nullable=True)  # Optional, won't override agent-specific callback
    task_callback = db.Column(db.String(200), nullable=True)  # Optional
    share_crew = db.Column(db.Boolean, nullable=True)  # Optional
    output_log_file = db.Column(db.String(200), nullable=True)  # Optional, True or path to log file
    manager_agent_id = db.Column(db.Integer, db.ForeignKey("agent.id"), nullable=True)
    manager = db.relationship("Agent", backref="managed_projects", foreign_keys=[manager_agent_id])
    manager_callbacks = db.Column(db.String(200), nullable=True)  # Optional, list of callback handlers for manager
    prompt_file = db.Column(db.String(200), nullable=True)  # Optional, path to prompt JSON file

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(db.String(50), nullable=False)
    goal = db.Column(db.String(200), nullable=False)
    backstory = db.Column(db.String(200), nullable=False)
    llm = db.Column(db.String(50), default=os.getenv("OPENAI_MODEL_NAME", "gpt-4"), nullable=True)
    tools = db.Column(db.String, default='[]', nullable=True)
    function_calling_llm = db.Column(db.String(200), nullable=True)
    max_iter = db.Column(db.Integer, default=25, nullable=True)
    max_rpm = db.Column(db.Integer, nullable=True)
    max_execution_time = db.Column(db.Integer, nullable=True)
    verbose = db.Column(db.Boolean, default=False, nullable=True)
    allow_delegation = db.Column(db.Boolean, default=True, nullable=True)
    step_callback = db.Column(db.String(200), nullable=True)
    cache = db.Column(db.Boolean, default=True, nullable=True)
    system_template = db.Column(db.String(200), nullable=True)  
    prompt_template = db.Column(db.String(200), nullable=True)
    response_template = db.Column(db.String(200), nullable=True)
    tasks = db.relationship('Task', back_populates='agent')
    projects = db.relationship('Project', secondary=agents_projects, lazy='subquery', backref=db.backref('agents', lazy=True))

@property
def tools_list(self):
    return json.loads(self.tools)

@tools_list.setter
def tools_list(self, value):
    self.tools = json.dumps(value)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String(100), nullable=False)  # Name of the task
    description = db.Column(db.String(200), nullable=False)  # Description of the task
    input = db.Column(db.String(200), nullable=False)  # A detailed description of what the tasks input should look like
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False)
    agent = db.relationship('Agent', back_populates='tasks')
    expected_output = db.Column(db.String(200), nullable=False)  # A detailed description of what the tasks output should look like
    tools = db.Column(db.String(200), nullable=True)  # The functions or capabilities that the agent will use to complete the task
    context = db.Column(db.String(200), nullable=True)  # Specifies tasks whose outputs are used as inputs to this task
    async_execution = db.Column(db.Boolean, nullable=True)  # Specifies if the task should be executed asynchronously
    config = db.Column(db.String(200), nullable=True)  # Additional configuration for the task
    output_json = db.Column(db.String(200), nullable=True)  # Outputs a json object, requiring an openAI client
    output_pydantic = db.Column(db.String(200), nullable=True)  # Outputs a pydantic object, requiring an openAI client
    output_file = db.Column(db.String(200), nullable=True)  # Saves the task output to a file based on json or pydantic
    callback = db.Column(db.String(200), nullable=True)  # A callback function that is called after the task is executed
    human_input = db.Column(db.Boolean, nullable=True)  # Specifies if the task requires human input
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)

class Tool(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    project = db.relationship('Project', secondary=tools_projects, lazy='subquery', backref=db.backref('tools', lazy=True))
