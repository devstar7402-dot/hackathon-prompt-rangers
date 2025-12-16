
import os
from pathlib import Path
from agents.base_agent import BaseAgent

class Agent(BaseAgent):
    """
    A more capable agent that is aware of the file system.
    Inherits from BaseAgent.
    """
    def __init__(self, name: str, sub_agents: list = None):
        super().__init__(name, sub_agents)
        self._cwd = str(Path.cwd())

    @property
    def cwd(self) -> str:
        """Return the current working directory."""
        return self._cwd

    def get_cwd(self) -> str:
        """
        An alias for the cwd property.
        
        :return: The current working directory as a string.
        """
        return self.cwd

    def run(self, *args, **kwargs):
        """
        The main execution method for an agent.
        Subclasses should override this method.
        """
        print(f"Agent {self.name} is running in {self.get_cwd()}")
        # The default run method does nothing.
        pass

if __name__ == '__main__':
    # Example of how to use the new Agent
    file_system_aware_agent = Agent(name="FileSystemAgent")
    file_system_aware_agent.run()
    print(f"The agent's CWD is: {file_system_aware_agent.get_cwd()}")
