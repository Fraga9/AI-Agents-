from crewai import TaskManager, AgentManager
from agents import AISoftwareCompanyAgent
from tasks import AISoftwareCompanyTasks

agents = AISoftwareCompanyAgent
tasks = AISoftwareCompanyTasks


task_manager = TaskManager() # Initialize the task manager for the simulation
agent_manager = AgentManager() # Initialize the agent manager for the simulation

#Setting up agents
boss = agents.boss_agent
productManager = agents.productManager_agent
architect = agents.architect_agent
projectManager = agents.projectManager_agent
engineer = agents.engineer_agent
QA = agents.QA_agent

#Setting up tasks
set_high_level_requirements_task = tasks.set_high_level_requirements_task(boss)
#
write_tasks_task = tasks.write_tasks_task(projectManager, [set_high_level_requirements_task])
assign_tasks_task = tasks.assign_tasks_task(projectManager, [write_tasks_task])
#
write_PRD_task = tasks.write_PRD_task(productManager, [assign_tasks_task])
revise_PRD_task = tasks.revise_PRD_task(productManager, [write_PRD_task])
#
write_design_task = tasks.write_design_task(architect, [assign_tasks_task])
revise_design_task = tasks.revise_design_task(architect, [write_design_task])
#TODO : what about a task that can be achieved by several agents ?
#And I guess that they receive orders from Project manager ?
review_PRD_task = tasks.review_PRD_task(architect, [revise_PRD_task])
review_code_task = tasks.review_code_task(architect, [debug_code_taskk]) #???
#
write_code_task = tasks.write_code_task(engineer, [assign_tasks_task])
review_code_task = tasks.review_code_task(engineer, [write_code_task])
debug_code_task = tasks.debug_code_task(engineer, [review_code_task])
#
write_tests_task = tasks.write_tests_task(QA, [assign_tasks_task])
run_tests_task = tasks.run_tests_task(QA, [write_tests_task])




