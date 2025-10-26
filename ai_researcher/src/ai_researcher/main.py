#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from ai_researcher.crew import AiResearcher

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'Large Language Models (LLM)',
        'current_year': str(datetime.now().year),
        'current_month': str(datetime.now().month),
    }

    try:
        AiResearcher().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


if __name__ == "__main__":
    run()