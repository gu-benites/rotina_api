# External Services - external_services.py
import os
import asyncio
import time
import json
import httpx
import pinecone
from openai import OpenAI

# Configuration variables from environment or config.py
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_ORG_ID = os.getenv('OPENAI_ORG_ID')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_REGION = os.getenv('PINECONE_REGION')
PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME')

# Initialize OpenAI client
client = OpenAI(
    organization=OPENAI_ORG_ID,
    api_key=OPENAI_API_KEY
)

# Pinecone-related functions
def initialize_pinecone():
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_REGION)

def connect_to_pinecone_index():
    index = pinecone.Index(PINECONE_INDEX_NAME)
    return index

async def aromachat(search_query):
    print("Getting embeddings from OpenAI...")
    model_embed = os.environ.get("OPENAI_MODEL_EMBED")
    embed_query = await asyncio.to_thread(
        client.embeddings.create, input=search_query, model=model_embed
    )
    embeddings = embed_query.data[0].embedding
    print("Embeddings obtained.")

    # Retry logic for Pinecone connection
    max_retries = 3
    for retry_count in range(max_retries):
        try:
            print("Initializing Pinecone...")
            initialize_pinecone()

            print("Connecting to Pinecone index...")
            index = connect_to_pinecone_index()

            print(f"Searching Pinecone query: {search_query}.")
            query_response = index.query(
                include_values=False,
                include_metadata=True,
                vector=embeddings,
                top_k=5
            )

            pinecone_results = {
                'description': f'context to help answer query: {search_query}. Only use context if relevant information can be found regarding user search_query.',
                'context': []
            }

            for match in query_response.matches:
                if match.score > 0.70:  # Threshold can be adjusted as needed
                    context_text = match.metadata.get('text')
                    pinecone_results['context'].append(context_text)

            print("Results from Pinecone successfully extracted.")
            return pinecone_results
        except Exception as e:
            print(f"Error connecting to Pinecone: {str(e)}")
            if retry_count < max_retries - 1:
                print("Retrying...")
                time.sleep(2)
            else:
                print("Max retries reached. Unable to connect to Pinecone.")
                raise

# You would continue to add more OpenAI or Pinecone interaction functions here as needed.
