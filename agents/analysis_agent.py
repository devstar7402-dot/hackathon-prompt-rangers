
import time
from agents.base_agent import BaseAgent

class AnalysisAgent(BaseAgent):
    def __init__(self):
        """
        Initializes the AnalysisAgent.
        """
        super().__init__(name="AnalysisAgent")
        print(f"{self.name} initialized.")

    def run(self, data: dict) -> str:
        """
        Analyzes the given data and generates a summary.

        :param data: A dictionary containing data from the DataGatheringAgent.
        :return: A string containing the analysis summary.
        """
        print("Analyzing data...")
        time.sleep(1)  # Simulate analysis time

        summary = self._generate_summary(data)
        
        print("Analysis complete.")
        return summary

    def _generate_summary(self, data: dict) -> str:
        """
        Generates a summary from the provided data.
        """
        prop_details = data.get("property_details", {})
        market_trends = data.get("market_trends", {})
        demographics = data.get("demographics", {})

        summary = f"""
Executive Summary for: {prop_details.get('address', 'N/A')}
-------------------------------------------------
Property Overview:
- Type: {prop_details.get('property_type', 'N/A')}
- Year Built: {prop_details.get('year_built', 'N/A')}
- Square Footage: {prop_details.get('square_footage', 'N/A')}

Market Analysis:
- Neighborhood Growth: {market_trends.get('neighborhood_growth', 'N/A')}
- Vacancy Rate: {market_trends.get('vacancy_rate', 'N/A')}
- Average Rent (per sq. ft.): {market_trends.get('average_rent_psf', 'N/A')}

Demographic Insights:
- Population Density: {demographics.get('population_density', 'N/A')}
- Median Income: {demographics.get('median_income', 'N/A')}
"""
        return summary.strip()
