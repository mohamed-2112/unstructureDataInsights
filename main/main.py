from dotenv import load_dotenv
from pathlib import Path
import logging
import os
from main.agent.agent_runner import agent_runner

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    """
    Main function to run the application.
    This is the entry point.
    """
    load_environment()
    print("Hello and welcome to the application!")
    agent_runner()


def load_environment():
    """
    Load environment variables from the .env file.
    """
    env_path = Path('config') / '.env'
    logging.info(f'filename: {env_path}')
    if env_path.exists():
        try:
            load_dotenv(dotenv_path=env_path)
            openai_key = os.getenv('OPENAI_API_KEY')
            print(openai_key)
            print("Environment variables loaded from .env file.")
        except KeyError:
            raise Exception(f"Couldn't find environment variables in .env.")
    else:
        print(".env file not found. Make sure to create one if environment variables are needed.")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
