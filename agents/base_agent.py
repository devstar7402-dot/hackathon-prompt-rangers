
from __future__ import annotations
from typing import List, Optional

class BaseAgent:
    """
    The base class for all agents in the system, inspired by the google-adk structure.
    Manages the hierarchical relationship between agents.
    """
    def __init__(self, name: str, sub_agents: Optional[List[BaseAgent]] = None):
        self.name = name
        self.parent_agent: Optional[BaseAgent] = None
        self.sub_agents: List[BaseAgent] = sub_agents or []
        
        for agent in self.sub_agents:
            agent.parent_agent = self

    @property
    def root_agent(self) -> BaseAgent:
        """Gets the root agent of this agent."""
        root = self
        while root.parent_agent is not None:
            root = root.parent_agent
        return root

    def find_sub_agent(self, name: str) -> Optional[BaseAgent]:
        """Finds a sub-agent by name."""
        for agent in self.sub_agents:
            if agent.name == name:
                return agent
        return None

    def run(self, *args, **kwargs):
        """
        The main execution method for an agent.
        Subclasses should override this method.
        """
        raise NotImplementedError(f"{self.name} has not implemented the 'run' method.")
