from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Dashboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    agents = db.relationship('Agent', backref='dashboard', lazy=True)
    tasks = db.relationship('Task', backref='dashboard', lazy=True)

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50), nullable=False)
    goal = db.Column(db.String(200), nullable=True)
    backstory_context = db.Column(db.String(200), nullable=True)
    llm = db.Column(db.String(50), nullable=True)
    tools = db.Column(db.String(200), nullable=True)
    max_iter = db.Column(db.Integer, nullable=True)
    dashboard_id = db.Column(db.Integer, db.ForeignKey('dashboard.id'), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    agent = db.Column(db.String(100), nullable=False)
    expected_output = db.Column(db.String(200), nullable=True)
    tools = db.Column(db.String(200), nullable=True)
    context = db.Column(db.String(200), nullable=True)
    dashboard_id = db.Column(db.Integer, db.ForeignKey('dashboard.id'), nullable=False)
