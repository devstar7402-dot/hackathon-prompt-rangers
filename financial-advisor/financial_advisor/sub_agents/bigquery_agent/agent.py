from google.adk.agents import Agent
from google.adk.tools.bigquery import BigQueryCredentialsConfig, BigQueryToolset
import google.auth
import dotenv

dotenv.load_dotenv()

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