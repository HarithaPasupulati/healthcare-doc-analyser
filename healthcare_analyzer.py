from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os
import json
from datetime import datetime

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

def analyse_document(client, texts):
    report = []

    sentiment_results = client.analyze_sentiment(documents=texts)
    entity_results = client.recognize_entities(documents=texts)
    keyphrase_results = client.extract_key_phrases(documents=texts)

    for i, (text, sentiment, entities, keyphrases) in enumerate(
        zip(texts, sentiment_results, entity_results, keyphrase_results)
    ):
        doc_report = {
            "document_id": i + 1,
            "text": text,
            "sentiment": {
                "overall": sentiment.sentiment,
                "scores": {
                    "positive": round(sentiment.confidence_scores.positive, 2),
                    "neutral": round(sentiment.confidence_scores.neutral, 2),
                    "negative": round(sentiment.confidence_scores.negative, 2)
                },
                "flag": get_safety_flag(sentiment.confidence_scores.negative)
            },
            "entities": [
                {
                    "text": e.text,
                    "category": e.category,
                    "confidence": round(e.confidence_score, 2)
                }
                for e in entities.entities
            ],
            "key_phrases": keyphrases.key_phrases
        }
        report.append(doc_report)

    return report

def get_safety_flag(negative_score):
    if negative_score > 0.70:
        return "HIGH RISK - Review required"
    elif negative_score > 0.40:
        return "MEDIUM RISK - Monitor"
    else:
        return "SAFE"

def print_report(report):
    print("\n" + "="*60)
    print("       HEALTHCARE DOCUMENT ANALYSIS REPORT")
    print("="*60)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total documents analysed: {len(report)}")
    print("="*60)

    for doc in report:
        print(f"\nDocument {doc['document_id']}:")
        print(f"Text     : {doc['text'][:70]}...")
        print(f"Sentiment: {doc['sentiment']['overall'].upper()} | Flag: {doc['sentiment']['flag']}")
        print(f"Scores   : Positive={doc['sentiment']['scores']['positive']} | Neutral={doc['sentiment']['scores']['neutral']} | Negative={doc['sentiment']['scores']['negative']}")
        entity_str = ", ".join([f"{e['text']} ({e['category']})" for e in doc['entities']])
        print(f"Entities : {entity_str}")
        print(f"Key phrases: {', '.join(doc['key_phrases'])}")
        print("-"*60)

def save_report(report, filename="analysis_report.json"):
    with open(filename, "w") as f:
        json.dump(report, f, indent=4)
    print(f"\nReport saved to {filename} ✅")

if __name__ == "__main__":
    client = get_client()

    print("\nHealthcare Document Analyser")
    print("="*60)
    print("Enter your medical documents below.")
    print("Type each document on a new line.")
    print("Press Enter twice when done.\n")

    documents = []
    while True:
        text = input(f"Document {len(documents)+1}: ")
        if text == "":
            if len(documents) == 0:
                print("Please enter at least one document!")
                continue
            break
        documents.append(text)

    print("\nAnalysing your documents...")
    report = analyse_document(client, documents)
    print_report(report)
    save_report(report)