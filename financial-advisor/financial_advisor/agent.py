from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk import Agent
from google.adk.tools import google_search
from google.adk.tools.bigquery import BigQueryCredentialsConfig, BigQueryToolset
import google.auth
import dotenv

dotenv.load_dotenv()
MODEL = "gemini-2.5-pro"
credentials, _ = google.auth.default()
credentials_config = BigQueryCredentialsConfig(credentials=credentials)
bigquery_toolset = BigQueryToolset(
  credentials_config=credentials_config
)

bigquery_agent = Agent(
 model="gemini-2.5-flash",
 name="bigquery_agent",
 description="Agent that answers questions about BigQuery data by executing SQL queries.",
 instruction=(
     """
       You are a BigQuery data analysis agent.
       You are able to answer questions on data stored in project-id: 'ccibt-hack25ww7-740' on the commercail real estate customer dataset.
     """
 ),
 tools=[bigquery_toolset]
)
Reporting_Agent = LlmAgent(
    name="Reporting_Agent",
    model="gemini-2.5-flash",
    description=(
        "An agent that can synthesize insights from commercial and flood analysis "
        "to provide comprehensive reporting."
    ),
    instruction=(
        """Generate comprehensive reports synthesizing commercial real estate report

1. Coordinate insights from root_agent
2. Create a commercial credit memo for the risk anlayst to mail to the user"""
    ),
)
data_analyst_agent = Agent(
    model=MODEL,
    name="data_analyst_agent",
    instruction=("""
Agent Role: data_analyst
Tool Usage: Exclusively use the Google Search tool.

Overall Goal: To generate a comprehensive and timely market analysis report for a provided real estate address. This involves iteratively using the Google Search tool to gather a target number of distinct, recent (within a specified timeframe), and insightful pieces of information. The analysis will focus on both SEC-related data and general market/stock intelligence, which will then be synthesized into a structured report, relying exclusively on the collected data.
Input: Use address provided.
Output: Fetch top 5 google results for the address and provide this data back to the user.

"""),
    output_key="market_data_analysis_output",
    tools=[google_search],
)
root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="A helpful assistant for commercial real estate agent.",
    instruction=(
        """You are a Commercial Real Estate Loan Analysis Risk agent and generate a property review.
       You are able to answer questions on data stored in project-id: 'ccibt-hack25ww7-740' on the property_info dataset, property_info table.
       
       At the beginning, Introduce yourself to the user first. Say something like: "

        Hello! I'm here to help you generate property memo.
        My main goal is to provide you with comprehensive advice by guiding you through a step-by-step process.
        We'll work together to analyze market tickers, develop effective trading strategies, define clear execution plans,
        and thoroughly evaluate your overall risk.

        Prompt the user to provie a property address.

        * Address validation in prospect database *
        Valid if the address is available in the BigQuery table and return that address is not to be reviewed.
        If address exists, return all data to user
        Generate comprehensive reports synthesizing commercial real estate report

1. Coordinate insights from root_agent
2. Create a commercial credit memo for the risk anlayst to mail to the user
3. Run data analyst agent with above address and fetch details.
"""
    ),
    #sub_agents=[Reporting_Agent], 
     tools=[
        AgentTool(agent=bigquery_agent),
        AgentTool(agent=data_analyst_agent),
        AgentTool(agent=Reporting_Agent),
    ], # avoid assigning arbitrary fields on pydantic-based Agentadk
)

Commercial_Agent = LlmAgent(
    name="Commercial_Agent",
    model="gemini-2.5-flash",
    description=(
        "An agent that can analyze commercial real estate data and provide insights "
        "based on the user input."
    ),
    instruction=(
        """You are a Commercial Real Estate Loan Analysis Risk agent and generate a property review.
       You are able to answer questions on data stored in project-id: 'ccibt-hack25ww7-740' on the property_info dataset, property_info table.
       
       At the beginning, Introduce yourself to the user first. Say something like: "

        Hello! I'm here to help you generate property memo.
        My main goal is to provide you with comprehensive advice by guiding you through a step-by-step process.
        We'll work together to analyze market tickers, develop effective trading strategies, define clear execution plans,
        and thoroughly evaluate your overall risk.

        Prompt the user to provie a property address.

        * Address validation in prospect database *
        Valid if the address is available in the BigQuery table and return that address is not to be reviewed.
        If address exists, return all data to user"""
    ),
    tools=[
        AgentTool(agent=bigquery_agent),
    ],
)

# Expose the agents from this module without assigning arbitrary attributes
# on the root_agent object (some ADK Agent classes are Pydantic models and
# disallow adding new fields). Use module-level names and a simple registry.
#COMMERCIAL_AGENT = Commercial_Agent
REPORTING_AGENT = Reporting_Agent
SUB_AGENTS = [Reporting_Agent]

try:
    # If the ADK Agent supports registering sub-agents, try to register them.
    if hasattr(root_agent, "add_agent"):
        try:
          #  root_agent.add_agent(Commercial_Agent)
            root_agent.add_agent(Reporting_Agent)
        except Exception:
            # best-effort only; registration failures shouldn't break imports
            pass
except Exception:
    # swallow any unexpected errors during attach so imports remain safe
    pass
