
from agents.base_agent import BaseAgent
from agents.data_gathering_agent import DataGatheringAgent
from agents.analysis_agent import AnalysisAgent
from agents.memo_generation_agent import MemoGenerationAgent

class OrchestratorAgent(BaseAgent):
    def __init__(self, gcp_project_id: str):
        """
        Initializes the OrchestratorAgent which acts as the root agent.
        :param gcp_project_id: The Google Cloud Project ID.
        """
        sub_agents = [
            DataGatheringAgent(gcp_project_id=gcp_project_id),
            AnalysisAgent(),
            MemoGenerationAgent()
        ]
        super().__init__(name="OrchestratorAgent", sub_agents=sub_agents)
        print(f"{self.name} initialized as the root agent.")

    def run(self, property_address: str) -> str:
        """
        Runs the full agent pipeline.

        :param property_address: The address of the property to analyze.
        :return: The final generated memo as a string.
        """
        print("\n--- Starting Automated Memo Generation Pipeline ---")
        
        # Find the sub-agents
        gathering_agent = self.find_sub_agent("DataGatheringAgent")
        analysis_agent = self.find_sub_agent("AnalysisAgent")
        memo_agent = self.find_sub_agent("MemoGenerationAgent")

        if not all([gathering_agent, analysis_agent, memo_agent]):
            raise ValueError("One or more sub-agents were not found.")

        # Run the pipeline
        gathered_data = gathering_agent.run(property_address=property_address)
        
        if not gathered_data:
            return "Could not generate a memo. Failed to gather data from BigQuery."

        analysis_summary = analysis_agent.run(data=gathered_data)
        final_memo = memo_agent.run(
            analysis_summary=analysis_summary, 
            property_address=property_address
        )

        print("--- Pipeline Finished ---")
        return final_memo
