from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from typing import List

from deep_researcher.tools.pushover_tool import PushoverNotificationTool

@CrewBase
class DeepResearcher():
    """DeepResearcher crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    serper_tool = SerperDevTool(n_results=10)
    pushover_notification_tool = PushoverNotificationTool()

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            verbose=True,
            tools=[self.serper_tool],
            max_iterations=4,
        )

    @agent
    def reporter(self) -> Agent:
        return Agent(
            config=self.agents_config['reporter'],
            verbose=True,
            tools=[],  # No tools for report creation - just writing
        )

    @agent
    def translator(self) -> Agent:
        return Agent(
            config=self.agents_config['translator'],
            verbose=True,
            tools=[],  # No tools for translation - just writing
        )

    @agent
    def notifier(self) -> Agent:
        return Agent(
            config=self.agents_config['notifier'],
            verbose=True,
            tools=[self.pushover_notification_tool],
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
            output_file='outputs/report_en.md',
        )

    @task
    def translation_task(self) -> Task:
        return Task(
            config=self.tasks_config['translation_task'],
            output_file='outputs/report_zh.md',
        )

    @task
    def notification_task(self) -> Task:
        return Task(
            config=self.tasks_config['notification_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the DeepResearcher crew"""

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
