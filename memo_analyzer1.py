import os
from google.cloud import bigquery, language_v1
import vertexai
from vertexai.generative_models import GenerativeModel

# --- Configuration ---
# PLEASE REPLACE THESE VALUES WITH YOUR GCP AND BIGQUERY DETAILS
GCP_PROJECT_ID = "ccibt-hack25ww7-740"
GCP_LOCATION = "us-central1"  # e.g., "us-central1"
BIGQUERY_TABLE_ID = "ccibt-hack25ww7-740.property_info.property_info"

def initialize_vertex_ai():
    """Initializes the Vertex AI SDK."""
    print("Initializing Vertex AI...")
    vertexai.init(project=GCP_PROJECT_ID, location=GCP_LOCATION)
    print("Vertex AI initialized.")

def query_bigquery_data(table_id: str) -> str:
    """
    Connects to BigQuery and fetches the content of the most recent memo.
    
    Args:
        table_id: The full ID of the BigQuery table (project.dataset.table).

    Returns:
        The text content of the memo, or an empty string if not found.
    """
    print(f"Attempting to retrieve memo from BigQuery table: {table_id}")
    try:
        client = bigquery.Client()
        # This query assumes a 'created_at' column to find the latest memo.
        # Adjust the query to match your table's schema.
        query = f"SELECT title FROM `{table_id}` LIMIT 1"
        
        query_job = client.query(query)
        results = query_job.result()
        
        memo_content = ""
        for row in results:
            memo_content = row.memo_content
            break  # We only need the first result
        
        if not memo_content:
            print("Warning: No memo content found in the table.")
        else:
            print("Successfully retrieved memo from BigQuery.")
        return memo_content
    except Exception as e:
        print(f"An error occurred while connecting to BigQuery: {e}")
        return ""

def analyze_memo_content(memo_text: str) -> dict:
    """
    Performs summarization, entity, and sentiment analysis using Google Cloud AI.

    Args:
        memo_text: The text of the memo to analyze.

    Returns:
        A dictionary containing the analysis results.
    """
    if not memo_text:
        return {}

    print("Starting memo analysis with Vertex AI...")
    analysis_results = {}

    try:
        # 1. Summarization with Gemini
        print(" - Generating summary...")
        model = GenerativeModel("gemini-2.5-flash-lite")
        prompt = f"Please provide a concise, professional summary of the following memo:\n\n{memo_text}"
        response = model.generate_content(prompt)
        analysis_results['summary'] = response.text

        # 2. NLP Analysis with Cloud Natural Language API
        print(" - Analyzing entities and sentiment...")
        lang_client = language_v1.LanguageServiceClient()
        document = language_v1.Document(content=memo_text, type_=language_v1.Document.Type.PLAIN_TEXT)
        
        # Entity Analysis
        entities_response = lang_client.analyze_entities(document=document)
        entities = {}
        for entity in entities_response.entities:
            entity_type = language_v1.Entity.Type(entity.type_).name
            if entity_type not in entities:
                entities[entity_type] = []
            # Avoid duplicate entities
            if entity.name not in entities[entity_type]:
                entities[entity_type].append(entity.name)
        analysis_results['entities'] = entities
        
        # Sentiment Analysis
        sentiment_response = lang_client.analyze_sentiment(document=document)
        analysis_results['sentiment'] = {
            "score": f"{sentiment_response.document_sentiment.score:.2f}",
            "magnitude": f"{sentiment_response.document_sentiment.magnitude:.2f}"
        }
        print("Analysis complete.")
        
    except Exception as e:
        print(f"An error occurred during Vertex AI analysis: {e}")

    return analysis_results

def generate_report(analysis: dict):
    """
    Formats and prints the final analysis report to the console.

    Args:
        analysis: A dictionary containing the analysis results.
    """
    if not analysis:
        print("Cannot generate report because analysis results are empty.")
        return

    print("\n\n###################################")
    print("## Commercial Memo Analysis Report ##")
    print("###################################\n")

    # --- Executive Summary ---
    print("--- 1. Executive Summary ---")
    print(analysis.get('summary', 'Not available.'))
    print("\n" + "="*40 + "\n")

    # --- Sentiment Analysis ---
    print("--- 2. Sentiment Analysis ---")
    sentiment = analysis.get('sentiment', {})
    if sentiment:
        score = float(sentiment.get('score', 0))
        sentiment_desc = "Neutral"
        if score > 0.25: sentiment_desc = "Positive"
        elif score < -0.25: sentiment_desc = "Negative"
        print(f"Overall Sentiment: {sentiment_desc} (Score: {sentiment.get('score')}, Magnitude: {sentiment.get('magnitude')})")
        print("\n*Score indicates the overall emotional leaning of the text (positive/negative).")
        print("*Magnitude indicates the overall strength of emotion.")
    else:
        print("Not available.")
    print("\n" + "="*40 + "\n")

    # --- Key Entities ---
    print("--- 3. Key Entities Identified ---")
    entities = analysis.get('entities', {})
    if entities:
        for entity_type, entity_list in entities.items():
            print(f"  - {entity_type}: {', '.join(entity_list)}")
    else:
        print("No entities found.")
    
    print("\n\n--- End of Report ---")


def main():
    """
    Main function to run the memo analysis pipeline.
    """
    if "your-gcp-project-id" in GCP_PROJECT_ID:
        print("ERROR: Please update the GCP_PROJECT_ID and BIGQUERY_TABLE_ID in the script before running.")
        return

    initialize_vertex_ai()
    memo_text = retrieve_memo_from_bigquery(BIGQUERY_TABLE_ID)
    
    if memo_text:
        analysis_results = analyze_memo_content(memo_text)
        generate_report(analysis_results)
    else:
        print("Halting process as no memo could be retrieved.")


if __name__ == "__main__":
    main()
