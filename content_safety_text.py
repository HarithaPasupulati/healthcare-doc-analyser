from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

load_dotenv()

def get_client():
    key = os.getenv("AZURE_KEY")
    endpoint = os.getenv("AZURE_ENDPOINT")
    return TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

def check_content_safety(client, texts):
    print("\n=== CONTENT SAFETY CHECK ===")
    results = client.analyze_sentiment(documents=texts)
    for text, result in zip(texts, results):
        if not result.is_error:
            print(f"\nText: '{text[:60]}...'")
            print(f"  Overall sentiment : {result.sentiment.upper()}")
            print(f"  Positive  : {result.confidence_scores.positive:.2f}")
            print(f"  Neutral   : {result.confidence_scores.neutral:.2f}")
            print(f"  Negative  : {result.confidence_scores.negative:.2f}")
            if result.confidence_scores.negative > 0.7:
                print("  ⚠ WARNING: High negative content detected — review required!")
            elif result.confidence_scores.negative > 0.4:
                print("  ⚡ CAUTION: Moderate negative content detected")
            else:
                print("  ✓ Content appears safe")

if __name__ == "__main__":
    client = get_client()

    documents = [
        "The patient recovered well after surgery and is in stable condition.",
        "The doctor was negligent and the treatment caused serious complications.",
        "Clinical trial results show promising outcomes for cancer patients.",
        "The medication caused severe side effects and the patient deteriorated rapidly."
    ]

    check_content_safety(client, documents)