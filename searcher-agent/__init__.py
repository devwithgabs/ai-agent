import os

from dotenv import load_dotenv

load_dotenv()

agent_env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(agent_env_path):
    load_dotenv(dotenv_path=agent_env_path, override=True)


from .agent import root_agent


__all__ = ["root_agent"]
