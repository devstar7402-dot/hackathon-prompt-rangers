from google.cloud import bigquery

def query_bigquery_data(project_id: str, dataset_id: str, table_id: str):
    """
    Connects to BigQuery and retrieves data from a specified table.

    Args:
        project_id (str): Your Google Cloud project ID.
        dataset_id (str): The ID of the BigQuery dataset.
        table_id (str): The ID of the BigQuery table.
    """
    try:
        # Construct a BigQuery client object.
        # The client will use the default credentials if running in a GCP environment
        # or if you have authenticated locally using gcloud auth application-default login.
        client = bigquery.Client(project=project_id)

        # Construct the fully qualified table ID
        table_ref = f"{project_id}.{dataset_id}.{table_id}"

        # Construct the SQL query
        # This example selects all columns and limits to 100 rows.
        # You can customize this query as needed.
        query = f"SELECT * FROM {table_ref} LIMIT 100"

        print(f"Executing query: {query}")

        # Execute the query
        query_job = client.query(query)

        # Fetch and print the results
        print("Query results:")
        for row in query_job.result():
            # Each row is a Row object, which can be accessed by column name or index
            print(row)
            # Example of accessing specific columns:
            # print(f"Column1: {row['column_name_1']}, Column2: {row.column_name_2}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # --- Configuration ---
    # Replace with your actual Google Cloud Project ID
    your_project_id = "ccibt-hack25ww7-740"
    # Replace with your actual BigQuery Dataset ID
    your_dataset_id = "property_info"
    # Replace with your actual BigQuery Table ID
    your_table_id = "property_info"
    # ---------------------

    if your_project_id == "your-gcp-project-id" or your_dataset_id == "your_bigquery_dataset_id" or your_table_id == "your_bigquery_table_id":
        print("Please update 'your_project_id', 'your_dataset_id', and 'your_table_id' with your actual BigQuery details.")
    else:
        query_bigquery_data(your_project_id, your_dataset_id, your_table_id)