from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

load_dotenv()

def get_client():
    key = os.getenv("AZURE_KEY")
    endpoint = os.getenv("AZURE_ENDPOINT")
    if not key or not endpoint:
        raise ValueError("Missing AZURE_KEY or AZURE_ENDPOINT in .env file")
    return TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

def detect_language(client, texts):
    print("\n=== LANGUAGE DETECTION ===")
    results = client.detect_language(documents=texts)
    for text, result in zip(texts, results):
        if not result.is_error:
            print(f"Text: '{text[:50]}...'")
            print(f"  Language : {result.primary_language.name}")
            print(f"  Confidence: {result.primary_language.confidence_score:.2f}")
        else:
            print(f"  Error: {result.error}")

def analyze_sentiment(client, texts):
    print("\n=== SENTIMENT ANALYSIS ===")
    results = client.analyze_sentiment(documents=texts)
    for text, result in zip(texts, results):
        if not result.is_error:
            print(f"Text: '{text[:50]}...'")
            print(f"  Sentiment : {result.sentiment.upper()}")
            print(f"  Positive  : {result.confidence_scores.positive:.2f}")
            print(f"  Neutral   : {result.confidence_scores.neutral:.2f}")
            print(f"  Negative  : {result.confidence_scores.negative:.2f}")
        else:
            print(f"  Error: {result.error}")

def extract_key_phrases(client, texts):
    print("\n=== KEY PHRASES ===")
    results = client.extract_key_phrases(documents=texts)
    for text, result in zip(texts, results):
        if not result.is_error:
            print(f"Text: '{text[:50]}...'")
            print(f"  Key phrases: {', '.join(result.key_phrases)}")
        else:
            print(f"  Error: {result.error}")

def extract_entities(client, texts):
    print("\n=== NAMED ENTITY RECOGNITION ===")
    results = client.recognize_entities(documents=texts)
    for text, result in zip(texts, results):
        if not result.is_error:
            print(f"Text: '{text[:50]}...'")
            for entity in result.entities:
                print(f"  Entity: {entity.text:20} | Category: {entity.category:15} | Confidence: {entity.confidence_score:.2f}")
        else:
            print(f"  Error: {result.error}")

if __name__ == "__main__":
    client = get_client()

    documents = [
        "Broad medical scope: A dataset spanning 32 medical and public health subdomains.",
        "Comprehensive Research Backbone: Over 1,850 peer-reviewed journals, books, and more than 750,000 peer-reviewed articles.",
        "High volume: Over 5.5 billion words.",
        "Continuously Updated Resource: Approximately 270 chapters and articles are included annually."
    ]

    detect_language(client, documents)
    analyze_sentiment(client, documents)
    extract_key_phrases(client, documents)
    extract_entities(client, documents)