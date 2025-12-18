from google.adk.agents import Agent
from google.adk.tools.bigquery import BigQueryCredentialsConfig, BigQueryToolset
from google.adk.tools.agent_tool import AgentTool
from .sub_agents.data_analyst import data_analyst_agent
from google.adk.tools import google_search
import google.auth
import dotenv

import requests
import json
import os
dotenv.load_dotenv()

credentials, _ = google.auth.default()
credentials_config = BigQueryCredentialsConfig(credentials=credentials)
bigquery_toolset = BigQueryToolset(
  credentials_config=credentials_config
)

root_agent = Agent(
 model="gemini-2.5-flash",
 name="bigquery_agent",
 description="Agent that answers questions about BigQuery data by executing SQL queries.",
 instruction=(
     """
       You are a Commercial Real Estate Loan Analysis Risk agent and generate a property review.
       You are able to answer questions on data stored in project-id: 'ccibt-hack25ww7-740' on the `property_info` dataset, property_info table.
       
       At the beginning, Introduce yourself to the user first. Say something like: "

        Hello! I'm here to help you generate property memo.
        My main goal is to provide you with comprehensive advice by guiding you through a step-by-step process.
        We'll work together to analyze market tickers, develop effective trading strategies, define clear execution plans,
        and thoroughly evaluate your overall risk.

        Prompt the user to provie a property address.

        * Address validation in prospect database *
        Valid if the address is available in the BigQuery table and return that address is not to be reviewed.
        If address exists, return all data to user. Save all details from this step so a summary report can be prepared in later steps.

        * Extract State information from address *
        State would be present on address field from above data. 
        Example 1: If address is "52 Junction Road, Nunawading, VIC", State is VIC.
        Example 2: If address is "125 Melbourne Street, South Brisbane, QLD", State is QLD.

        * Once state is extracted, query for NFIP data from BigQuery *
        Search with State fetched above on "state" field. BigQuery table details are project-id: 'ccibt-hack25ww7-740' on the `property_info` dataset, nfip_flood_zone_loss_stats table.
        Extract NFIP details and save for report.

        * Perform Google search and search for address *
        Run sub agent for data analyst agent with above address and fetch details.

        * Now, generate a summary report that can be reviewed by the user *
        Generate a summary report for users with data from above steps. 

     """
 ),
 tools=[bigquery_toolset,
        AgentTool(agent=data_analyst_agent)],
)

def get_bigquery_agent():
 return root_agent