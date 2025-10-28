#!/usr/bin/env python
import argparse
from datetime import datetime
import os
import warnings
from typing import Optional

from deep_researcher.crew import AiResearcher

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run(args: Optional[argparse.Namespace] = None):
    """
    Run the crew.
    """
    topic = args.topic if (args is not None) and hasattr(args, 'topic') else os.getenv('CREW_TOPIC')
    if topic is None:
        raise ValueError("A research topic is required")

    inputs = {
        'topic': topic,
        'current_date': datetime.now().strftime("%B %d, %Y"),  # Use United States date format
    }

    try:
        AiResearcher().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Deep Researcher')
    parser.add_argument(
        '--topic', '-t',
        type=str,
        required=True,
        help='The research topic to investigate'
    )
    args = parser.parse_args()

    # Run the crew
    run(args)