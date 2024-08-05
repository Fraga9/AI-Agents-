from langchain_community.chat_models.azure_openai import AzureChatOpenAI
from crewai import Agent, Task, Crew, Process
from langchain_core.tools import Tool
from flask import Flask, jsonify
from API.extract_data import data_extraction
#Search tools
from langchain_community.utilities import GoogleSerperAPIWrapper


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
        print('project key : ', key, ' Tasks : ', [task.description for task in projects[key][1].tasks], ' Agents : ', [agent.role for agent in projects[key][1].agents])

for key in projects:
    print(f"## Welcome to the Project : {projects[key][0]}")
    results = projects[key][1].kickoff()



