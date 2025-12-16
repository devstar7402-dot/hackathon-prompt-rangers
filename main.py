
import os
from agents.orchestrator_agent import OrchestratorAgent

def run_analysis(property_address: str, gcp_project_id: str):
    """
    Initializes the agent pipeline and runs the analysis for a given property address.
    """
    # The OrchestratorAgent is the root agent that manages the entire workflow.
    root_agent = OrchestratorAgent(gcp_project_id=gcp_project_id)
    
    # Run the pipeline
    final_memo = root_agent.run(property_address)
    
    # Print the final result
    print("\n--- Final Generated Memo ---")
    print(final_memo)
    print("----------------------------")

if __name__ == '__main__':
    # Get the GCP Project ID from an environment variable
    gcp_project_id = os.environ.get("GCP_PROJECT_ID")
    
    if not gcp_project_id:
        print("ERROR: The GCP_PROJECT_ID environment variable is not set.")
        print("Please set it to your Google Cloud Project ID.")
        print("export GCP_PROJECT_ID='your-project-id'")
        exit(1)

    # Define the property address to be analyzed
    # This should be an address that exists in your BigQuery table
    sample_address = "101 Digital Avenue, Tech City, TX"
    
    # Run the full analysis
    run_analysis(sample_address, gcp_project_id)

