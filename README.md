# 🏥 Healthcare Document Analyser

An intelligent healthcare document analysis 
application built with Python and Azure AI Language.

## What it does
- Detects sentiment in clinical notes
- Extracts named entities (people, locations, 
  medications, dates)
- Identifies key medical phrases
- Flags high-risk negative content for review
- Generates structured JSON reports

## Tech stack
- Python 3.9+
- Azure AI Language (TextAnalyticsClient)
- Streamlit (web UI)
- python-dotenv (secure credentials)

## How to run

1. Clone the repo
2. Install dependencies:
pip install -r requirements.txt

3. Create .env file:
AZURE_KEY=your_key_here
AZURE_ENDPOINT=your_endpoint_here

4. Run the web app:
streamlit run app.py

## Project structure
- explore.py — first Azure AI experiments
- analyzer.py — structured NER and sentiment
- healthcare_analyzer.py — full analyzer 
  with JSON output
- app.py — Streamlit web application
- requirements.txt — all dependencies

## Azure AI services used
- Sentiment Analysis
- Named Entity Recognition (NER)
- Key Phrase Extraction
- Language Detection
- Content Safety Flagging

## Part of
Azure AI Engineer Associate (AI-102) 
certification journey