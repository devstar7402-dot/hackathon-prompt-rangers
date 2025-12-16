
import time
from agents.base_agent import BaseAgent
from google.cloud import bigquery
import os

class DataGatheringAgent(BaseAgent):
    def __init__(self, gcp_project_id: str):
        """
        Initializes the DataGatheringAgent with a GCP Project ID.
        :param gcp_project_id: Your Google Cloud Project ID.
        """
        super().__init__(name="DataGatheringAgent")
        if not gcp_project_id:
            raise ValueError("GCP Project ID is required.")
        self.project_id = gcp_project_id
        self.bq_client = bigquery.Client(project=self.project_id)
        print(f"{self.name} initialized for GCP project: {self.project_id}")

    def run(self, property_address: str) -> dict:
        """
        Gathers data for a given property address from BigQuery.
        """
        print(f"Gathering data from BigQuery for: {property_address}...")
        return self._fetch_data_from_bigquery(property_address)

    def _fetch_data_from_bigquery(self, address: str) -> dict:
        """
        Fetches property and insurance data from BigQuery.
        """
        # NOTE: This query assumes a dataset named 'property_data' and tables
        # named 'properties' and 'insurance'. You will need to adjust this
        # to match your actual BigQuery schema.
        query = f"""
            SELECT
                p.year_built,
                p.square_footage,
                p.property_type,
                i.policy_type,
                i.coverage_amount
            FROM
                `{self.project_id}.property_data.properties` AS p
            JOIN
                `{self.project_id}.property_data.insurance` AS i ON p.property_id = i.property_id
            WHERE
                p.address = @address
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("address", "STRING", address),
            ]
        )

        try:
            query_job = self.bq_client.query(query, job_config=job_config)
            results = query_job.result()  # Waits for the job to complete.

            if results.total_rows == 0:
                print(f"No data found for address: {address}")
                return {}

            # Assuming one result for simplicity
            row = list(results)[0]

            data = {
                "property_details": {
                    "address": address,
                    "year_built": row.year_built,
                    "square_footage": row.square_footage,
                    "property_type": row.property_type,
                },
                "insurance_details": {
                    "policy_type": row.policy_type,
                    "coverage_amount": row.coverage_amount,
                },
                # Mocking these for now, can be expanded
                "market_trends": {"vacancy_rate": "5%"},
                "demographics": {"median_income": "$85,000"},
            }
            print("Data gathering complete.")
            return data

        except Exception as e:
            print(f"An error occurred while querying BigQuery: {e}")
            return {}
