from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from typing import List

@CrewBase
class AiResearcher():
    """AiResearcher crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        serper_tool = SerperDevTool()
        self.tools = [serper_tool]

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            verbose=True,
            tools=self.tools,
        )

    @agent
    def reporter(self) -> Agent:
        return Agent(
            config=self.agents_config['reporter'],
            verbose=True,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'],
            output_file='outputs/report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AiResearcher crew"""

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
