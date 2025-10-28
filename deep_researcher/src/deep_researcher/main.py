#!/usr/bin/env python
import warnings

from datetime import datetime

from deep_researcher.crew import AiResearcher

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'Large Language Models (LLM)',
        'current_date': datetime.now().strftime("%B %d, %Y"),  # Use United States date format
    }

    try:
        AiResearcher().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


if __name__ == "__main__":
    run()