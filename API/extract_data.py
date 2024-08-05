import requests
import os
from enum import Enum
from crewai import Agent, Task, Crew
from langchain_community.chat_models.azure_openai import AzureChatOpenAI
from langchain.agents import AgentType, initialize_agent, load_tools
import importlib
from langchain_core.tools import Tool
#Search tools
from search_tools import SearchTools

llm = AzureChatOpenAI(temperature=0, max_tokens=1000,
                      openai_api_key='some-key',
                      model_name='gpt-35-turbo',
                      openai_api_version='some-version',
                      azure_endpoint='http://10.73.14.148:6257')

# human_tool = load_tools(["human"],
#                         llm = llm)

class process(Enum):
    seq = "sequential"

class data_extraction():
    def __init__(self):
        pass

    def extract_agents():
        url = 'http://127.0.0.1:5000/agents'
        response = requests.get(url)

        agents = {}
        if response.status_code == 200:
            agents_data = response.json()
        else:
            print('agents failure')
            return {}
        for i, agent_data in enumerate(agents_data):
            id = agent_data.get('id')
            tools_names = agent_data.get('tools') if isinstance(agent_data.get('tools'), list) else []
            list_tool = []
            if "search internet" in tools_names:
                list_tool.append(SearchTools.search_internet)
            if "search news" in tools_names:
                list_tool.append(SearchTools.search_news)

            agent = Agent(
                role=agent_data.get('role'),
                goal=agent_data.get('goal'),
                backstory=agent_data.get('backstory'),
                llm=llm if isinstance(agent_data.get('llm'), str) else llm,
                tools=list_tool,
                function_calling_llm=agent_data.get('function_calling_llm'),
                max_iter=agent_data.get('max_iter') if isinstance(agent_data.get('max_iter'), int) else 25,
                max_rpm=agent_data.get('max_rpm'),
                max_execution_time=agent_data.get('max_execution_time'),
                verbose=agent_data.get('verbose') if isinstance(agent_data.get('verbose'), bool) else False,
                allow_delegation=agent_data.get('allow_delegation') if isinstance(agent_data.get('allow_delegation'), bool) else True,
                step_callback=agent_data.get('step_callback'),
                cache=agent_data.get('cache') if isinstance(agent_data.get('True'), bool) else True,
                system_template=agent_data.get('system_template'),
                prompt_template=agent_data.get('prompt_template'),
                response_template=agent_data.get('response_template'),
            )
            agents[id] = agent #{1:Agent_1, 2:Agent_2, etc}

        return agents
    

    def extract_tasks(agents):
        url = 'http://127.0.0.1:5000/tasks'
        response = requests.get(url)

        tasks = {}
        if response.status_code == 200:
            tasks_data = response.json()
        else:
            print('tasks failure')
            return {}
        for i, task_data in enumerate(tasks_data):
            agent_id = task_data.get('agent_id')
            id = task_data.get('id')
            task = Task(
                description=task_data.get('description'),
                agent=agents[agent_id],
                expected_output=task_data.get('expected_output'),
                tools=task_data.get('tools') if isinstance(task_data.get('tools'), list) else [],
                async_execution=task_data.get('async_execution') if isinstance(task_data.get('async_execution'), bool) else False,
                context=task_data.get('context') if isinstance(task_data.get('context'), list) else [],
                config=task_data.get('config') if isinstance(task_data.get('config'), dict) else {},
                output_json=task_data.get('output_json'),
                output_pydantic=task_data.get('output_pydantic'),
                output_file=task_data.get('output_file'),
                output=task_data.get('output'),
                callback=task_data.get('callback'),
                human_input=task_data.get('human_input') if isinstance(task_data.get('human_input'), bool) else False,
            )
            tasks[id] = task

        return tasks


    def extract_projects(agents, tasks):
        url = 'http://127.0.0.1:5000/projects'
        response = requests.get(url)
        project_list = response.json()
        if response.status_code != 200:
            print('projects failure')
            return {}
        nb_projects = len(project_list)

        projects = {}
        for i in range(nb_projects):
            project_id = project_list[i].get('id')
            url = f'http://127.0.0.1:5000/projects/{project_id}'
            response = requests.get(url)
            if response.status_code == 200:
                project_data = response.json()
            else:
                print('projects failure')
                return {}
            
            seq = process.seq

            agent_ids = [agent['id'] for agent in project_data['agents']]
            agent_names = [agents[id] for id in agent_ids]

            task_ids = [task['id'] for task in project_data['tasks']]
            task_names = [tasks[id] for id in task_ids]

            project = Crew(
                agents=agent_names,
                tasks=task_names,
                process=project_data.get('process') if isinstance(project_data.get('process'), Enum) else seq,
                verbose=project_data.get('verbose'), # if isinstance(project_data.get('verbose'), bool) else False,
                manager_llm=project_data.get('manager_llm'), # if isinstance(project_data.get('manager_llm'), str) else llm,
                function_calling_llm=project_data.get('function_calling_llm'), # if isinstance(project_data.get('function_calling_llm'), str) else llm,
                config=project_data.get('config') if isinstance(project_data.get('config'), dict) else {}, #if (isinstance(project_data.get('config'), TEST JSON) or isinstance(project_data.get('config'), dict)) else {},
                max_rpm=project_data.get('max_rpm'),
                language=project_data.get('language') if isinstance(project_data.get('language'), str) else "en",
                language_file=project_data.get('language+file'),
                memory=project_data.get('memory'),
                cache=project_data.get('cache'),
                embedder=project_data.get('embedder'),
                full_output=project_data.get('full_output'),
                step_callback=project_data.get('step_callback'),
                task_callback=project_data.get('task_callback'),
                share_crew=project_data.get('share_crew'),
                output_log_file=project_data.get('output_log_file'),
                manager_agent_id=project_data.get('manager_agent_id'),
                manager_callbacks=project_data.get('manager_callbacks'),
                prompt_file=project_data.get('prompt_file'),
                planning=project_data.get('planning'),
            )
            projects[project_id] = (project_list[i].get('name'), project)

        return projects
