from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("AZURE_KEY")
endpoint = os.getenv("AZURE_ENDPOINT")

client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

documents = [
    "The patient was admitted with severe chest pain and high fever.",
    "The treatment was very successful and the patient recovered quickly.",
    "I am not happy with the service provided at the hospital."
]

print("=== LANGUAGE DETECTION ===")
result = client.detect_language(documents=documents)
for doc in result:
    print(f"Language: {doc.primary_language.name} (confidence: {doc.primary_language.confidence_score:.2f})")

print("\n=== SENTIMENT ANALYSIS ===")
result = client.analyze_sentiment(documents=documents)
for doc in result:
    print(f"Sentiment: {doc.sentiment} | Positive: {doc.confidence_scores.positive:.2f} | Negative: {doc.confidence_scores.negative:.2f}")

print("\n=== KEY PHRASES ===")
result = client.extract_key_phrases(documents=documents)
for doc in result:
    print(f"Key phrases: {', '.join(doc.key_phrases)}")