from langchain_community.chat_models.azure_openai import AzureChatOpenAI
from crewai import Agent, Task, Crew, Process
from flask import Flask, jsonify
import sqlite3
from extract_data import data_extraction

llm = AzureChatOpenAI(temperature=0, max_tokens=1000,
                      openai_api_key='some-key',
                      model_name='gpt-35-turbo',
                      openai_api_version='some-version',
                      azure_endpoint='http://10.73.14.148:6257')


data = data_extraction

#Extract from each projects
agents = data_extraction.extract_agents() #dictionary of all agents {id: Agent}
tasks = data_extraction.extract_tasks(agents) #dictionary of all tasks {id: Task}
projects = data_extraction.extract_projects(agents, tasks) 

for i, agent in agents.items():
    print('agent : ', agent.role)

for i, task in tasks.items():
    print('task : ', task.description, ' Agents : ', task.agent.role)

for key in projects.keys():
        print('project key : ', key, ' Tasks : ', [task.description for task in projects[key].tasks], ' Agents : ', [agent.role for agent in projects[key].agents])

for key in projects:
    results = projects[key].kickoff()


